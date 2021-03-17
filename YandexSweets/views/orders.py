import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models.order import Order
from YandexSweets.serializers.order_serializer import OrderSerializer


class Orders(APIView):
    def post(self, request):
        received_body = json.loads(request.data)
        orders_list = received_body['data']
        orders_id = []
        invalid_orders_id = []
        for order in orders_list:
            order_id = order['order_id']
            id_entity_json = {'id': order_id}
            orders_id.append(id_entity_json)
            try:
                existing_order = Order.objects.get(pk=order_id)
                serializer = OrderSerializer(existing_order, data=order)
            except Order.DoesNotExist:
                serializer = OrderSerializer(data=Order)
            if serializer.is_valid():
                serializer.save()
            else:
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
                "validation_error": {
                    "orders": invalid_orders_id
                }
            }
            response_body = json.dumps(response_body)
            response_status = status.HTTP_201_CREATED
        return Response(data=response_body, status=response_status)
