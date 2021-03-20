from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from YandexSweets.models import Courier
from YandexSweets.time_utils import *

courier_field_list = []


class CourierSerializer(serializers.Serializer):
    courier_id = serializers.IntegerField(validators=[UniqueValidator(queryset=Courier.objects.all())])
    courier_type = serializers.ChoiceField(Courier.COURIER_TYPE_CHOICES)
    regions = serializers.ListField(child=serializers.IntegerField())
    working_hours = serializers.ListField(child=serializers.CharField(max_length=12))

    def validate_courier_type(self, value):
        if value not in Courier.COURIER_MAX_WEIGHT.keys():
            message = 'Courier type must be one of these types: [{types}]. Input regions : {input_c_type}' \
                .format(types=', '.join(Courier.COURIER_MAX_WEIGHT.keys()), input_c_type=value)
            raise ValidationError(message)
        return value

    def validate_regions(self, regions):
        if regions is None or len(regions) == 0:
            raise ValidationError('Courier must work in at least one region')
        if type(regions) is not list:
            raise ValidationError('Regions must be enumerated in list data structure')

        for region in regions:
            if type(region) is not int:
                raise ValidationError('Region must be a decimal value')
            if region <= 0:
                raise ValidationError('Region must be a positive integer')
        return regions

    def validate_working_hours(self, working_hours):
        if type(working_hours) is not list:
            raise ValidationError('Working hours must be enumerated in list data structure')
        if len(working_hours) == 0:
            raise ValidationError('There should be at least one working period')
        for working_period in working_hours:
            if type(working_period) is not str:
                raise ValidationError('Working period regions type is not string')
            try:
                for hour_stamp in get_start_end_period(working_period):
                    if not is_correct_hours(hour_stamp):
                        raise ValidationError()
            except Exception:
                raise ValidationError('Incorrect working period: {}'.format(working_period))

        return working_hours

    def update(self, instance: Courier, validated_data: dict):
        for key in validated_data.keys():
            instance[key] = validated_data[key]
        instance.save()
        return instance

    def create(self, validated_data):
        return Courier.objects.create(**validated_data)

    def validate(self, data: dict):
        c = Courier()
        # TODO: we can make code faster
        if len(courier_field_list) == 0:
            for field in c.get_list_of_fields():
                try:
                    field = field.attname
                    courier_field_list.append(field)
                except Exception:
                    pass
        for key in self.initial_data.keys():
            if key not in courier_field_list:
                raise ValidationError('Unexpected field: ' + key)
        return data
