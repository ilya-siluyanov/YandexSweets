from rest_framework.serializers import ModelSerializer

from YandexSweets.models import Order


class K(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
