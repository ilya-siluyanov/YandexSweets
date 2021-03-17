import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models.order import Order
from YandexSweets.serializers.order_serializer import OrderSerializer
from YandexSweets.views.time_utils import get_start_end_periods


class Orders(APIView):

    @staticmethod
    def post(request):
        received_body = json.loads(request.data)
        orders_list = received_body['data']
        orders_id = []
        invalid_orders_id = []
        for order in orders_list:
            order_id = order['order_id']
            id_entity_json = {'id': order_id}
            orders_id.append(id_entity_json)
            if 'delivery_hours' not in order.keys():
                order['delivery_hours'] = []
            periods_c = order['delivery_hours']
            periods = []
            for period in periods_c:
                periods += [get_start_end_periods(period)]
            order['delivery_hours'] = periods
            try:
                existing_order = Order.objects.get(pk=order_id)
                serializer = OrderSerializer(existing_order, data=order)
            except Order.DoesNotExist:
                serializer = OrderSerializer(data=order)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
                invalid_orders_id.append(id_entity_json)

        if len(invalid_orders_id) > 0:
            response_body = {
                "validation_error": {
                    "orders": invalid_orders_id
                }
            }
            response_body = json.dumps(response_body)
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            response_body = {
                "orders": orders_id
            }
            response_body = json.dumps(response_body)
            response_status = status.HTTP_201_CREATED
        return Response(data=response_body, status=response_status)
