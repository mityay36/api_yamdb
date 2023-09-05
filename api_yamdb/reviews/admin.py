from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title, User


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category')
    empty_value_diplay = '-пусто-'


admin.site.register(User)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(GenreTitle)
