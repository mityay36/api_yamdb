from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from api.mixins import ModelMixinSet
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (AdminOnly, AuthorOrCanEditOrReadOnly,
                          CanEditOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrCanEditOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (CanEditOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (CanEditOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (CanEditOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    filterset_class = TitleFilter

    def get_queryset(self):
        queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrCanEditOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review_pk(self):
        return self.kwargs.get('review_id')

    def get_queryset(self):
        queryset = get_object_or_404(
            Review,
            pk=self.get_review_pk()
        ).comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.get_review_pk()
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


class SignUpView(
    RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        if User.objects.filter(
                username=self.request.data.get('username'),
                email=self.request.data.get('email')
        ).exists():
            return self.retrieve(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        username = serializer.data["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.email_user(
            subject='confirmation_code',
            message=f'Ваш код - {user.confirmation_code}',
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenViewBase):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('=username',)
    lookup_fields = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_object(self):
        username = self.kwargs.get('pk')
        user = get_object_or_404(User, username=username)
        return user

    @action(methods=['get', 'post', 'patch', 'put', 'delete'], detail=False)
    def me(self, request):
        if request.method == 'GET':
            user = User.objects.get(username=request.user.username)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH' or request.method == 'PUT':
            partial = True if request.method == 'PATCH' else False
            user = User.objects.get(username=request.user.username)
            data = request.data.copy()
            data['role'] = user.role
            serializer = self.get_serializer(
                user,
                data=data,
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(user, '_prefetched_objects_cache', None):
                user._prefetched_objects_cache = {}

            return Response(serializer.data)

        if request.method == 'POST':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            raise MethodNotAllowed(method='DELETE')

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        return (AdminOnly(),)
