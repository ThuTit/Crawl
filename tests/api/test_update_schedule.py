import requests
from settings import PCR_URL_SHOP
from support.db.db_connection import DbConnectMysql
from support.Excel2Json import create_data_json_pcr_39, create_data_json_pcr_39_2
from collections import OrderedDict
import pytest
from datetime import datetime, timedelta
import random
import json

db = DbConnectMysql()
url_create = PCR_URL_SHOP + 'task-schedules'
url_update = PCR_URL_SHOP + 'task-schedules/'
data = create_data_json_pcr_39()
data2 = create_data_json_pcr_39_2()


class TestPCR47:
    ISSUE_KEY = 'PCR-47'
    FOLDER = '/QC/API/Update lịch'

    def get_id_active(self):
        user = OrderedDict()
        id = []
        shop_list = db.get_data_all('select * from shops where activate = 1;')
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
        shop_list = db.get_data_all('select * from task_schedules;')
        id = [shop_list[i]['id'] for i in range(len(shop_list))]
        return requests.put(url=url_update + str(random.choice(id)), json=json)

    def get_id_active_patch(self):
        shop_list = db.get_data_all('select * from task_schedules where activate = 1;')
        id = [shop_list[i]['id'] for i in range(len(shop_list))]
        return random.choice(id)

    def get_id_inactive_patch(self):
        shop_list = db.get_data_all('select * from task_schedules where activate = 0;')
        id = [shop_list[i]['id'] for i in range(len(shop_list))]
        return random.choice(id)

    # def setup_class(self):
    #     print('setup')
    #     time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #     for i in range(10):
    #         db.execute_query(
    #             f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt2_qc{i}', 'https://thunt2_qc{i}.vn', {random.choice([0, 1])}, {random.choice([0, 1])});")
    #     shop_list = db.get_data_all('select * from shops where activate = 1;')
    #     id = [shop_list[i]['id'] for i in range(len(shop_list))]
    #     for j in range(10):
    #         json1 = {
    #             "crawlType": "CRAWL_CATEGORY",
    #             "scheduleName": "test_valid",
    #             "scheduleSettings": {"repeat_days": [0, 1, 2, 3]},
    #             "scheduleType": "WEEKLY",
    #             "startDate": datetime.now().strftime('%Y-%m-%d'),
    #             "scheduleTime": "09:00",
    #             "activate": True,
    #             "scheduleTargets": {
    #                 "shopIds": [
    #                     random.choice(id)
    #                 ]
    #             }
    #
    #         }
    #         json2 = {
    #             "crawlType": "CRAWL_CATEGORY",
    #             "scheduleName": "test_valid",
    #             "scheduleSettings": {"repeat_days": [0, 1, 2, 3]},
    #             "scheduleType": "WEEKLY",
    #             "startDate": datetime.now().strftime('%Y-%m-%d'),
    #             "scheduleTime": "09:00",
    #             "activate": True,
    #             "scheduleTargets": {
    #                 "shopIds": [
    #                     random.choice(id)
    #                 ]
    #             }
    #
    #         }
    #
    #         requests.post(url=url_create, json=json1)
    #         requests.post(url=url_create, json=json2)
    #
    # def teardown_class(self):
    #     print('teardown')
    #     db.execute_query("delete from schedule_targets;")
    #     db.execute_query("delete from task_schedules where schedule_name like '%test%';")
    #     db.execute_query("delete from shops where name like 'thunt2_qc%';")

    def test_active(self):
        '''
        Kiểm tra update trạng thái của record khi đang ở trạng thái active
        Step by step:
        Hiển thị thông báo thành công
        :return:
        '''
        id = self.get_id_active_patch()
        params = {
            "scheduleName": "test_valid",
            "activate": False,
        }
        response = requests.patch(url=url_update + str(id), data=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_inactive(self):
        '''
        Kiểm tra update trạng thái của record khi đang ở trạng thái inactive
        Step by step:
        Hiển thị thông báo thành công
        :return:
        '''
        id = self.get_id_inactive_patch()
        params = {
            "scheduleName": "test_valid",
            "activate": True,
        }
        response = requests.patch(url=url_update + str(id), data=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_activate_different_true_false(self):
        '''
        Kiểm tra update trạng thái của record khi activate khác true/false
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active_patch()
        params = {
            "scheduleName": "test_valid",
            "activate": 'rtyui',
        }
        response = requests.patch(url=url_update + str(id), data=params)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_not_activate(self):
        '''
        Kiểm tra update trạng thái của record khi không có trường activate
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active_patch()
        params = {
            "scheduleName": "test_valid"
        }
        response = requests.patch(url=url_update + str(id), data=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_scheduleName(self):
        '''
        Kiểm tra update trạng thái của record khi không có trường scheduleName
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active_patch()
        params = {
            "activate": True,
        }
        response = requests.patch(url=url_update + str(id), data=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_data(self):
        '''
        Kiểm tra update trạng thái của record khi payload = null
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active_patch()
        url = url_update + str(id)
        response = requests.patch(url=url)
        assert response.status_code == 200

    def test_data_rong(self):
        '''
        Kiểm tra update trạng thái của record khi payload = {}
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        id = self.get_id_active_patch()
        params = {
        }
        response = requests.patch(url=url_update + str(id), data=params)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_not_id(self):
        '''
        Kiểm tra update trạng thái của record khi không có trường scheduleName
        Step by step:
        Hiển thị thông báo lỗi
        :return:
        '''
        params = {
            "scheduleName": "test_valid",
            "activate": True
        }
        response = requests.patch(url=url_update, data=params)
        assert response.status_code == 404

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
        # _payload['scheduleTargets'] = json.loads(_payload.pop('scheduleTargets'))
        print(json.dumps(_payload))
        response = self.call_api(json=_payload)
        result = response.json()
        assert response.status_code == expect
        assert result['code'] == code


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
