import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.serializers import CourierSerializer
from YandexSweets.time_utils import *
from ... import serializers


class CouriersView(APIView):

    @staticmethod
    def get(request, c_id):
        try:
            courier_object = Courier.objects.get(pk=c_id)
        except Courier.DoesNotExist:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        courier_object_dict = CourierSerializer(courier_object).data
        for ind, period in enumerate(courier_object_dict['working_hours']):
            courier_object_dict['working_hours'][ind] = parse_time(period[0]) \
                                                        + '-' \
                                                        + parse_time(period[1])
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
            if 'working_hours' not in courier.keys():
                courier['working_hours'] = []
            periods_c = courier['working_hours']
            periods = []
            for period in periods_c:
                periods += [get_start_end_periods(period)]
            courier['working_hours'] = periods
            try:
                existing_courier = Courier.objects.get(pk=courier_id)
                serializer = CourierSerializer(existing_courier, data=courier, partial=True)
            except Courier.DoesNotExist:
                serializer = CourierSerializer(data=courier)
            except Exception:
                serializer = CourierSerializer(data=courier)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
                invalid_couriers_id.append(json_courier_id)
        if len(invalid_couriers_id) > 0:
            validation_error_object = {
                'validation_error_object': {
                    'couriers': invalid_couriers_id
                }
            }
            response_body = json.dumps(validation_error_object)
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            response_body = {
                'couriers': couriers_id
            }
            response_body = json.dumps(response_body)
            response_status = status.HTTP_201_CREATED
        return Response(data=response_body, status=response_status)

    @staticmethod
    def patch(request, c_id):
        req_body = json.loads(request.data)

        for field in req_body.keys():
            if req_body[field] is None:
                res_body = {
                    'description':
                        'There is no value for field ' + field
                }
                res_body = json.dumps(res_body)
                return Response(data=res_body, status=status.HTTP_400_BAD_REQUEST)

        try:
            courier = Courier.objects.get(pk=c_id)
        except Courier.DoesNotExist as e:
            res_body = {
                'description': 'There is no such a courier with id=' + str(c_id)
            }
            res_body = json.dumps(res_body)
            return Response(data=res_body, status=status.HTTP_400_BAD_REQUEST)
        for field in req_body.keys():
            courier[field] = req_body[field]
        courier.save()

        for order in courier.order_set.all():
            if not courier.is_inside_working_time(order):
                courier.make_order_free(order)

        for order in courier.order_set.all():
            if order.weight > Courier.COURIER_MAX_WEIGHT[courier.courier_type]:
                courier.make_order_free(order)

        for order in courier.order_set.all():
            if order.region not in courier.regions:
                courier.make_order_free(order)

        res_body = serializers.CourierSerializer(Courier.objects.get(pk=c_id)).data
        return Response(data=res_body, status=status.HTTP_200_OK)
