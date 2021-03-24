import json
import os

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from YandexSweets.tests.post_orders_assign import OrdersAssign
from YandexSweets.views import CouriersView
from YandexSweetsProject.settings import BASE_DIR


class PatchCourierData(TestCase):
    def test_patch_data(self):
        OrdersAssign().test_orders_assign()
        f = APIRequestFactory()
        test_data_dir = str(BASE_DIR) + '/YandexSweets/tests/test_files/couriers_patch_data'
        for file in sorted(os.listdir(test_data_dir)):
            print(file)
            print()
            input = json.loads(open(test_data_dir + '/' + file, mode='r').read())
            courier_id = input['id']
            data = input['data']
            status_code = input['expect']
            request = f.patch('/couriers', data=data, format='json')
            response = CouriersView.as_view()(request, courier_id)
            print(response.status_code, response.data)
            assert response.status_code == status_code, 'Error: exp {},got {},file={}'.format(status_code,
                                                                                              response.status_code,
                                                                                              file)
            print()
