from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=100)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name!r}"


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        verbose_name_plural = ('Товары')
        verbose_name = ('Товар')

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(null=False, blank=True, verbose_name='Описание')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    # reviews =
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name!r} {self.price!r}"


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, verbose_name='Текст отзыва', help_text='Тут Ваш отзыв')
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True)

    class Meta:
        verbose_name_plural = ('Отзывы')
        verbose_name = ('Отзыв')

    def __str__(self):
        return f'{self.user} - {self.product}'

    def view_reviews(self):
        return self.text if len(self.text) < 15 else (self.text[:15] + '...')
    # view_reviews.short_description = 'Комментарий'