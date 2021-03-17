import requests as req
import json


def post(path, file_name):
    f = open(file_name, mode='r')
    json_body = f.read()
    print(json_body)
    json_body = json.loads(json_body)
    json_body = json.dumps(json_body)
    response = req.post(url="http://localhost:8000" + path, json=json_body)
    print(json.loads(response.content))


post('/couriers', 'couriers_data.json')
post('/orders', 'orders_data.json')
