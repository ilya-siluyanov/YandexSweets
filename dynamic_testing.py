import json

import requests as req
from datetime import datetime as dt
import time

base = 'http://127.0.0.1:8000/'
headers = {
    'Content-Type': 'application/json'
}


def request(method, url, data={}):
    print(method(base + url, data=json.dumps(data), headers=headers).text)


couriers = {
    "data": [
        {
            "courier_id": 1,
            "courier_type": "bike",
            "regions": [1],
            "working_hours": ["00:00-23:59"]
        },
    ]
}

orders = {
    "data": [
        {
            "order_id": 1,
            "weight": 1.5,
            "region": 1,
            "delivery_hours": ["14:00-16:00", "19:00-20:00"]
        },
        {
            "order_id": 2,
            "weight": 25,
            "region": 1,
            "delivery_hours": ["00:00-12:01", "20:00-23:59"]
        },
        {
            "order_id": 3,
            "weight": 14.99,
            "region": 1,
            "delivery_hours": ["00:00-12:01", "20:00-23:59"]
        },
        {
            "order_id": 4,
            "weight": 10,
            "region": 1,
            "delivery_hours": ["00:00-12:01", "20:00-23:59"]
        },
    ]
}

request(req.post, 'couriers', couriers)
request(req.post, 'orders', orders)
request(req.post, 'orders/assign', {'courier_id': 1})
