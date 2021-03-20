import json
import os

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from YandexSweets.models import Courier
from YandexSweets.tests.post_orders import PostOrders
from YandexSweets.tests.post_couriers import PostCouriers
from YandexSweets.views import OrdersAssignView
from YandexSweetsProject.settings import BASE_DIR


class OrdersAssign(TestCase):

    def test_orders_assign(self):
        # TODO : if there is problem with field existing in model, there will be no messages about fields which
        #  should not be in request
        PostCouriers().test_register_new_couriers()
        PostOrders().test_register_new_orders()
        f = APIRequestFactory()
        test_dir = str(BASE_DIR) + '/' + 'YandexSweets/tests/test_files/orders_assign_data'
        for file in os.listdir(test_dir):
            input = json.loads(open(test_dir + '/' + file, mode='r').read())
            req_body = input['input']
            expect_orders = input['expect']['orders']
            request = f.post('/orders/assign', data=req_body, format='json')
            response = OrdersAssignView.as_view()(request)
            response = json.loads(response.data)
            print(json.dumps(response, indent=2))
            c_orders = Courier.objects.get(pk=req_body['courier_id'])
            c_orders = c_orders.order_set.all()
            orders = [c_order.order_id for c_order in c_orders]
            orders.sort()
            expect_orders.sort()
            assert expect_orders == orders, 'Wrong answer,expect = {},found = {},file = {}'.format(expect_orders,
                                                                                                   orders, file)
