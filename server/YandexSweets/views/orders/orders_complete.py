import json
from django.utils import dateparse as dp

from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.models.delivery_pack import DeliveryPack
from YandexSweets.models.order import Order
from YandexSweets.models.pydantic import OrderComplete


class OrdersCompleteView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        req_body = request.data
        try:
            req_data = OrderComplete.parse_obj(req_body)
            courier = Courier.objects.get(pk=req_data.courier_id)  # type: Courier
            delivery_pack = courier.deliverypack_set.filter(delivery_ended=False).get()  # type: DeliveryPack
            order = delivery_pack.orders().get(pk=req_data.order_id)  # type: Order

            if order.delivery_time is None:
                delivery_time = (
                        dp.parse_datetime(req_data.complete_time) - delivery_pack.last_complete_time)
                order.set_completed(delivery_time.seconds)
            order.save()

            all_orders_complete = True
            for assigned_order in delivery_pack.orders():
                if assigned_order.delivery_time is None:
                    all_orders_complete = False
                    break
            if all_orders_complete:
                delivery_pack.delivery_ended = True
            delivery_pack.save()
        except ValidationError as e:
            print(e.json())
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except (Courier.DoesNotExist, Order.DoesNotExist, DeliveryPack.DoesNotExist, TypeError) as e:
            print(e.args)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'order_id': order.order_id}, status=status.HTTP_200_OK)
