import json
from django.utils import timezone as dt
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.models.order import Order
from YandexSweets.models.pydantic import OrdersAssign
from YandexSweets.time_utils import inside_bounds, get_formatted_current_time


class OrdersAssignView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        req_body = request.data
        try:
            req_body = OrdersAssign.parse_obj(req_body)
            courier = Courier.objects.get(pk=req_body.courier_id)
        except (Courier.DoesNotExist, ValidationError) as e:
            print(e.args)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(courier__courier_id__isnull=True)
        orders = orders.filter(completed_time__isnull=True)
        orders = orders.filter(region__in=courier.regions)
        orders = orders.filter(weight__lte=Courier.COURIER_MAX_WEIGHT[courier.courier_type])
        current_time = dt.now()
        response_body = {
            'orders': []
        }
        for order in orders:
            if order.is_inside_working_time(courier):
                order.courier = courier
                order.assign_to_courier_time = current_time
                order.save()
                response_body['orders'].append({'id': order.order_id})

        courier.save()
        if len(response_body['orders']) > 0:
            response_body['assign_time'] = get_formatted_current_time()
        return Response(data=response_body, status=status.HTTP_200_OK)
