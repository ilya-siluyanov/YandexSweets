import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.serializers import CourierSerializer
from YandexSweets.time_utils import *
from ... import serializers


class CouriersView(APIView):
    C = {
        Courier.foot: 2,
        Courier.bike: 5,
        Courier.car: 9
    }

    @staticmethod
    def get(request, c_id):
        try:
            courier = Courier.objects.get(pk=c_id)
        except Courier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        completed_orders = courier.order_set \
            .filter(courier_id=courier.courier_id) \
            .filter(completed_time__isnull=False) \
            .filter(region__in=courier.regions)
        delivery_time_and_times = {}
        earnings = 0
        for completed_order in completed_orders:
            pair = delivery_time_and_times[completed_order.region] \
                if completed_order.region in delivery_time_and_times.keys() else {}
            for key in ('time', 'times'):
                if key not in pair.keys():
                    pair[key] = 0
            pair['time'] += (completed_order.completed_time
                             - completed_order.assign_to_courier_time).seconds
            pair['times'] += 1
            delivery_time_and_times[completed_order.region] = pair
            c = CouriersView.C[completed_order.delivery_type]
            earnings += 500 * c
        t = -1
        for region_info in delivery_time_and_times.items():
            td = region_info[1]['time'] / region_info[1]['times']
            if t == -1:
                t = td
            else:
                t = min(t, td)
        rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
        res_body = serializers.CourierSerializer(courier).data
        res_body['rating'] = float('{:.2f}'.format(rating))
        res_body['earnings'] = earnings
        return Response(data=json.dumps(res_body), status=status.HTTP_200_OK)

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
            return Response(data=res_body, status=status.HTTP_404_NOT_FOUND)
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
