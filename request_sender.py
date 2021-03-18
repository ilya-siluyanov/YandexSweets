import json

import requests as req


def send(path, file_name, method):
    print(method.__name__ + ' ' + path + ' ' + file_name)
    f = open(file_name, mode='r')
    json_body = f.read()
    json_body = json.loads(json_body)
    json_body = json.dumps(json_body)
    response = method(url="http://localhost:8000" + path, json=json_body)
    print(response.json())
    print()


send('/couriers', 'files/couriers_data.json', req.post)
send('/orders', 'files/orders_data.json', req.post)
send('/orders/assign', 'files/orders_assign_data.json', req.post)
send('/orders/complete', 'files/order_complete_data.json', req.post)
send('/couriers/1', 'files/order_complete_data.json', req.get)
