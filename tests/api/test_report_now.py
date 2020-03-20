import copy
import json
import os

import pytest
import requests

from settings import PCR_URL_TEST1
from support.Excel2Json import create_data_json_pcr_99
from support.schema import get_api_schema, validate
from tests.api.test_get_detail_scheduler_report import SCHEMA_BASE_URL

url = PCR_URL_TEST1 + 'tasks/report'
data = create_data_json_pcr_99()


class TestPCR99:
    ISSUE_KEY = 'PCR-99'
    FOLDER = "/QC/API/PCR-99: Send report now"

    def call_api(self, payload):
        return requests.post(url=url, json=payload)

    @pytest.mark.parametrize('des, data, expect, code, ', data)
    def test_send_report_now(self, des, data, expect, code):
        f'''
        '{des}'
        :param data:
        :param expect:
        :param code:
        :return:
        '''

        _payload = data
        _payload['variables'] = json.loads(_payload.pop('variables'))
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == expect
        assert result['code'] == code
        if expect == 200:
            api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_send_report_now_success'))
            is_valid, message, error_path = validate(result, api_schema)
            assert is_valid, (error_path + ': ' + message)
        else:
            api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_send_report_now_fail'))
            is_valid, message, error_path = validate(result, api_schema)
            assert is_valid, (error_path + ': ' + message)

    def test_not_name(self):
        '''
        Kiểm tra response khi không có trường name
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
        del _payload['sellerId']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'seller_id': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_shop_ids(self):
        '''
        Kiểm tra response khi không có trường shop_ids
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
        del _payload['variables']
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'variables': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_null_name(self):
        '''
        Kiểm tra response khi có trường name = null
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
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
        _payload = copy.deepcopy(data[0][1])
        _payload['sellerId'] = None
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'seller_id': [ErrorDetail(string='This field may not be null.', code='null')]}"
