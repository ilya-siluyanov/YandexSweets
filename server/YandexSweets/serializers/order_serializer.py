from datetime import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from ..models import Courier
from ..models.order import Order
from ..time_utils import get_start_end_period, is_correct_hours


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(validators=[UniqueValidator(queryset=Order.objects.all())])
    weight = serializers.FloatField()
    region = serializers.IntegerField()
    delivery_hours = serializers.ListField(allow_empty=False, child=serializers.CharField(max_length=12))
    courier = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, many=True,
                                                 queryset=Courier.objects.all())
    assign_to_courier_time = serializers.DateTimeField(required=False)
    completed_time = serializers.DateTimeField(required=False)
    delivery_type = serializers.CharField(max_length=4, required=False)

    def validate_order_id(self, value):
        if type(value) is not int:
            raise ValidationError('Id must be integer')
        if value <= 0:
            raise ValidationError('Id must be positive integer')
        return value

    def validate_weight(self, value):
        if value is None:
            raise ValidationError('Value is absent')

        if type(value) in (float, int):
            if value < 0.01 or value > 50:
                raise ValidationError('Value is out of bounds [0.01;50] : {}'.format(value))
            return value
        else:
            raise ValidationError('Type of regions is not float : {}'.format(type(value)))

    def validate_region(self, value):
        if value is None:
            raise ValidationError('Region must be specified')
        if type(value) is not int:
            raise ValidationError('Region must be exactly one integer')
        if value <= 0:
            raise ValidationError('Region must be positive integer')
        return value

    def validate_delivery_hours(self, value):
        if value is None:
            raise ValidationError('Value is absent')
        if type(value) is not list:
            raise ValidationError('Delivery hours must be enumerated in list data structure')
        if len(value) == 0:
            raise ValidationError('There must be at least one delivery period')

        for delivery_period in value:
            if type(delivery_period) is not str:
                raise ValidationError('Working period regions type is not string')
            try:
                for hour_stamp in get_start_end_period(delivery_period):
                    if not is_correct_hours(hour_stamp):
                        raise ValidationError()
            except Exception:
                raise ValidationError('Incorrect delivery period: {}'.format(delivery_period))
        return value

    def validate_assign_to_courier_time(self, value):
        if value is None:
            raise ValidationError('Value is absent')
        if type(value) is not list:
            raise ValidationError('Time of order assignment must be exactly one timestamp')
        try:
            res = dt.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            if res != value:
                raise Exception()
            return value
        except Exception:
            raise ValidationError('incorrect delivery_timestamp')

    def validate_courier(self, value: Courier):
        try:
            c = Courier.objects.filter(pk=value.courier_id).all()
            return value
        except Courier.DoesNotExist:
            raise ValidationError('There is no such a courier with id {c_id}'.format(c_id=value.courier_id))

    def validate_completed_time(self, value):
        if value is None:
            raise ValidationError('Value is absent')
        try:
            self.validate_delivery_hours(value)
            return value
        except ValidationError:
            raise ValidationError('incorrect timestamp of order completion')

    def validate_delivery_type(self, value):
        if value is None:
            raise ValidationError('Delivery type must be specified')
        if type(value) is not str:
            raise ValidationError('Delivery type must be exactly one string')
        if value not in Courier.COURIER_MAX_WEIGHT.keys():
            message = 'Courier type must be one of these types: [{types}]. Input regions : {input_c_type}' \
                .format(types=', '.join(Courier.COURIER_MAX_WEIGHT.keys()), input_c_type=value)
            raise ValidationError(message)
        return value

    def update(self, instance: Order, validated_data: dict):
        for key in validated_data.keys():
            instance[key] = validated_data[key]
        instance.save()
        return instance

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
