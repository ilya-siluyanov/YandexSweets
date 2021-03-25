import json
from django.utils import timezone
from datetime import datetime as dt

from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.models.order import Order
from YandexSweets.models.pydantic import OrderComplete


class OrdersCompleteView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        req_body = request.data
        try:
            req_data = OrderComplete.parse_obj(req_body)
            courier = Courier.objects.get(pk=req_data.courier_id)
            order = courier.order_set.get(pk=req_data.order_id)
            if order.completed_time is None:
                order.set_completed(dt.strptime(req_data.complete_time, '%Y-%m-%dT%H:%M:%S.%fZ'))
                order.delivery_type = courier.courier_type
            order.save()
        except ValidationError as e:
            print(e.json())
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Courier.DoesNotExist as e:
            print(e.args)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'order_id': order.order_id}, status=status.HTTP_200_OK)
