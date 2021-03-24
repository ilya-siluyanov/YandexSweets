from django.test import TestCase
from rest_framework.test import APIRequestFactory

from YandexSweets.models import Courier
from YandexSweets.tests.post_orders_complete import PostOrdersComplete
from YandexSweets.views import CouriersView


class GetCouriersData(TestCase):
    def test_get_couriers(self):
        PostOrdersComplete().test_complete_order()
        print("GET /couriers")
        f = APIRequestFactory()
        for courier in Courier.objects.all():
            request = f.get('/couriers')
            response = CouriersView.as_view()(request, courier.courier_id)
            print(response.status_code, response.data)
            assert response.status_code == 200, "Expect status code 200"
