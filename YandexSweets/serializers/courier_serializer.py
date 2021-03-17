from rest_framework import serializers

from YandexSweets.models import Courier


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']
