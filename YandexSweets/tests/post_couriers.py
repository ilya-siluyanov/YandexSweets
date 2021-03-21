import json
import os
from django.test import TestCase
from rest_framework.test import *

from YandexSweets.views import CouriersView
from YandexSweetsProject.settings import BASE_DIR


# noinspection PyMethodMayBeStatic
class PostCouriers(TestCase):
    def test_register_new_couriers(self):
        # TODO : if there is problem with field existing in model, there will be no messages about fields which
        #  should not be in request
        f = APIRequestFactory()
        test_files_dir = str(BASE_DIR) + '/YandexSweets/tests/test_files/couriers_test_data'
        # for file in os.listdir(test_files_dir):
        files = os.listdir(test_files_dir)
        files.sort()
        for file in files:
            couriers_data = json.loads(open(test_files_dir + '/' + file, mode='r').read())
            req_body = couriers_data['input']
            expect = couriers_data['expect']['fields_with_errors']
            if len(expect) == 0:
                print(file)
            request = f.post('/couriers', req_body, format='json')
            response = CouriersView.as_view()(request)
            res_body = response.data
            print(response.status_code, json.dumps(res_body, indent=2))
            if 'validation_error' in res_body.keys():
                res_body = res_body['validation_error']['couriers']
                for courier in res_body:
                    for field in courier.keys():
                        if field == 'id':
                            continue
                        if field == 'non_field_errors':
                            field = courier[field].split(': ')[1]
                        assert field in expect, 'There should be error with the field {},file={}'.format(field,
                                                                                                         file)
            else:
                assert len(expect) == 0, 'There should not be any errors, file={}'.format(file)
