import json
import os

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from YandexSweets.models import Courier
from YandexSweets.tests.post_couriers import PostCouriers
from YandexSweets.tests.post_orders import PostOrders
from YandexSweets.views import OrdersAssignView
from YandexSweetsProject.settings import BASE_DIR


class OrdersAssign(TestCase):

    def test_orders_assign(self):
        # TODO : if there is problem with field existing in model, there will be no messages about fields which
        #  should not be in request

        PostCouriers().test_register_new_couriers()
        PostOrders().test_register_new_orders()
        f = APIRequestFactory()
        test_files_dir = str(BASE_DIR) + '/' + 'YandexSweets/tests/test_files/orders_assign_data'
        files = os.listdir(test_files_dir)
        files.sort()
        for file in files:
            print(file)
            print()
            input = json.loads(open(test_files_dir + '/' + file, mode='r').read())
            req_body = input['input']
            expect_orders = input['expect']['orders']
            request = f.post('/orders/assign', data=req_body, format='json')
            response = OrdersAssignView.as_view()(request)
            status_code = response.status_code
            response = response.data
            print(status_code, json.dumps(response, indent=2))
            if status_code == 200:
                c_orders = response['orders']
            else:
                c_orders = {}
            orders = [c_order['id'] for c_order in c_orders]
            orders.sort()
            expect_orders.sort()
            assert expect_orders == orders, 'Wrong answer,expect = {},found = {},file = {}'.format(expect_orders,
                                                                                                   orders, file)
            print()
