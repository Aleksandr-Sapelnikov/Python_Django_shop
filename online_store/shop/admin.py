from django.contrib import admin
from .models import Category, Product, Reviews, Order, OrderItem


@admin.register(Category)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']


@admin.register(Product)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity']


@admin.register(Reviews)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'view_reviews', 'created']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'delivery_type', 'payment_method', 'created']
    list_filter = ['delivery_type', 'created', 'status', 'payment_method']
    inlines = [OrderItemInline]
