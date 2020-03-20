import json
import os
from datetime import datetime
import copy
import random

import requests

from support.db.db_connection import DbConnect
from settings import db_connection_test1, PCR_URL_TEST1, BASE_DIR
import pytest
from support.Excel2Json import create_data_json_pcr_93
from support.schema import get_api_schema, validate

db = DbConnect(db_connection_test1)
data = create_data_json_pcr_93()
url = PCR_URL_TEST1 + 'products/brand'

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')


class TestPCR93:
    ISSUE_KEY = 'PCR-93'
    FOLDER = "/QC/API/PCR-93: Get list brand of product"
    # def settup_class(self):
    #     print('setup')
    # def teardown_class(self):
    #     db.execute_query("delete from schedulers where name like '%test%';")

    def call_api(self, payload):
        response = requests.get(url=url, params=payload)
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
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == expect
        assert result['code'] == code

    def test_so_luong_brand(self):
        '''
        Kiểm tra số lượng brand trả về
        Step by step:
        Expect: Bằng với số record khi thực hiện query select distinct brand from crawled_products where shop_id = 39 and brand is not null order by brand asc;
        :return:
        '''
        _payload = {"pageSize": 15, "page": 1, "shopId": 39}
        print(json.dumps(_payload))
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        record = db.get_all_data("select distinct brand from crawled_products where shop_id = 39 and brand is not null order by brand asc;")
        # print(data)
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['totalItems'] == len(record)

    def test_pageSize_null(self):
        '''
        Kiểm tra response trả về khi pageSize = null
        Step by step:
        Expect: Trả về success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        _payload['pageSize'] = None
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['pageSize'] == 10

    def test_page_null(self):
        '''
        Kiểm tra response trả về khi page = null
        Step by step:
        Expect: Trả về success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        _payload['page'] = None
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['currentPage'] == 1

    def test_q_null(self):
        '''
        Kiểm tra response trả về khi q = null
        Step by step:
        Expect: Trả về success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        _payload['q'] = None
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
    def test_shopId_null(self):
        '''
        Kiểm tra response trả về khi shopId = null
        Step by step:
        Expect: Trả về bad_request
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        _payload['shopId'] = None
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'shopId': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_pageSize_not(self):
        '''
        Kiểm tra response trả về khi không có trường pageSize
        Step by step:
        Expect: Trả về success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        del _payload['pageSize']
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['pageSize'] == 10

    def test_page_not(self):
        '''
        Kiểm tra response trả về khi không có trường page
        Step by step:
        Expect: Trả về success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        del _payload['page']
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['currentPage'] == 1

    def test_q_not(self):
        '''
        Kiểm tra response trả về khi không có trường q
        Step by step:
        Expect: Trả về success
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        del _payload['q']
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_shopId_not(self):
        '''
        Kiểm tra response trả về khi không có trường shopId
        Step by step:
        Expect: Trả về bad_request
        :return:
        '''
        _payload = copy.deepcopy(data[0][1])
        print(_payload)
        del _payload['shopId']
        print(_payload)
        response = self.call_api(payload=_payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'shopId': [ErrorDetail(string='This field is required.', code='required')]}"
