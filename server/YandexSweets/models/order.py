from collections import deque
from typing import List, Tuple

from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models import fields, ForeignKey, CASCADE

from .courier import Courier
from .delivery_pack import DeliveryPack
from ..time_utils import parse_period


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
        timeline = self.create_timeline(courier)
        h = 0
        intersection_start = -1
        for timestamp in timeline:
            h += timestamp[1]
            if h > 1 and timestamp[1] == 1:
                intersection_start = timestamp[0]
            if h == 1 and timestamp[1] == -1:
                if timestamp[0] - intersection_start >= 1:
                    return True
        return False

    def create_timeline(self, courier: Courier) -> List[Tuple[int, int]]:
        def sorting_function(x):
            return parse_period(x)[0]

        working_timeline = deque()
        courier.working_hours.sort(key=sorting_function)
        self.delivery_hours.sort(key=sorting_function)
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
                    timeline.append(delivery_period)
                    delivery_timeline.popleft()
                elif working_period[1] < delivery_period[1]:
                    timeline.append(working_period)
                    working_timeline.popleft()
                else:
                    timeline.append(delivery_period)
                    delivery_timeline.popleft()
            else:
                timeline.append(delivery_period)
                delivery_timeline.popleft()
        while len(working_timeline) > 0:
            timeline.append(working_timeline[0])
            working_timeline.popleft()
        while len(delivery_timeline) > 0:
            timeline.append(delivery_timeline[0])
            delivery_timeline.popleft()
        return timeline

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get_list_of_fields(self):
        return self._meta.get_fields()
