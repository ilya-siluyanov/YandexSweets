from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models import fields

from YandexSweets.time_utils import inside_bounds


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
        (bike, foot),
        (car, foot)
    )

    courier_type = fields.CharField(max_length=4
                                    , choices=COURIER_TYPE_CHOICES
                                    , default='foot')

    regions = pg_fields.ArrayField(fields.IntegerField())
    working_hours = pg_fields.ArrayField(pg_fields.ArrayField(fields.IntegerField(), size=2))

    def make_order_free(self, order):
        if order not in self.order_set.all():
            return
        order.courier_id = None
        order.save()

    def is_inside_working_time(self, order):
        for working_hour in self.working_hours:
            for delivery_hour in order.delivery_hours:
                if inside_bounds(delivery_hour, working_hour):
                    return True
        return False

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
