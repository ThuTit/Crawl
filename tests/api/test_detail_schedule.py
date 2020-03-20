import requests
from settings import PCR_URL_SHOP
from support.db.db_connection import DbConnectMysql
from support.Excel2Json import create_data_json_pcr_39, create_data_json_pcr_39_2
from any_case import converts_keys
from collections import OrderedDict
import pytest
from datetime import datetime, timedelta
import random
import json
import time

db = DbConnectMysql()
url_create = PCR_URL_SHOP + 'task-schedules'
url_detail = PCR_URL_SHOP + 'task-schedules/'
data = create_data_json_pcr_39()
data2 = create_data_json_pcr_39_2()


class TestPCR48:
    ISSUE_KEY = 'PCR-48'
    FOLDER = '/QC/API/Chi tiết lịch'

    def call_api(self):
        shop_list = db.get_data_all('select * from task_schedules;')
        id = [shop_list[i]['id'] for i in range(len(shop_list))]
        return requests.get(url=url_detail + str(random.choice(id)))

    def setup_class(self):
        print('setup')
        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(10):
            db.execute_query(
                f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt2_qc{i}', 'https://thunt2_qc{i}.vn', 1, {random.choice([0, 1])});")
        shop_list = db.get_data_all('select * from shops where activate = 1;')
        id = [shop_list[i]['id'] for i in range(len(shop_list))]
        for j in range(10):
            json = {
                "crawlType": "CRAWL_CATEGORY",
                "scheduleName": "test_valid",
                "scheduleSettings": {"repeat_days": [0, 1, 2, 3]},
                "scheduleType": "WEEKLY",
                "startDate": datetime.now().strftime('%Y-%m-%d'),
                "scheduleTime": "09:00",
                "activate": random.choice([True, False]),
                "scheduleTargets": {
                    "shopIds": [
                        random.choice(id)
                    ]
                }

            }
            requests.post(url=url_create, json=json)

    def teardown_class(self):
        print('teardown')
        db.execute_query("delete from schedule_targets;")
        db.execute_query("delete from task_schedules where schedule_name like '%test%';")
        db.execute_query("delete from shops where name like 'thunt2_qc%';")

    def test_response(self):
        '''
        Kiểm tra response trả về khi gọi api detail hợp lệ
        Step by step:
        Trả về thông tin đúng của lịch
        :return:
        '''

        response = self.call_api()
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        record1 = db.get_data_one(f"select * from task_schedules where id = {result['result']['id']};")
        hours, remainder = divmod(timedelta.total_seconds(record1['schedule_time']), 3600)
        minutes, seconds = divmod(remainder, 60)
        assert result['result']['crawlType'] == record1['crawl_type']
        assert result['result']['scheduleName'] == record1['schedule_name']
        assert result['result']['scheduleSettings'] == converts_keys(data=json.loads(record1['schedule_settings']),
                                                                     case='camel')
        assert result['result']['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        assert result['result']['scheduleType'] == record1['schedule_type']
        assert result['result']['state'] == record1['state']
        assert result['result']['startDate'] == datetime.strftime(record1['start_date'], '%Y-%m-%d')
        state = True if record1['activate'] == 1 else False
        assert result['result']['activate'] == state
        record2 = db.get_data_all(f"select * from schedule_targets where schedule_id = {result['result']['id']};")
        assert len(result['result']['scheduleTargets']['shops']) == len(record2)
        for i in range(len(record2)):
            info_shop = db.get_data_one(
                f"select * from shops where id = {result['result']['scheduleTargets']['shops'][i]['id']};")
            assert result['result']['scheduleTargets']['shops'][i]['name'] == info_shop['name']
            assert result['result']['scheduleTargets']['shops'][i]['domain'] == info_shop['domain']
            state_shop = True if info_shop['activate'] == 1 else False
            assert result['result']['scheduleTargets']['shops'][i]['activate'] == state_shop
            assert result['result']['scheduleTargets']['shops'][i]['activeInProductPrice'] == info_shop[
                'active_in_product_price']
            assert result['result']['scheduleTargets']['shops'][i]['createdAt'] == datetime.strftime(
                info_shop['created_at'] + timedelta(hours=7), '%Y-%m-%dT%H:%M:%S+07:00')
            assert result['result']['scheduleTargets']['shops'][i]['updatedAt'] == datetime.strftime(
                info_shop['updated_at'] + timedelta(hours=7), '%Y-%m-%dT%H:%M:%S+07:00')

    def test_id_null(self):
        '''
        Kiểm tra response trả về khi task_schedule_id = null
        Step by step:
        status_code = 404
        :return:
        '''
        response = requests.get(url=url_detail)
        assert response.status_code == 404

    def test_id_not_exist(self):
        '''
        Kiểm tra response trả về khi task_schedule_id không tồn tại
        Step by step:
        status_code = 404
        :return:
        '''
        response = requests.get(url=url_detail + str(0))
        result = response.json()
        assert response.status_code == 404
        assert result['code'] == 'record_does_not_exist'
