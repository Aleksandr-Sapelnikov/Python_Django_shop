from django.contrib import admin
from .models import Category


@admin.register(Category)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']

