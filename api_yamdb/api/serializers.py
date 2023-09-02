from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Category, Genre, Title, User
from .permissions import IsAdminOrStaff


class GenreField(serializers.SlugRelatedField):

    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class CategoryField(serializers.SlugRelatedField):

    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=serializers.PrimaryKeyRelatedField(read_only=True)
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('pub_date',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            )
        ]

    def validate_score(self, value):
        if isinstance(value, int) and 1 <= value <= 10:
            return value
        raise serializers.ValidationError(
            'score - should be integer from 1 to 10'
        )


class UserSerializer(serializers.ModelSerializer):
    permission_classes = (IsAdminOrStaff,)

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
    genre = GenreField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=False,
        many=True
    )
    category = CategoryField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )
    rating = serializers.IntegerField(
        required=False
    )

    class Meta:
        model = Title
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Title
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)
