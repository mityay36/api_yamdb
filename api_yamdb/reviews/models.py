from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

from .validators import validate_title_year


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )

    slug = models.SlugField(
        max_length=50,
        verbose_name="slug",
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )

    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Индетификатор"
    )

    class Meta:
        verbose_name = "Жанр"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Название", db_index=True
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание"
    )
    year = models.IntegerField(
        verbose_name="Дата выхода", validators=(validate_title_year,)
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        default=None,
    )

    class Meta:
        verbose_name = "Произведение"
        ordering = ("name",)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Жанр",
    )


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    score = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        error_messages={"validators": "Оценка должна быть от 1 до 10!"},
        verbose_name="Оценка произведения",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв"
    )
    text = models.TextField(verbose_name="Текст комментария")
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации комментария"
    )

    class Meta:
        verbose_name = "Комментарий"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
