import json
import os
from datetime import datetime
import copy
import random

import requests

from support.db.db_connection import DbConnect
from settings import db_connection_test1, PCR_URL_TEST1, BASE_DIR
import pytest
from support.Excel2Json import create_data_json_pcr_79
from support.schema import get_api_schema, validate

db = DbConnect(db_connection_test1)
data = create_data_json_pcr_79()
url = PCR_URL_TEST1 + 'schedulers'

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')
_json = {
    "name": "test",
    "taskId": 1,
    "sellerId": 3,
    "active": True,
    "scheduleType": "WEEKLY",
    "startDate": datetime.now().strftime('%d-%m-%Y'),
    "scheduleTime": "09:00",
    "settings": {
        "repeat_days": [
            0,
            1,
            2,
            3
        ]
    },
    "variables": {
        "template": "send_email_compare_price",
        "shop_ids": [
            39
        ],
        "category_ids": ["01-N001-12-02"],
        "subject": "test",
        "receivers": [
            "thu.nt3@teko.vn"
        ]
    }
}


class TestPCR79:
    ISSUE_KEY = 'PCR-79'
    FOLDER = "/QC/API/PCR-79: Scheduler create scheduler update"
    def settup_class(self):
        print('setup')
    def teardown_class(self):
        db.execute_query("delete from schedulers where name like '%test%';")

    def call_api(self, payload):
        response = requests.post(url=url, json=payload)
        return response

    def call_api_update(self, payload, id):
        response = requests.put(url=url + "/" + str(id), json=payload)
        return response

    def get_id_schedule(self):
        ids = db.get_one_data("select id from schedulers order by id desc;")
        return ids['id']

    @pytest.mark.parametrize('des, data, expect, code, ', data)
    def test_create(self, des, data, expect, code):
        f'''
        '{des}'
        :param data:
        :param expect:
        :param code:
        :return:
        '''
        _payload = data
        _payload['settings'] = json.loads(_payload.pop('settings'))
        _payload['variables'] = json.loads(_payload.pop('variables'))
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == expect
        assert result['code'] == code


    @pytest.mark.parametrize('des, data, expect, code, ', data)
    def test_update(self, des, data, expect, code):
        f'''
            '{des}'
            :param data:
            :param expect:
            :param code:
            :return:
            '''
        _payload = data
        id = self.get_id_schedule()
        print(id)
        print(json.dumps(_payload))
        # _payload['settings'] = json.loads(_payload.pop('settings'))
        # _payload['variables'] = json.loads(_payload.pop('variables'))
        print(json.dumps(_payload))
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == expect
        assert result['code'] == code

    def test_not_name(self):
        '''
        Kiểm tra response khi không có trường name
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['name']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'name': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_taskId(self):
        '''
        Kiểm tra response khi không có trường taskId
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['taskId']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'task_id': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_sellerId(self):
        '''
        Kiểm tra response khi không có trường sellerId
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['sellerId']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'seller_id': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_active(self):
        '''
        Kiểm tra response khi không có trường active
        Step by step:
        Expect: trả về kết success
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['active']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result['message'] == "{'active': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_repeat_day(self):
        '''
        Kiểm tra response khi không có trường repeat_day
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['settings']['repeat_days']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_repeat_day_missing_or_not_valid'
        assert result['message'] == "Repeat day is missing or not valid"

    def test_not_setting(self):
        '''
        Kiểm tra response khi không có trường setting
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['settings']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'settings': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_scheduleType(self):
        '''
        Kiểm tra response khi không có trường scheduleType
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['scheduleType']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_type': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_startDate(self):
        '''
        Kiểm tra response khi không có trường startDate
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['startDate']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'start_date': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_scheduleTime(self):
        '''
        Kiểm tra response khi không có trường scheduleTime
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['scheduleTime']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_time': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_template(self):
        '''
        Kiểm tra response khi không có trường template
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['variables']['template']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'template' is a required property"

    def test_not_shop_ids(self):
        '''
        Kiểm tra response khi không có trường shop_ids
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['variables']['shop_ids']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'shop_ids' is a required property"

    def test_not_subject(self):
        '''
        Kiểm tra response khi không có trường subject
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['variables']['subject']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'subject' is a required property"

    def test_not_receivers(self):
        '''
        Kiểm tra response khi không có trường receivers
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['variables']['receivers']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'receivers' is a required property"

    def test_not_category_ids(self):
        '''
        Kiểm tra response khi không có trường category_ids
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['variables']['category_ids']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_variables(self):
        '''
        Kiểm tra response khi không có trường variables
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        del _payload['variables']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'variables': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_startDate_not_exist(self):
        '''
        Kiểm tra response khi trường startDate không tồn tại
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['startDate'] = '2020-12-32'
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'start_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', code='invalid')]}"

    def test_startDate_null(self):
        '''
        Kiểm tra response khi trường startDate = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['startDate'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'start_date': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_startDate_space(self):
        '''
        Kiểm tra response khi trường startDate = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['startDate'] = ' '
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'start_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', code='invalid')]}"

    def test_startDate_not_datetime(self):
        '''
        Kiểm tra response khi trường startDate không đúng định dạng
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['startDate'] = 'sdfghjk'
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'start_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', code='invalid')]}"

    def test_null_name(self):
        '''
        Kiểm tra response khi có trường name = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['name'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'name': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_null_taskId(self):
        '''
        Kiểm tra response khi có trường taskId = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['taskId'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'task_id': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_null_sellerId(self):
        '''
        Kiểm tra response khi trường sellerId = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['sellerId'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'seller_id': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_null_active(self):
        '''
        Kiểm tra response khi có trường active = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['active'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'active': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_null_scheduleType(self):
        '''
        Kiểm tra response khi trường scheduleType = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['scheduleType'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_type': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_null_scheduleTime(self):
        '''
        Kiểm tra response khi trường scheduleTime = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(_json)
        _payload['scheduleTime'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_time': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_update_not_name(self):
        '''
        Kiểm tra response khi update không có trường name
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        del _payload['name']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'name': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_taskId(self):
        '''
        Kiểm tra response khi update không có trường taskId
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        del _payload['taskId']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'task_id': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_sellerId(self):
        '''
        Kiểm tra response khi update không có trường sellerId
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        del _payload['sellerId']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'seller_id': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_active(self):
        '''
        Kiểm tra response khi update không có trường active
        Step by step:
        Expect: trả về kết success
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        del _payload['active']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result['message'] == "{'active': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_repeat_day(self):
        '''
        Kiểm tra response khi update không có trường repeat_day
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        del _payload['settings']['repeat_days']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_repeat_day_missing_or_not_valid'
        assert result['message'] == "Repeat day is missing or not valid"

    def test_update_not_setting(self):
        '''
        Kiểm tra response khi update không có trường setting
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        del _payload['settings']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'settings': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_scheduleType(self):
        '''
        Kiểm tra response khi update không có trường scheduleType
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['scheduleType']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_type': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_startDate(self):
        '''
        Kiểm tra response khi update không có trường startDate
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['startDate']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'start_date': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_scheduleTime(self):
        '''
        Kiểm tra response khi update không có trường scheduleTime
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['scheduleTime']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_time': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_update_not_template(self):
        '''
        Kiểm tra response khi update không có trường template
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['variables']['template']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'template' is a required property"

    def test_update_not_shop_ids(self):
        '''
        Kiểm tra response khi update không có trường shop_ids
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['variables']['shop_ids']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'shop_ids' is a required property"

    def test_update_not_subject(self):
        '''
        Kiểm tra response khi update không có trường subject
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['variables']['subject']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'subject' is a required property"

    def test_update_not_receivers(self):
        '''
        Kiểm tra response khi update không có trường receivers
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['variables']['receivers']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_invalid_variable'
        assert result['message'] == "'receivers' is a required property"

    def test_update_not_category_ids(self):
        '''
        Kiểm tra response khi update không có trường category_ids
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['variables']['category_ids']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result['message'] == "'receivers' is a required property"

    def test_update_not_variables(self):
        '''
        Kiểm tra response khi update không có trường variables
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        del _payload['variables']
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'variables': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_startDate_not_exist(self):
        '''
        Kiểm tra response khi trường startDate không tồn tại
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        _payload['startDate'] = '2020-12-32'
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'start_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', code='invalid')]}"

    def test_startDate_null(self):
        '''
        Kiểm tra response khi trường startDate = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        _payload['startDate'] = None
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'start_date': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_startDate_space(self):
        '''
        Kiểm tra response khi trường startDate = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        _payload['startDate'] = ' '
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'start_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', code='invalid')]}"

    def test_startDate_not_datetime(self):
        '''
        Kiểm tra response khi trường startDate không đúng định dạng
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        _payload['startDate'] = 'sdfghjk'
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'start_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', code='invalid')]}"

    def test_update_null_name(self):
        '''
        Kiểm tra response khi update có trường name = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # _payload = data[0][1].copy()
        # print(json.dumps(_payload))
        # _payload['settings'] = json.loads(_payload.pop('settings'))
        # _payload['variables'] = json.loads(_payload.pop('variables'))
        _payload['name'] = None
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'name': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_update_null_taskId(self):
        '''
        Kiểm tra response khi update có trường taskId = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        # print(json.dumps(_payload))
        # _payload['settings'] = json.loads(_payload.pop('settings'))
        # _payload['variables'] = json.loads(_payload.pop('variables'))
        _payload['taskId'] = None
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'task_id': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_update_null_sellerId(self):
        '''
        Kiểm tra response khi update trường sellerId = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        _payload['sellerId'] = None
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'seller_id': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_update_null_active(self):
        '''
        Kiểm tra response khi update có trường active = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        _payload['active'] = None
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'active': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_update_null_scheduleType(self):
        '''
        Kiểm tra response khi update trường scheduleType = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        _payload['scheduleType'] = None
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_type': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_update_null_scheduleTime(self):
        '''
        Kiểm tra response khi update trường scheduleTime = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        id = self.get_id_schedule()
        _payload = copy.deepcopy(_json)
        _payload['scheduleTime'] = None
        response = self.call_api_update(payload=_payload, id=id)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'schedule_time': [ErrorDetail(string='This field may not be null.', code='null')]}"
