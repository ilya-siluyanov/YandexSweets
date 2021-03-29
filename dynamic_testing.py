import json
import requests as req

couriers = {
    "data": [
        {
            "courier_id": 2,
            "courier_type": "car",
            "regions": [1],
            "working_hours": ["10:00-11:01", "08:00-09:00", "12:00-13:00"]
        }
    ]
}

orders = {
    "data": [
        {
            "order_id": 5,
            "weight": 8,
            "region": 1,
            "delivery_hours": ["11:00-12:00"]
        },
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
    "courier_id": 2
}
response = req.post(base + 'orders/assign', data=json.dumps(orders_assign), headers=headers)
print(response.text)
# body = {
#     "working_hours": ["10:00-11:01"]
# }
# response = req.patch(base + 'couriers/2', data=json.dumps(body), headers=headers)
# print(response.text)
body = {
    "working_hours": ["09:00-09:01"]
}

response = req.patch(base + 'couriers/2', data=json.dumps(body), headers=headers)
print(response.text)

orders_assign = {
    "courier_id": 2
}
response = req.post(base + 'orders/assign', data=json.dumps(orders_assign), headers=headers)

print(response.text)
body = {
    "courier_id": 2,
    "order_id": 5,
    "complete_time": "2021-03-29T12:06:01.42Z"
}

response = req.post(base + 'orders/complete', data=json.dumps(body), headers=headers)
print(response.text)

body = {
    "courier_id": 2,
    "order_id": 2,
    "complete_time": "2021-03-29T12:06:01.42Z"
}

response = req.post(base + 'orders/complete', data=json.dumps(body), headers=headers)
print(response.text)
