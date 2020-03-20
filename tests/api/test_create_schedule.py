import requests
from settings import PCR_URL_TEST1, db_connection_test1
from support.db.db_connection import DbConnect
from support.Excel2Json import create_data_json_pcr_39, create_data_json_pcr_39_2
from collections import OrderedDict
import pytest
import collections
from datetime import datetime, timedelta
import random
import json

db = DbConnect(db_connection_test1)
url = PCR_URL_TEST1 + 'task-schedules'
data = create_data_json_pcr_39()
data2 = create_data_json_pcr_39_2()


class TestPCR39:
    ISSUE_KEY = 'PCR-39'
    FOLDER = '/QC/API/Tạo lịch'

    # def setup_class(self):
    #     print('setup')
    #     time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #     for i in range(10):
    #         db.execute_query(
    #             f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt1_qc{i}', 'https://thunt1_qc{i}.vn', {random.choice([0, 1])}, {random.choice([0, 1])});")

    # def teardown_class(self):
    #     print('teardown')
    #     db.execute_query("delete from schedule_targets;")
    #     db.execute_query("delete from task_schedules;")
    #     # db.execute_query("delete from shops where name like 'thunt1_qc%';")

    def get_id_active(self):
        user = OrderedDict()
        id = []
        shop_list = db.get_all_data('select * from shops where activate = 1;')
        for i in range(len(shop_list)):
            id.append(shop_list[i]['id'])
        _json = {
            'shopIds': [random.choice(id)]
        }
        user['scheduleTargets'] = _json
        return user

    def get_id_inactive(self):
        user = OrderedDict()
        id = []
        shop_list = db.get_data_all('select * from shops where activate = 0;')
        for i in range(len(shop_list)):
            id.append(shop_list[i]['id'])
        _json = {
            'shopIds': [random.choice(id)]
        }
        user['scheduleTargets'] = _json
        return user

    def call_api(self, json):
        return requests.post(url=url, json=json)

    @pytest.mark.parametrize('data, expect, code, descrip', data)
    def test_(self, data, expect, code, descrip):
        f'''
        {descrip}
        :return:
        '''
        id = self.get_id_active()
        print(data)
        _payload = data.copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == expect
        assert result['code'] == code
        if code == 200:
            db.execute_query("delete from schedule_targets;")
            #     db.execute_query("delete from task_schedules;")
            db.execute_query(f"delete from shops where id = {id};")


    def test_crawlType_null(self):
        '''
        Kiểm tra response trả về khi crawlType null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[0])
        _payload = data2[0].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        _payload['crawlType'] = json.loads(_payload.pop('crawlType'))
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_not_crawlType(self):
        '''
        Kiểm tra response trả về khi không có trường crawlType
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[1])
        _payload = data2[1].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        del _payload['crawlType']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_scheduleName_null(self):
        '''
        Kiểm tra response trả về khi scheduleName null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[2])
        _payload = data2[2].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        _payload['scheduleName'] = json.loads(_payload.pop('scheduleName'))
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_not_scheduleName(self):
        '''
        Kiểm tra response trả về khi không có trường scheduleName
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[3])
        _payload = data2[3].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        del _payload['scheduleName']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_repeat_days_null(self):
        '''
        Kiểm tra response trả về khi repeat_days null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[4])
        _payload = data2[4].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # _payload['repeat_day'] = json.loads(_payload.pop('repeat_day'))
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_repeat_day_missing_or_not_valid'


    def test_not_repeat_days(self):
        '''
        Kiểm tra response trả về khi không có trường repeat_days
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[5])
        _payload = data2[5].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleSettings']['repeat_day']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_repeat_day_missing_or_not_valid'


    def test_scheduleType_null(self):
        '''
        Kiểm tra response trả về khi scheduleType null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[6])
        _payload = data2[6].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        _payload['scheduleType'] = json.loads(_payload.pop('scheduleType'))
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_not_scheduleType(self):
        '''
        Kiểm tra response trả về khi không có trường scheduleType
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[7])
        _payload = data2[7].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        del _payload['scheduleType']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_startDate_null(self):
        '''
        Kiểm tra response trả về khi startDate null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[8])
        _payload = data2[8].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        _payload.update({'startDate': None})
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_not_startDate(self):
        '''
        Kiểm tra response trả về khi không có trường startDate
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[9])
        _payload = data2[9].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        del _payload['startDate']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_scheduleTime_null(self):
        '''
        Kiểm tra response trả về khi scheduleTime null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[10])
        _payload = data2[10].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        _payload['scheduleTime'] = json.loads(_payload.pop('scheduleTime'))
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_not_scheduleTime(self):
        '''
        Kiểm tra response trả về khi không có trường scheduleTime
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[11])
        _payload = data2[11].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_startDate_not_datetime(self):
        '''
        Kiểm tra response trả về khi trường startDate là string
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[12])
        _payload = data2[12].copy()
        _payload.update(id)
        _payload.update({'startDate': 'poiuyt'})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_startDate_wrong_format(self):
        '''
        Kiểm tra response trả về khi trường startDate sai format yyyy-mm-dd
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[13])
        _payload = data2[13].copy()
        _payload.update(id)
        _payload.update({'startDate': '11/12/2019'})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_startDate_is_past(self):
        '''
        Kiểm tra response trả về khi trường startDate là quá khứ
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[13])
        _payload = data2[13].copy()
        _payload.update(id)
        _payload.update({'startDate': '2019-11-11'})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_date_greater_or_equal'


    def test_startDate_is_future(self):
        '''
        Kiểm tra response trả về khi trường startDate là tương lai
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        id = self.get_id_active()
        print(data2[13])
        _payload = data2[13].copy()
        _payload.update(id)
        _payload.update({'startDate': time})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'


    def test_startDate_not_exist(self):
        '''
        Kiểm tra response trả về khi trường startDate không tồn tại
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[14])
        _payload = data2[14].copy()
        _payload.update(id)
        _payload.update({'startDate': '2020-02-30'})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_scheduleSetting_not_object(self):
        '''
        Kiểm tra response trả về khi trường scheduleSetting không phải object
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[15])
        _payload = data2[15].copy()
        _payload.update(id)
        # _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'invalid_json'


    def test_activate_not_true_false(self):
        '''
        Kiểm tra response trả về khi trường activate không phải true/false
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[16])
        _payload = data2[16].copy()
        _payload.update(id)
        _payload.update({'activate': 'fghjk'})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_activate_null(self):
        '''
        Kiểm tra response trả về khi trường activate null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[17])
        _payload = data2[17].copy()
        _payload.update(id)
        _payload.update({'activate': None})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_activate_space(self):
        '''
        Kiểm tra response trả về khi trường activate = space
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active()
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload.update({'activate': ''})
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_shopIds_have_element_not_int(self):
        '''
        Kiểm tra response trả về khi trường shopIds có phần tử không phải int
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = {
            "scheduleTargets": {"shopIds": ['tyuiop']}
        }
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_shopIds_have_element_null(self):
        '''
        Kiểm tra response trả về khi trường shopIds có phần tử null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = {
            "scheduleTargets": {"shopIds": [None]}
        }
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_shopIds_have_element_inactive(self):
        '''
        Kiểm tra response trả về khi trường shopIds có phần tử inactive
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_inactive()
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'task_schedule_some_invalid_shop'


    def test_shopIds_null(self):
        '''
        Kiểm tra response trả về khi trường shopIds null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = {
            "scheduleTargets": {"shopIds": None}
        }
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_not_shopIds(self):
        '''
        Kiểm tra response trả về khi không có trường shopIds
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = {
            "scheduleTargets": {"categoryIds": []}
        }
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_scheduleTargets_not_object(self):
        '''
        Kiểm tra response trả về khi scheduleTargets không phải object
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = {
            "scheduleTargets": 'qưertyuio'
        }
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_scheduleTargets_null(self):
        '''
        Kiểm tra response trả về khi scheduleTargets null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = {
            "scheduleTargets": None
        }
        print(data2[18])
        _payload = data2[18].copy()
        _payload.update(id)
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_not_scheduleTargets(self):
        '''
        Kiểm tra response trả về khi không có trường scheduleTargets
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        print(data2[18])
        _payload = data2[18].copy()
        _payload['scheduleSettings'] = json.loads(_payload.pop('scheduleSettings'))
        # del _payload['scheduleTime']
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
