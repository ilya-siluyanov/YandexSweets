import json
import logging

import requests as req

logging.basicConfig(filename='prof_helper.log', format='%(name)s:%(asctime)s\t%(message)s')


def url(path: str) -> str:
    return "http://localhost:8080/" + path


def get_formatted_time(time: int) -> str:
    hours = time // 60
    minutes = time - hours * 60
    res = list(map(str, [hours, minutes]))
    for ind, t in enumerate(res):
        if len(str(t)) != 2:
            res[ind] = '0' + str(t)
    return ':'.join([res[0], res[1]])


def request(method, path: str, body: dict) -> req.Response:
    headers: dict = {"content-type": "application/json"}
    response = method(url(path), data=json.dumps(body), headers=headers)
    logging.warning(f"{response.content.decode()} {response.status_code}")
    return response


def generate_courier(amount=1):
    """
    generates a courier with around 8640 time intervals of working time
    (in seconds from day start) - 0 + 4*t - 1 + *4t from 00:00 to 23:59
    """
    req_body = {
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'car',
                'regions': [1, 2, 3, 4],
                'working_hours': [

                ]
            }
        ]
    }

    for t in range(10000):
        if len(req_body['data'][0]['working_hours']) >= amount:
            break
        date_start = get_formatted_time(4 * t)
        date_end = get_formatted_time(4 * t + 1)
        req_body['data'][0]['working_hours'].append("-".join((date_start, date_end)))
    request(req.post, 'couriers', body=req_body)


def generate_order(amount=1):
    """
    generates an order with around 8640 time intervals of working time
    (in seconds from day start) - 2 + 4*t - 3 + *4t from 00:00 to 23:59
    """
    req_body = {
        'data': [
            {
                'order_id': 1,
                'weight': 10.5,
                'region': 1,
                'delivery_hours': [

                ]
            }
        ]
    }

    for t in range(10000):
        if len(req_body['data'][0]['delivery_hours']) >= amount:
            break
        date_start = get_formatted_time(4 * t + 2)
        date_end = get_formatted_time(4 * t + 3)
        req_body['data'][0]['delivery_hours'].append("-".join((date_start, date_end)))
    request(req.post, 'orders', body=req_body)


def main():
    n = 200
    generate_courier(n)
    generate_order(n)
    request(req.post, 'orders/assign', body={'courier_id': 1})


if __name__ == "__main__":
    main()
