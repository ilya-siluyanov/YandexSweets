from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models import fields
from rest_framework.validators import UniqueValidator

from .courier import Courier


class Order(models.Model):
    order_id = fields.IntegerField(primary_key=True)
    weight = fields.FloatField()
    region = fields.IntegerField()
    delivery_hours = pg_fields.ArrayField(fields.CharField(max_length=12))
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, default=None, blank=True, null=True)
    assign_to_courier_time = fields.DateTimeField(null=True)
    completed_time = fields.DateTimeField(null=True)
    delivery_type = fields.CharField(max_length=4, choices=Courier.COURIER_TYPE_CHOICES, null=True)

    def is_completed(self):
        return self.completed_time is not None

    def set_completed(self, timestamp):
        if not self.is_completed():
            self.completed_time = timestamp

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get_list_of_fields(self):
        return self._meta.get_fields()
