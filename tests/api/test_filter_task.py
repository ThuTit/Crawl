import json
import os

import pytest
import requests

from settings import PCR_URL_TEST1, BASE_DIR
from support.Excel2Json import create_data_json_pcr_84
from support.schema import get_api_schema, validate

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')
url = PCR_URL_TEST1 + 'tasks'
data = create_data_json_pcr_84()


class TestPCR84:
    ISSUE_KEY = 'PCR-84'
    FOLDER = "/QC/API/PCR-84: Filter task"

    def call_api(self, params):
        return requests.get(url=url, params=params)

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
        response = self.call_api(params=_payload)
        print(response.url)
        result = response.json()
        print(json.dumps(result))
        assert response.status_code == expect
        assert result['code'] == code
        if expect == 200:
            api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_filter_task_success'))
            is_valid, message, error_path = validate(result, api_schema)
            assert is_valid, (error_path + ': ' + message)
        else:
            api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_filter_task_fail'))
            is_valid, message, error_path = validate(result, api_schema)
            assert is_valid, (error_path + ': ' + message)

    def test_type_null(self):
        '''
        Kiểm tra response khi type = null
        Step by step:
        Expect: status_code = 200
        :return:
        '''
        params = {
            'type': None,
            'active': True
        }
        response = self.call_api(params=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_active_null(self):
        '''
        Kiểm tra response khi active = null
        Step by step:
        Expect: status_code = 200
        :return:
        '''
        params = {
            'active': None,
            'type': 'reporting'
        }
        response = self.call_api(params=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_type(self):
        '''
        Kiểm tra response khi không có trường type
        Step by step:
        Expect: status_code = 200
        :return:
        '''
        params = {
            # 'type': None,
            'active': True
        }
        response = self.call_api(params=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_active(self):
        '''
        Kiểm tra response khi không có trường active
        Step by step:
        Expect: status_code = 200
        :return:
        '''
        params = {
            'type': 'reporting'
            # 'active': True
        }
        response = self.call_api(params=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
