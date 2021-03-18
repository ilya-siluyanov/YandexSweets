import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models.order import Order
from YandexSweets.serializers.order_serializer import OrderSerializer
from YandexSweets.time_utils import get_start_end_periods


class Orders(APIView):

    @staticmethod
    def post(request):
        received_body = json.loads(request.data)
        orders_list = received_body['data']
        order_ids = [{'id': order['order_id']} for order in orders_list]
        invalid_order_ids = []
        for order in orders_list:
            order_id = order['order_id']
            if 'delivery_hours' not in order.keys():
                order['delivery_hours'] = []
            for index, period in enumerate(order['delivery_hours']):
                order['delivery_hours'][index] = get_start_end_periods(period)
            try:
                existing_order = Order.objects.get(pk=order_id)
                serializer = OrderSerializer(existing_order, data=order)
            except Order.DoesNotExist as e:
                print(e.args)
                serializer = OrderSerializer(data=order)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
                invalid_order_ids.append({'id': order['order_id']})

        if len(invalid_order_ids) > 0:
            response_body = {
                'validation_error': {
                    'orders': invalid_order_ids
                }
            }
            response_body = json.dumps(response_body)
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            response_body = {
                'orders': order_ids
            }
            response_body = json.dumps(response_body)
            response_status = status.HTTP_201_CREATED
        return Response(data=response_body, status=response_status)
