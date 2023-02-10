from django.contrib import admin
from .models import Category, Product, Reviews


@admin.register(Category)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']


@admin.register(Product)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity']


@admin.register(Reviews)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'view_reviews', 'created']
