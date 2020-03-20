import json
import os

import requests

from support.db.db_connection import DbConnect
from settings import db_connection_test1, PCR_URL_TEST1, BASE_DIR
import pytest
from support.Excel2Json import create_data_json_pcr_53, create_data_json_pcr_53_2
from support.schema import get_api_schema, validate

db = DbConnect(db_connection_test1)
data = create_data_json_pcr_53()
data1 = create_data_json_pcr_53_2()
url = PCR_URL_TEST1 + 'product-suggestions'

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')


class TestPCR53:
    ISSUE_KEY = 'PCR-53'
    FOLDER = "/QC/API/POST Product Suggesstions"

    def call_api(self, payload):
        response = requests.post(url=url, json=payload)
        return response

    @pytest.mark.parametrize('des, data, expect, code, ', data)
    def test_(self, des, data, expect, code):
        f'''
        '{des}'
        :param data:
        :param expect:
        :param code:
        :return:
        '''
        _payload = data

        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == expect
        assert result['code'] == code

    def test_not_pageSize(self):
        '''
        Kiểm tra response khi không có trường pageSize
        Step by step:
        Expect: trả về kết quả default pageSize = 10
        :return:
        '''
        _payload = data1[0].copy()
        # print((_payload.pop('shopIds')))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['pageSize']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['pageSize'] == 10

    def test_not_page(self):
        '''
        Kiểm tra response khi không có trường page
        Step by step:
        Expect: trả về kết quả default currentPage = 1
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['page']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['currentPage'] == 1

    def test_not_state(self):
        '''
        Kiểm tra response khi không có trường state
        Step by step:
        Expect: trả về kết quả lỗi
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['state']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'state': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_name(self):
        '''
        Kiểm tra response khi không có trường name
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['name']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result['message'] == "{'state': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_brand(self):
        '''
        Kiểm tra response khi không có trường brand
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['brand']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_shopIds_have_cat(self):
        '''
        Kiểm tra response khi không có trường shopIds có trường categoryIds
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['shopIds']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_categoryIds(self):
        '''
        Kiểm tra response khi không có trường categoryIds
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['categoryIds']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_orderBy(self):
        '''
        Kiểm tra response khi không có trường orderBy
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['orderBy']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_skus(self):
        '''
        Kiểm tra response khi không có trường skus
        Step by step:
        Expect: trả về kết quả success
        :return:
        '''
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['skus']
        print(json.dumps(_payload))
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
        _payload = data1[0].copy()
        # print(json.dumps(_payload))
        _payload['shopIds'] = json.loads(_payload.pop('shopIds'))
        _payload['categoryIds'] = json.loads(_payload.pop('categoryIds'))
        _payload['skus'] = json.loads(_payload.pop('skus'))
        del _payload['sellerId']
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_response_success(self):
        '''
        Kiểm tra cấu trúc response trả về khi success
        :return:
        '''
        data = {"state": "PENDING"}
        response = requests.post(url=url, json=data)
        _json = response.json()
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        assert isinstance(_json, dict)
        assert _json['code'] == 'success'

        api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_suggestion_success'))
        is_valid, message, error_path = validate(_json, api_schema)
        assert is_valid, (error_path + ': ' + message)

    def test_response_error(self):
        '''
        Kiểm tra cấu trúc response trả về khi lỗi
        :return:
        '''
        data = {"state": "PENDINGs"}
        response = requests.post(url=url, json=data)
        _json = response.json()

        api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_suggestion_error'))
        is_valid, message, error_path = validate(_json, api_schema)
        assert is_valid, (error_path + ': ' + message)
