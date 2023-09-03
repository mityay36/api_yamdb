from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Category, Genre, Title, User


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

    def validate(self, data):
        if Review.objects.filter(
                author=self.context['request'].user,
                title=self.context.get('view').kwargs.get('title_id')
        ).exists() and self.context.get('request').method == 'POST':
            raise serializers.ValidationError(
                'You cannot leave a second review for this title.'
            )
        return data

    def validate_score(self, value):
        if isinstance(value, int) and 1 <= value <= 10:
            return value
        raise serializers.ValidationError(
            'score - should be integer from 1 to 10'
        )


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
