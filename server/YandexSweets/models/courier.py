from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models import fields


class Courier(models.Model):
    courier_id = fields.IntegerField(primary_key=True)

    foot = 'foot'
    bike = 'bike'
    car = 'car'

    COURIER_MAX_WEIGHT = {
        foot: 10,
        bike: 15,
        car: 50
    }
    COURIER_TYPE_CHOICES = (
        (foot, foot),
        (bike, bike),
        (car, car)
    )

    courier_type = fields.CharField(max_length=4
                                    , choices=COURIER_TYPE_CHOICES
                                    , default='foot', null=False, blank=False)

    regions = pg_fields.ArrayField(fields.IntegerField())

    working_hours = pg_fields.ArrayField(fields.CharField(max_length=12))

    def assign_pack(self, delivery_pack, timestamp):
        delivery_pack.courier = self
        delivery_pack.assign_time = timestamp
        delivery_pack.delivery_type = self.courier_type
        delivery_pack.last_complete_time = timestamp
        delivery_pack.total_weight = 0
        delivery_pack.save()

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get_list_of_fields(self):
        return self._meta.get_fields()
