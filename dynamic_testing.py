import json
import requests as req

headers = {
    'Content-Type': 'application/json'
}
base = 'http://127.0.0.1:8000/'

couriers = {
    "data": [
        {
            "courier_id": 1,
            "courier_type": "bike",
            "regions": [1],
            "working_hours": ["00:00-23:59"]
        }
    ]
}

orders = {
    "data": [
        {
            "order_id": 1,
            "weight": 25,
            "region": 1,
            "delivery_hours": ["11:00-12:00"]
        },
        {
            "order_id": 2,
            "weight": 13,
            "region": 1,
            "delivery_hours": ["11:00-12:00"]
        },
        {
            "order_id": 3,
            "weight": 8,
            "region": 1,
            "delivery_hours": ["11:00-12:00"]
        },
    ]
}

response = req.post(base + 'couriers', data=json.dumps(couriers),
                    headers=headers)
print(response.text)
response = req.post(base + 'orders', data=json.dumps(orders),
                    headers=headers)
print(response.text)

body = {
    "courier_id": 1
}

response = req.post(base + 'orders/assign', data=json.dumps(body), headers=headers)
print(response.text)

body = {
    "courier_type": "car"
}

response = req.patch(base + 'couriers/1', data=json.dumps(body), headers=headers)
print(response.text)

body = {
    "courier_id": 1
}

response = req.post(base + 'orders/assign', data=json.dumps(body), headers=headers)
print(response.text)

body = {
    "courier_id": 1,
    "order_id": 2,
    "complete_time": "2021-03-29T20:50:01.42Z"
}

response = req.post(base + 'orders/complete', data=json.dumps(body), headers=headers)
print(response.text)

body = {
    "courier_id": 1
}

response = req.post(base + 'orders/assign', data=json.dumps(body), headers=headers)
print(response.text)

body = {
    "courier_id": 1,
    "order_id": 3,
    "complete_time": "2021-03-29T20:50:01.42Z"
}

response = req.post(base + 'orders/complete', data=json.dumps(body), headers=headers)
print(response.text)

response = req.get(base + 'couriers/1')
print(response.text)

body = {
    "courier_id": 1
}

response = req.post(base + 'orders/assign', data=json.dumps(body), headers=headers)
print(response.text)

body = {
    "courier_id": 1,
    "order_id": 1,
    "complete_time": "2021-03-29T20:55:01.42Z"
}

response = req.post(base + 'orders/assign', data=json.dumps(body), headers=headers)
