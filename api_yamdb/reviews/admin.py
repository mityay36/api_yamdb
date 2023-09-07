from django.contrib import admin

from users.models import User

from .models import Category, Genre, GenreTitle, Title


@admin.register(Title, Genre, Category, GenreTitle, User)
class TitleAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    empty_value_diplay = "-пусто-"
