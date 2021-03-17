from django.db import models
from django.db.models import fields
from django.contrib.postgres import fields as pg_fields


class Order(models.Model):
    order_id = fields.IntegerField(primary_key=True)
    weight = fields.FloatField()
    region = fields.IntegerField()
    delivery_hours = pg_fields.ArrayField(pg_fields.ArrayField(fields.IntegerField(), size=2))
