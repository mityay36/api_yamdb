from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )

    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,

    )

    class Meta:
        verbose_name = 'Категория'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Индетификатор'
    )

    class Meta:
        verbose_name = 'Жанр'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):

    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        db_index=True
    )

    descriprion = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    year = models.IntegerField(
        verbose_name='Дата выхода'
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        ordering = ('name',)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )

    text = models.TextField(
        verbose_name='Текст отзыва'
    )

    score = models.IntegerField()

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    text = models.TextField(
        verbose_name='Текст комментария'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ('pub_date',)

    def __str__(self):
        return self.name
