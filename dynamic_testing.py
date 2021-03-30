import json

from requests import *
from datetime import datetime as dt

base = 'http://127.0.0.1:8000/'
headers = {
    'Content-Type': 'application/json'
}


def request(method, url, data={}):
    print(method(base + url, data=json.dumps(data), headers=headers).text)


request(post, 'couriers', {
    "data": [
        {
            "courier_id": 1,
            "courier_type": "car",
            "regions": [1],
            "working_hours": ["00:00-23:59"]
        }
    ]
})

request(post, 'orders', {
    'data': [
        {
            'order_id': 1,
            'weight': 3.5,
            'region': 1,
            'delivery_hours': ['10:00-11:00']
        },
        {
            'order_id': 2,
            'weight': 10,
            'region': 1,
            'delivery_hours': ['10:00-11:00']
        },
        {
            'order_id': 3,
            'weight': 20,
            'region': 1,
            'delivery_hours': ['10:00-11:00']
        },
        {
            'order_id': 4,
            'weight': 15,
            'region': 1,
            'delivery_hours': ['10:00-11:00']
        },
    ]
})

request(post, 'orders/assign', {'courier_id': 1})

request(patch, 'couriers/1', {'courier_type': 'foot'})
request(post, 'orders/assign', {'courier_id': 1})
request(post, 'orders/complete', {'order_id': 1, 'courier_id': 1, 'complete_time': dt.utcnow().isoformat() + 'Z'})
request(get, 'couriers/1')
request(post, 'orders/assign', {'courier_id': 1})
