from django.db import models
from django.db.models import fields
from django.contrib.postgres import fields as pg_fields


class Courier(models.Model):
    courier_id = fields.IntegerField(primary_key=True)
    COURIER_TYPE_CHOICES = (
        ("foot", "foot"),
        ("bike", "bike"),
        ("car", "car")
    )
    courier_type = fields.CharField(max_length=4
                                    , choices=COURIER_TYPE_CHOICES
                                    , default="foot")

    regions = pg_fields.ArrayField(fields.IntegerField())
    working_hours = pg_fields.ArrayField(fields.CharField(max_length=12))