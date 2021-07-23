from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models import fields, ForeignKey, CASCADE

from .courier import Courier
from .delivery_pack import DeliveryPack
from .. import time_utils


class Order(models.Model):
    order_id = fields.IntegerField(primary_key=True)
    weight = fields.FloatField()
    region = fields.IntegerField()
    delivery_hours = pg_fields.ArrayField(fields.CharField(max_length=12))

    delivery_pack = ForeignKey(DeliveryPack, on_delete=CASCADE, default=None, blank=True, null=True)
    delivery_time = fields.IntegerField(default=None, blank=True, null=True)

    def is_completed(self):
        return self.delivery_time is not None

    def set_completed(self, seconds: int):
        if not self.is_completed():
            self.delivery_time = seconds

    def is_inside_working_time(self, courier: Courier):
        for available_period in self.delivery_hours:
            for delivery_period in courier.working_hours:
                result = time_utils.inside_bounds(available_period, delivery_period)
                if result:
                    return True
        return False

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get_list_of_fields(self):
        return self._meta.get_fields()
