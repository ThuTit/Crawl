import json
import os
from datetime import datetime
import copy
import random

import requests

from support.db.db_connection import DbConnect
from settings import db_connection_test1, PCR_URL_TEST1, BASE_DIR
import pytest
from support.Excel2Json import create_data_json_pcr_78
from support.schema import get_api_schema, validate

db = DbConnect(db_connection_test1)
data = create_data_json_pcr_78()
url = PCR_URL_TEST1 + 'schedulers'

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')


class TestPCR78:
    ISSUE_KEY = 'PCR-78'
    FOLDER = "/QC/API/PCR-78: Scheduler list"

    def setup_class(self):
        for i in range(10):
            _json = {
                "name": "test" + str(i),
                "taskId": 1,
                "sellerId": 1,
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
            requests.post(url=url, json=_json)

    def teardown_class(self):
        db.execute_query("delete from schedulers where name like '%test%';")

    def call_api(self, payload):
        response = requests.get(url=url, params=payload)
        return response

    @pytest.mark.parametrize('des, data, expect, code, ', data)
    def test_get_list(self, des, data, expect, code):
        f'''
          '{des}'
          :param data:
          :param expect:
          :param code:
          :return:
          '''
        _payload = data
        # _payload['settings'] = json.loads(_payload.pop('settings'))
        # _payload['variables'] = json.loads(_payload.pop('variables'))
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        print(response.url)
        result = response.json()
        print(json.dumps(result))
        assert response.status_code == expect
        assert result['code'] == code
        if code == 200:
            api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_get_list_scheduler_success'))
            is_valid, message, error_path = validate(result, api_schema)
            assert is_valid, (error_path + ': ' + message)
        else:
            api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_get_list_scheduler_fail'))
            is_valid, message, error_path = validate(result, api_schema)
            assert is_valid, (error_path + ': ' + message)


    def test_not_pageSize(self):
        '''
        Kiểm tra response khi không có trường pageSize
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        del _payload['pageSize']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_page(self):
        '''
        Kiểm tra response khi không có trường page
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        del _payload['page']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_searchText(self):
        '''
        Kiểm tra response khi không có trường searchText
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        del _payload['searchText']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_active(self):
        '''
        Kiểm tra response khi không có trường active
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        del _payload['active']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_sellerId(self):
        '''
        Kiểm tra response khi không có trường sellerId
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        del _payload['sellerId']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_variables(self):
        '''
        Kiểm tra response khi không có trường variables
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        del _payload['variables']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
    def test_response_correct(self):
        '''
        Kiểm tra tính đúng đắn của response trả về
        Step by step:
        Expect: Trả về dữ liệu đúng
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        response = self.call_api(payload=_payload)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['totalItems'] == 10
