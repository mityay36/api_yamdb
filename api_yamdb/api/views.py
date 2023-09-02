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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CanEditOrReadOnly,)

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
