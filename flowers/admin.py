from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Flower

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Flower)
class FlowerAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('title', 'description')