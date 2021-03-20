import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from YandexSweets.tests.post_orders_assign import OrdersAssign
from YandexSweets.views import CouriersView


class PatchCourierData(TestCase):
    def test_patch_data(self):
        OrdersAssign().test_orders_assign()
        f = APIRequestFactory()
        data = {
            'courier_type': 'bike'
        }
        request = f.patch('/couriers', data=data, format='json')
        response = CouriersView.as_view()(request, 10)
        print(response.data)
