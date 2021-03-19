import json
import os

from django.test import TestCase
from rest_framework.test import *

from YandexSweets.models import Courier, Order
from YandexSweets.views import CouriersView
from YandexSweetsProject.settings import BASE_DIR


class PostCouriers(TestCase):

    def setUp(self):
        Courier.objects.all().delete()
        Order.objects.all().delete()
        # order_complete_data = json.loads(open('test_files/order_complete_data.json', mode='r').read())
        # orders_assign_data = json.loads(open('test_files/orders_assign_data.json', mode='r').read())
        # orders_data = json.loads(open('test_files/orders_data.json', mode='r').read())
        # patch_courier_data = json.loads(open('test_files/orders_data.json', mode='r').read())

    def test_register_new_courier(self):
        f = APIRequestFactory()
        test_files_dir = str(BASE_DIR) + '/YandexSweets/tests/test_files/couriers_test_data'
        for file in os.listdir(test_files_dir):
            couriers_data = json.loads(open(test_files_dir + '/' + file, mode='r').read())
            req_body = couriers_data['input']
            expect = couriers_data['expect']['fields_with_errors']
            request = f.post('/couriers', req_body, format='json')
            response = CouriersView.as_view()(request)
            res_body = json.loads(response.data)
            if 'validation_error' in res_body.keys():
                res_body = res_body['validation_error']['couriers']
                for courier in res_body:
                    for field in courier.keys():
                        if field == 'id':
                            continue
                        if field == 'non_field_errors':
                            field = courier[field].split(': ')[1]
                        assert field in expect, 'There should be error with the field {},file={}'.format(field,
                                                                                                         file)
            else:
                assert len(expect) == 0, 'There should be not any errors'
