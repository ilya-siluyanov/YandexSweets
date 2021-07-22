from rest_framework.serializers import ModelSerializer

from ..models import Order


class K(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
