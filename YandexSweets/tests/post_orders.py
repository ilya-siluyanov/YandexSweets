import json
import os

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from YandexSweets.views import OrdersView
from YandexSweetsProject.settings import BASE_DIR


# noinspection PyMethodMayBeStatic
class PostOrders(TestCase):
    def test_register_new_orders(self):
        # TODO : if there is problem with field existing in model, there will be no messages about fields which
        #  should not be in request
        factory = APIRequestFactory()
        test_files_dir = str(BASE_DIR) + '/YandexSweets/tests/test_files/orders_test_data'
        for file in os.listdir(test_files_dir):
            orders_data = json.loads(open(test_files_dir + '/' + file, mode='r').read())
            # orders_data['input']['data'] = [orders_data['input']['data']]
            # open(test_files_dir + '/' + file, mode='w').write(json.dumps(orders_data, indent=2))
            req_body = orders_data['input']
            expect = orders_data['expect']['fields_with_errors']
            if len(expect) == 0:
                print(file)
            request = factory.post('/orders', req_body, format='json')
            response = OrdersView.as_view()(request)
            res_body = json.loads(response.data)
            print(json.dumps(res_body, indent=2))
            if 'validation_error' in res_body.keys():
                res_body = res_body['validation_error']['orders']
                for order in res_body:
                    for field in order.keys():
                        if field == 'id':
                            continue
                        if field == 'non_field_errors':
                            field = order[field].split(': ')[1]
                        assert field in expect, 'There should be error with the field {},file={}'.format(field,
                                                                                                         file)
            else:
                assert len(expect) == 0, 'There should be not any errors, file={}'.format(file)
