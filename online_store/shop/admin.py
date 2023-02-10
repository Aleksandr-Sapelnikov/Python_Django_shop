from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']


@admin.register(Product)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity']
