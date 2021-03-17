from rest_framework import serializers

from YandexSweets.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'weight', 'region', 'delivery_hours']