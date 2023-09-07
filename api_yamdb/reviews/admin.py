from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title, User


@admin.register(Title, User, Genre, Category, GenreTitle)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "year", "category")
    search_fields = ("name",)
    list_filter = ("year", "category")
    empty_value_diplay = "-пусто-"
