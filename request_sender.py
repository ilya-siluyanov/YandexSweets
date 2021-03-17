import requests as req
import json

f = open('couriers_data.json', mode='r')


def post_couriers():
    json_body = f.read()
    print(json_body)
    json_body = json.loads(json_body)
    json_body = json.dumps(json_body)
    response = req.post(url="http://localhost:8000/couriers", json=json_body)
    print(json.loads(response.content))

def post_orders():
    pass

post_couriers()
