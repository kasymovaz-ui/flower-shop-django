from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField("Категория", max_length=100)

    def __str__(self):
        return self.name

class Flower(models.Model):
    title = models.CharField("Название", max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='flowers')
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Остаток", default=0)
    image = models.ImageField("Фото", upload_to='flowers/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            n = 1
            while Flower.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{n}"
                n += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('flower_detail', args=[self.pk])