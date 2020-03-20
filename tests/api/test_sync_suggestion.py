import json
import os

import requests

from support.db.db_connection import DbConnect
from settings import db_connection_test1, PCR_URL_TEST1, BASE_DIR
import pytest
from support.Excel2Json import create_data_json_pcr_54, create_data_json_pcr_54_1
from support.schema import get_api_schema, validate

db = DbConnect(db_connection_test1)
data = create_data_json_pcr_54()
data1 = create_data_json_pcr_54_1()
url = PCR_URL_TEST1 + 'product-suggestions/sync'

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')
class TestPCR55:
    ISSUE_KEY = 'PCR-55'
    FOLDER = "/QC/API/Sync-PCR-55"
    def test_sync_type_all(self):
        '''
        Kiểm tra response khi sync_type = ALL
        Expect: success
        :return:
        '''
        param = {
            'sync_type': 'ALL'
        }
        response = requests.get(url=url, params=param)
        result= response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
    def test_sync_type_newest(self):
        '''
        Kiểm tra response khi sync_type = NEWEST
        Expect: success
        :return:
        '''
        param = {
            'sync_type': 'NEWEST'
        }
        response = requests.get(url=url, params=param)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
    def test_sync_type_khac_all_newest(self):
        '''
        Kiểm tra response khi sync_type khác newest/all
        Expect: báo lỗi
        :return:
        '''
        param = {
            'sync_type': 'ádfgh'
        }
        response = requests.get(url=url, params=param)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
    def test_not_sync_type(self):
        '''
        Kiểm tra response khi không có trường sync_type
        Expect: success, default = all
        :return:
        '''
        response = requests.get(url=url)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'