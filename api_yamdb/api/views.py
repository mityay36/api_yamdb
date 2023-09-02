from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import CanEditOrReadOnly
from .serializers import (
    ReviewSerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    CategorySerializer,
    UserSerializer
)
from reviews.models import Review, Title, Category, Genre, Comment, User


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (CanEditOrReadOnly,)

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer

    def get_queryset(self):
        queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
