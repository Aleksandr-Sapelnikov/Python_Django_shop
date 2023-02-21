from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализация в случае успешной оплаты"""
    class Meta:
        model = Order
        fields = ('status',)

    def update(self, instance, validated_data):
        instance.status = True
        instance.save()
        return instance


class OrderError(serializers.ModelSerializer):
    """Сериализация в случае ошибке при оплате"""
    class Meta:
        model = Order
        fields = ('error_text',)

    def update(self, instance, validated_data):
        instance.error_text = 'Ошибка при оплате заказа'
        instance.save()
        return instance
