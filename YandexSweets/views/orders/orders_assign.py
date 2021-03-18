import json
from datetime import datetime as dt

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
        except Courier.DoesNotExist as e:
            res_body = json.dumps(e.args)
            return Response(data=res_body, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects \
            .filter(courier__courier_id__isnull=True) \
            .filter(completed_time__isnull=True) \
            .filter(region__in=courier.regions) \
            .filter(weight__lte=Courier.COURIER_MAX_WEIGHT[courier.courier_type])

        for order in orders:
            for delivery_hour in order.delivery_hours:
                found = False
                for working_hour in courier.working_hours:
                    if inside_bounds(delivery_hour, working_hour):
                        order.courier = courier
                        order.assign_to_courier_time = dt.now()
                        order.save()
                        found = True
                        break
                if found:
                    break
        response_body = {
            'orders': [{'id': order.order_id} for order in orders]
        }

        if len(orders) > 0:
            courier.last_order_complete = dt.now()
            courier.save()
            response_body['assign_time'] = get_formatted_current_time()

        return Response(data=json.dumps(response_body), status=status.HTTP_200_OK)
