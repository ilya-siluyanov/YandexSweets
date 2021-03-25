import json
import requests as req

couriers = {
    "data": [
        {
            "courier_id": 1,
            "courier_type": "car",
            "regions": [1],
            "working_hours": ["12:00-13:00"]

        },
        {
            "courier_id": 2,
            "courier_type": "bike",
            "regions": [2],
            "working_hours": ["13:00-14:00"]
        },
        {
            "courier_id": 3,
            "courier_type": "car",
            "regions": [1],
            "working_hours": ["12:00-13:00"]
        }

    ]
}

orders = {
    "data": [
        {
            "order_id": 1,
            "weight": 8,
            "region": 1,
            "delivery_hours": ["09:00-18:00"]
        },
        {
            "order_id": 2,
            "weight": 12,
            "region": 2,
            "delivery_hours": ["13:20-14:00"]
        },
        {
            "order_id": 3,
            "weight": 25,
            "region": 1,
            "delivery_hours": ["12:00-18:00"]
        }
    ]
}

headers = {
    'Content-Type': 'application/json'
}
base = 'http://localhost:8000/'
response = req.post(base + 'couriers', data=json.dumps(couriers),
                    headers=headers)
print(response.text)
response = req.post(base + 'orders', data=json.dumps(orders),
                    headers=headers)
print(response.text)

orders_assign = {
    "courier_id": 1
}
response = req.post(base + 'orders/assign', data=json.dumps(orders_assign), headers=headers)
print(response.text)

orders_patch = {
    "courier_type": "foot"
}

response = req.patch(base + 'couriers/1', data=json.dumps(orders_patch), headers=headers)
print(response.text)
response = req.patch(base + 'couriers/1', data=json.dumps(orders_patch), headers=headers)
print(response.text)
response = req.patch(base + 'couriers/1', data=json.dumps(orders_patch), headers=headers)
print(response.text)

orders_complete = {
    "courier_id": 1,
    "order_id": 1,
    "complete_time": "2021-03-25T11:28:01.42Z"
}
response = req.post(base + 'orders/complete', data=json.dumps(orders_complete), headers=headers)
print(response.text)
response = req.post(base + 'orders/complete', data=json.dumps(orders_complete), headers=headers)
print(response.text)
response = req.post(base + 'orders/complete', data=json.dumps(orders_complete), headers=headers)
print(response.text)

response = req.get(base + 'couriers/1')
print(response.text)
