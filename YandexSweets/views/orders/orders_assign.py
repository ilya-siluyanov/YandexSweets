import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.models.order import Order
from YandexSweets.time_utils import inside_bounds, get_formatted_current_time


class OrdersAssignView(APIView):
    @staticmethod
    def post(request):
        req_body = json.loads(request.data)
        try:
            courier = Courier.objects.get(pk=req_body['courier_id'])
        except Courier.DoesNotExist:
            res_body = {
                'description': 'There is no such a courier with id=' + str(req_body['courier_id'])
            }
            res_body = json.dumps(res_body)
            return Response(data=res_body, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(courier__courier_id__isnull=True)
        orders = orders.filter(region__in=courier.regions)
        orders = orders.filter(
            weight__lte=Courier.COURIER_MAX_WEIGHT[courier.courier_type])
        orders_copy = orders[:]
        orders = []

        for order in orders_copy:
            for delivery_hour in order.delivery_hours:
                found = False
                for working_hour in courier.working_hours:
                    if inside_bounds(delivery_hour, working_hour):
                        orders.append(order)
                        found = True
                        break
                if found:
                    break

        for order in orders:
            order.courier = courier
            order.save()
        response_body = {
            'orders': [{'id': order.order_id} for order in orders]
        }

        if len(orders) > 0:
            response_body['assign_time'] = get_formatted_current_time()

        return Response(data=json.dumps(response_body), status=status.HTTP_200_OK)
