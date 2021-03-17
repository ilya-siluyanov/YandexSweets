import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.serializers import CourierSerializer


class Couriers(APIView):

    @staticmethod
    def get(request, c_id):
        try:
            courier_object = Courier.objects.get(pk=c_id)
        except Courier.DoesNotExist:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        courier_object_dict = CourierSerializer(courier_object).data
        return Response(data=json.dumps(courier_object_dict), status=status.HTTP_201_CREATED)

    @staticmethod
    def post(request):
        received_body = json.loads(request.data)
        courier_list = received_body['data']

        couriers_id = []
        invalid_couriers_id = []

        for courier in courier_list:
            courier_id = courier['courier_id']
            json_courier_id = {'id': courier_id}
            couriers_id.append(json_courier_id)
            try:
                existing_courier = Courier.objects.get(pk=courier_id)
                serializer = CourierSerializer(existing_courier, data=courier)
            except Courier.DoesNotExist:
                serializer = CourierSerializer(data=courier)
            except Exception:
                serializer = CourierSerializer(data=courier)
            if serializer.is_valid():
                serializer.save()
            else:
                invalid_couriers_id.append(json_courier_id)
        if len(invalid_couriers_id) > 0:
            validation_error_object = {
                'validation_error_object': {
                    'Couriers': invalid_couriers_id
                }
            }
            response_body = json.dumps(validation_error_object)
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            response_body = {
                'Couriers': couriers_id
            }
            response_body = json.dumps(response_body)
            response_status = status.HTTP_201_CREATED
        return Response(data=response_body, status=response_status)

    @staticmethod
    def patch(request, c_id):
        # TODO: implement
        return None
