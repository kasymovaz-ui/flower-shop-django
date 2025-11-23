from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Flower(models.Model):
    title = models.CharField("Название цветка", max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='flowers')
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Остаток на складе", default=0)
    available = models.BooleanField("В наличии", default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Цветок"
        verbose_name_plural = "Цветы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('flower_detail', args=[self.slug])