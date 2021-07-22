import json

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models.order import Order
from YandexSweets.serializers.order_serializer import OrderSerializer


class OrdersView(APIView):

    @staticmethod
    def post(request: Request) -> Response:
        req_body = request.data
        if request.content_type != 'application/json':
            req_body = json.loads(request.data)
        orders_list = req_body['data']
        order_ids = []
        invalid_order_ids = []
        correct_order_serializers = []
        for order in orders_list:
            order_id = order['order_id']
            dict_order_id = {'id': order_id}
            order_ids.append(dict_order_id)
            try:
                Order.objects.get(pk=order_id)
                dict_order_id['description'] = 'There is an existing order with such id'
                invalid_order_ids.append(dict_order_id)
            except Order.DoesNotExist:
                serializer = OrderSerializer(data=order)
                if serializer.is_valid():
                    correct_order_serializers.append(serializer)
                else:
                    for error in serializer.errors.items():
                        dict_order_id[error[0]] = str(error[1][0])
                    invalid_order_ids.append(dict_order_id)

        if len(invalid_order_ids) > 0:
            response_body = {
                'validation_error': {
                    'orders': invalid_order_ids
                }
            }
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            response_body = {
                'orders': order_ids
            }
            for order_serializer in correct_order_serializers:
                order_serializer.save()
            response_status = status.HTTP_201_CREATED
        return Response(data=response_body, status=response_status)
