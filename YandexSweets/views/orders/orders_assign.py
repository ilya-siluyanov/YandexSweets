from django.utils import timezone as dt
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.models.delivery_pack import DeliveryPack
from YandexSweets.models.order import Order
from YandexSweets.models.pydantic import OrdersAssign
from YandexSweets.time_utils import get_formatted_time


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

        response_body = {
            'orders': []
        }

        # there is delivery which is not ended
        if len(courier.deliverypack_set.filter(delivery_ended=False).all()) > 0:
            current_delivery_pack = courier.deliverypack_set.filter(delivery_ended=False).get()
            for order in current_delivery_pack.orders().filter(delivery_time__isnull=True):
                response_body['orders'].append({'id': order.order_id})
            response_body['assign_time'] = get_formatted_time(current_delivery_pack.assign_time)
            return Response(data=response_body, status=status.HTTP_200_OK)

        current_time = dt.now()
        delivery_pack = DeliveryPack()
        courier.assign_pack(delivery_pack, current_time)

        orders = Order.objects.filter(delivery_pack__isnull=True)
        orders = orders.filter(region__in=courier.regions)
        orders = orders.filter(weight__lte=Courier.COURIER_MAX_WEIGHT[courier.courier_type])

        for order in orders:
            if order.is_inside_working_time(courier):
                delivery_pack.assign_order(order)
                response_body['orders'].append({'id': order.order_id})

        courier.save()
        if len(response_body['orders']) > 0:
            response_body['assign_time'] = get_formatted_time(current_time)
        return Response(data=response_body, status=status.HTTP_200_OK)
