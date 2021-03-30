import json

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from YandexSweets.models import Courier, Order
from YandexSweets.models.delivery_pack import DeliveryPack
from YandexSweets.serializers import CourierSerializer


class CouriersView(APIView):
    C = {
        Courier.foot: 2,
        Courier.bike: 5,
        Courier.car: 9
    }

    @staticmethod
    def get(request: Request, c_id: int) -> Response:
        try:
            courier = Courier.objects.get(pk=c_id)
        except Courier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        completed_delivery_packs = courier.deliverypack_set.filter(delivery_ended=True)
        delivery_time_and_times = {}  # dict{region : {'time': sum of time, 'times' : number of orders for the region]}
        earnings = 0
        for delivery_pack in completed_delivery_packs:
            for completed_order in delivery_pack.orders():  # type: Order
                if completed_order.region not in delivery_time_and_times:
                    delivery_time_and_times[completed_order.region] = {'time': 0, 'times': 0}
                delivery_time_and_times[completed_order.region][
                    'time'] += completed_order.delivery_time
                delivery_time_and_times[completed_order.region]['times'] += 1
            c = CouriersView.C[delivery_pack.delivery_type]
            earnings += 500 * c
        t = -1
        for region_info in delivery_time_and_times.items():
            region_info = region_info[1]
            td = region_info['time'] / region_info['times']
            if t == -1:
                t = td
            else:
                t = min(t, td)
        if t == -1:
            t = 60 * 60
        rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
        res_body = CourierSerializer(courier).data
        if len(completed_delivery_packs) > 0:
            res_body['rating'] = float('{:.2f}'.format(rating))
        res_body['earnings'] = earnings
        return Response(data=res_body, status=status.HTTP_200_OK)

    @staticmethod
    def post(request: Request) -> Response:
        req_body = request.data
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
    def patch(request: Request, c_id: int) -> Response:
        req_body = request.data
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

        delivery_pack = courier.deliverypack_set.filter(delivery_ended=False).get()  # type: DeliveryPack
        not_completed_orders = delivery_pack.order_set.filter(
            delivery_time__isnull=True)
        for order in not_completed_orders:
            if not order.is_inside_working_time(courier):
                delivery_pack.make_order_free(order)

        for order in not_completed_orders:
            if order.weight > Courier.COURIER_MAX_WEIGHT[courier.courier_type]:
                delivery_pack.make_order_free(order)

        for order in not_completed_orders:
            if order.region not in courier.regions:
                delivery_pack.make_order_free(order)
        if len(delivery_pack.orders()) == 0:
            delivery_pack.delete()
        res_body = CourierSerializer(Courier.objects.get(pk=c_id)).data
        return Response(data=res_body, status=status.HTTP_200_OK)
