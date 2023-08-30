from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, CategoryViewSet, GenreViewSet,
    TitleViewSet, ReviewViewSet, CommentViewSet
)


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'genres', GenreViewSet, basename='genre')
v1_router.register(r'titles', TitleViewSet, basename='title')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
