import json
import os
from datetime import datetime, timedelta
import copy
import random

import requests
from any_case import converts_keys

from support.db.db_connection import DbConnect
from settings import db_connection_test1, PCR_URL_TEST1, BASE_DIR
import pytest
from support.Excel2Json import create_data_json_pcr_79
from support.schema import get_api_schema, validate

db = DbConnect(db_connection_test1)
data = create_data_json_pcr_79()
url = PCR_URL_TEST1 + 'schedulers/'

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')

class TestPCR78:
    ISSUE_KEY = 'PCR-90'
    FOLDER = "/QC/API/PCR-90: Scheduler detail"

    def call_api(self, id):
        response = requests.get(url=url+str(id))
        return response

    def get_id_schedule(self):
        ids = db.get_all_data("select id from schedulers ;")
        list_ids=[ids[i]['id'] for i in range(len(ids))]
        return random.choice(list_ids)
    def test_get_detail(self):
        '''
        Kiểm tra detail của lịch
        Step by step:
        Expect: Trả về đúng các trường và giá trị
        :return:
        '''
        id=self.get_id_schedule()
        response = self.call_api(id=id)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        print(json.dumps(result))
        data=db.get_one_data(f"select * from schedulers where id = '{id}';")
        hours, remainder = divmod(timedelta.total_seconds(data['schedule_time']), 3600)
        minutes, seconds = divmod(remainder, 60)
        assert result['result']['name'] == data['name']
        assert result['result']['startDate'] == datetime.strftime(data['start_date'], '%Y-%m-%d')
        assert result['result']['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        state = True if data['active'] == 1 else False
        assert result['result']['active'] == state
        assert result['result']['sellerId'] == data['seller_id']
        assert result['result']['scheduleType'] == data['schedule_type']
        assert result['result']['settings'] == converts_keys(data=json.loads(data['settings']), case='camel')
        assert result['result']['variables'] == converts_keys(data=json.loads(data['variables']), case='camel')
        assert result['result']['task'] == data['task_id']

    def test_id_null(self):
        '''
        Kiểm tra response trả về khi schedule_id = null
        Step by step:
        status_code = 404
        :return:
        '''
        response = requests.get(url=url)
        assert response.status_code == 404

    def test_id_not_exist(self):
        '''
        Kiểm tra response trả về khi schedule_id không tồn tại
        Step by step:
        status_code = 404
        :return:
        '''
        response = requests.get(url=url + str(0))
        result = response.json()
        assert response.status_code == 404
        assert result['code'] == 'record_does_not_exist'



