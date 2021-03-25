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

response = req.post('http://localhost:8000/couriers', data=json.dumps(couriers),
                    headers={'Content-Type': 'application/json'})
print(response.text)
response = req.post('http://localhost:8000/orders', data=json.dumps(orders),
                    headers={'Content-Type': 'application/json'})
print(response.text)
