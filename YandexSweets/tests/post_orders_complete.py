import json
import os

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from YandexSweets.tests.patch_courier_data import PatchCourierData
from YandexSweets.views import OrdersCompleteView
from YandexSweetsProject.settings import BASE_DIR


# noinspection PyMethodMayBeStatic

class PostOrdersComplete(TestCase):
    def test_complete_order(self):
        PatchCourierData().test_patch_data()
        # TODO : if there is problem with field existing in model, there will be no messages about fields which
        #  should not be in request

        f = APIRequestFactory()
        test_files_dir = str(BASE_DIR) + '/YandexSweets/tests/test_files/orders_complete_data'
        for file in os.listdir(test_files_dir):
            input_data = json.loads(open(test_files_dir + '/' + file, mode='r').read())
            req_body = input_data['input']
            expect = input_data['expect']
            request = f.post('orders/complete', data=req_body, format='json')
            response = OrdersCompleteView.as_view()(request)
            status_code = response.status_code
            print(status_code, json.dumps(response.data, indent=2))
            assert expect['status_code'] == status_code, \
                'Expected the same codes, got {} and {}, file={}'.format(expect['status_code'], status_code,
                                                                         file)
