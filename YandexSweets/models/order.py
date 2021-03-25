from collections import deque
from typing import List, Tuple

from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models import fields

from YandexSweets.models.courier import Courier
from YandexSweets.time_utils import parse_period


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

    def is_inside_working_time(self, courier: Courier):
        timeline = self.create_timeline(courier)
        h = 0
        for timestamp in timeline:
            h += timestamp[1]
            if h == 2:
                return True
        return False

    def create_timeline(self, courier: Courier) -> List[Tuple[int, int]]:
        working_timeline = deque()
        for working_period in courier.working_hours:
            start, end = parse_period(working_period)
            working_timeline.append((start, 1))
            working_timeline.append((end, -1))
        delivery_timeline = deque()
        for delivery_period in self.delivery_hours:
            start, end = parse_period(delivery_period)
            delivery_timeline.append((start, 1))
            delivery_timeline.append((end, -1))
        timeline = []
        while len(working_timeline) > 0 and len(delivery_timeline) > 0:
            working_period = working_timeline[0]
            delivery_period = delivery_timeline[0]

            if working_period[0] < delivery_period[0]:
                timeline.append(working_period)
                working_timeline.popleft()
            elif working_period[0] == delivery_period[0]:
                if working_period[1] > delivery_period[1]:
                    timeline.append(working_period)
                    working_timeline.popleft()
                elif working_period[1] < delivery_period[1]:
                    timeline.append(delivery_period)
                    delivery_timeline.popleft()
                else:
                    if working_period[1] == 1:
                        timeline.append(working_period)
                        working_timeline.popleft()
                    else:
                        timeline.append(delivery_period)
                        delivery_timeline.popleft()
            else:
                timeline.append(delivery_period)
                delivery_timeline.popleft()
        return timeline

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get_list_of_fields(self):
        return self._meta.get_fields()
