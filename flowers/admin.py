from django.contrib import admin
from .models import Category, Flower

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'available')
    list_filter = ('category', 'available')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')