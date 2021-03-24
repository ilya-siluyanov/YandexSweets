import json

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier
from YandexSweets.serializers import CourierSerializer


class CouriersView(APIView):
    C = {
        Courier.foot: 2,
        Courier.bike: 5,
        Courier.car: 9
    }

    @staticmethod
    def get(request: Request, c_id):
        try:
            courier = Courier.objects.get(pk=c_id)
        except Courier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        completed_orders = courier.order_set \
            .filter(courier_id=courier.courier_id) \
            .filter(completed_time__isnull=False)
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
        if t == -1:
            t = 60 * 60
        rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
        res_body = CourierSerializer(courier).data
        if len(completed_orders) > 0:
            res_body['rating'] = float('{:.2f}'.format(rating))
        res_body['earnings'] = earnings
        return Response(data=res_body, status=status.HTTP_200_OK)

    @staticmethod
    def post(request: Request):
        req_body = request.data
        if request.content_type != 'application/json':
            req_body = json.loads(request.data)
        courier_list = req_body['data']

        courier_ids = []
        invalid_courier_ids = []

        for courier in courier_list:
            courier_id = courier['courier_id']
            dict_courier_id = {'id': courier_id}
            courier_ids.append(dict_courier_id)

            try:
                Courier.objects.get(pk=courier_id)
                dict_courier_id['description'] = 'There is an existing courier with such id'
                invalid_courier_ids.append(dict_courier_id)
            except Courier.DoesNotExist:
                serializer = CourierSerializer(data=courier)
                if serializer.is_valid():
                    serializer.save()
                else:
                    for error in serializer.errors.items():
                        dict_courier_id[error[0]] = str(error[1][0])
                    invalid_courier_ids.append(dict_courier_id)

        if len(invalid_courier_ids) > 0:
            validation_error_object = {
                'validation_error': {
                    'couriers': invalid_courier_ids
                }
            }
            response_body = validation_error_object
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            response_body = {
                'couriers': courier_ids
            }
            response_body = response_body
            response_status = status.HTTP_201_CREATED
        return Response(data=response_body, status=response_status)

    @staticmethod
    def patch(request, c_id):
        req_body = request.data
        if request.content_type != 'application/json':
            req_body = json.loads(request.data)
        try:
            courier = Courier.objects.get(pk=c_id)
            serializer = CourierSerializer(courier, data=req_body, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValidationError(serializer.errors)
        except Courier.DoesNotExist as e:
            print(json.dumps(e, indent=2))
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            print(json.dumps(e.args, indent=2))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for order in courier.order_set.all():
            if not courier.is_inside_working_time(order):
                courier.make_order_free(order)

        for order in courier.order_set.all():
            if order.weight > Courier.COURIER_MAX_WEIGHT[courier.courier_type]:
                courier.make_order_free(order)

        for order in courier.order_set.all():
            if order.region not in courier.regions:
                courier.make_order_free(order)

        res_body = CourierSerializer(Courier.objects.get(pk=c_id)).data
        return Response(data=res_body, status=status.HTTP_200_OK)
