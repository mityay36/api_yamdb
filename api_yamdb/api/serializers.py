from rest_framework import serializers

from reviews.models import Review, Category, Genre, Title, User


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'text', 'author', 'pub_date')
