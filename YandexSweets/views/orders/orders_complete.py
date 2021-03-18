import json

from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime as dt
from YandexSweets.models import Courier
from YandexSweets.models.order import Order
from YandexSweets.models.pydantic import OrderComplete


class OrdersCompleteView(APIView):
    @staticmethod
    def post(request):
        try:
            req_data = OrderComplete.parse_raw(request.data)
            order = Order.objects.get(pk=req_data.order_id)
            courier = Courier.objects.get(pk=req_data.courier_id)
            if order.courier is None or order.courier_id != courier.courier_id:
                raise Exception('')
            order.set_completed(dt.strptime(req_data.complete_time, '%Y-%m-%dT%H:%M:%S.%fZ'))
        except Exception as e:
            return Response(data=e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=json.dumps({'order_id': order.order_id}), status=status.HTTP_200_OK)
