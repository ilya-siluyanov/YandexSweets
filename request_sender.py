import json

import requests as req

from YandexSweetsProject.settings import BASE_DIR


def send(path, file_name, method):
    print(method.__name__ + ' ' + path + ' ' + file_name)
    f = open(file_name, mode='r')
    json_body = f.read()
    json_body = json.loads(json_body)
    json_body = json.dumps(json_body)
    response = method(url="http://localhost:8000" + path, json=json_body)
    print(response.json())
    print()


send('/couriers', str(BASE_DIR) + '/test_files/couriers_data.json', req.post)
send('/orders', str(BASE_DIR) + '/test_files/orders_data.json', req.post)
send('/orders/assign', str(BASE_DIR) + '/test_files/orders_assign_data.json', req.post)
send('/orders/assign', str(BASE_DIR) + '/test_files/orders_assign_data.json', req.post)
send('/orders/complete', str(BASE_DIR) + '/test_files/order_complete_data.json', req.post)
send('/couriers/1', str(BASE_DIR) + '/test_files/order_complete_data.json', req.get)
