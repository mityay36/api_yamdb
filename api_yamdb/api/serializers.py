from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_title_year


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
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=serializers.PrimaryKeyRelatedField(read_only=True)
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date", "title")

    def validate(self, data):
        if (
            Review.objects.filter(
                author=self.context["request"].user,
                title=self.context.get("view").kwargs.get("title_id"),
            ).exists()
            and self.context.get("request").method == "POST"
        ):
            raise serializers.ValidationError(
                "You cannot leave a second review for this title."
            )
        return data

    def validate_score(self, value):
        if isinstance(value, int) and 1 <= value <= 10:
            return value
        raise (serializers.ValidationError(
            "score should be integer from 1 to 10"
        ))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "role": user.role,
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        fields = "__all__"
        model = Title

    def validate_year(self, value):
        return validate_title_year(value)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    review = serializers.HiddenField(
        default=serializers.PrimaryKeyRelatedField(read_only=True)
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date", "review")
        read_only_fields = (
            "id",
            "pub_date",
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError(
                'Имя "me" нельзя использовать в качестве никнейма.'
            )
        return username

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.email_user(
            subject="confirmation_code",
            message=f"Ваш код - {user.confirmation_code}",
            fail_silently=False,
        )
        return {
            "email": user.email,
            "username": user.username,
        }


class TokenSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user = None
        self.fields["password"].required = False

    class Meta:
        model = User
        fields = ("username", "confirmation_code")

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
        }
        confirm_code = None
        if "request" in self.context:
            authenticate_kwargs["request"] = self.context["request"]
            confirm_code = self.context["request"].data["confirmation_code"]
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            raise NotFound("Пользователь не существует!.")
        if self.user.confirmation_code != confirm_code:
            raise serializers.ValidationError("Неверный код подтверждения.")
        access = AccessToken.for_user(self.user)
        return {"token": str(access)}
