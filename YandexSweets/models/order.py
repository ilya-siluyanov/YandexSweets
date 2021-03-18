from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models import fields

from .courier import Courier


class Order(models.Model):
    order_id = fields.IntegerField(primary_key=True)
    weight = fields.FloatField()
    region = fields.IntegerField()
    delivery_hours = pg_fields.ArrayField(pg_fields.ArrayField(fields.IntegerField(), size=2))
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, default=None, blank=True, null=True)
    completed_time = fields.DateTimeField(null=True)

    def is_completed(self):
        return self.completed_time is not None

    def set_completed(self, timestamp):
        if not self.is_completed():
            self.completed_time = timestamp
