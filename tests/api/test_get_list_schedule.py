import requests
from any_case import converts_keys

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
# url_update = PCR_URL_SHOP + 'task-schedules/'
data = create_data_json_pcr_39()
data2 = create_data_json_pcr_39_2()


class TestPCR49:
    ISSUE_KEY = 'PCR-49'
    FOLDER = '/QC/API/Danh sách lịch'

    def call_api(self, pageSize, page, activate, orderBy, crawlType, shopIds):
        params = {
            'pageSize': pageSize,
            'page': page,
            'activate': activate,
            'orderBy': orderBy,
            'crawlType': crawlType,
            'shopIds': shopIds,
        }
        return requests.get(url=url_create, params=params)

    # def setup_class(self):
    #     print('setup')
    #     time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #     for i in range(10):
    #         db.execute_query(
    #             f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt2_qc{i}', 'https://thunt2_qc{i}.vn', 1, {random.choice([0, 1])});")
    #     shop_list = db.get_data_all('select * from shops where activate = 1;')
    #     id = [shop_list[i]['id'] for i in range(len(shop_list))]
    #     for j in range(30):
    #         json = {
    #             "crawlType": random.choice(['CRAWL_CATEGORY', 'CRAWL_PRODUCT']),
    #             "scheduleName": "test_valid",
    #             "scheduleSettings": {"repeat_days": [0, 1, 2, 3]},
    #             "scheduleType": "WEEKLY",
    #             "startDate": datetime.now().strftime('%Y-%m-%d'),
    #             "scheduleTime": "09:00",
    #             "activate": random.choice([True, False]),
    #             "scheduleTargets": {
    #                 "shopIds": [
    #                     random.choice(id)
    #                 ]
    #             }
    #
    #         }
    #         requests.post(url=url_create, json=json)

    # def teardown_class(self):
    #     print('teardown')
    #     db.execute_query("delete from schedule_targets;")
    #     db.execute_query("delete from task_schedules where schedule_name like '%test%';")
    #     db.execute_query("delete from shops where name like 'thunt2_qc%';")
    def test_pageSize_null(self):
        '''
        Kiểm tra response trả về khi pageSize = null
        Step by step:
        Trả về 25 bản ghi
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        print(json.dumps(result))
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['pageSize'] == 10

    def test_pageSize_specific(self):
        '''
        Kiểm tra response trả về khi pageSize = giá trị cụ thể = n
        Step by step:
        Trả về n bản ghi
        :return:
        '''
        pageSize = 15
        page = None
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['pageSize'] == 15

    def test_pageSize_0(self):
        '''
        Kiểm tra response trả về khi pageSize = 0
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = 0
        page = None
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400

    def test_pageSize_am(self):
        '''
        Kiểm tra response trả về khi pageSize < 0
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = -10
        page = None
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400

    def test_pageSize_string(self):
        '''
        Kiểm tra response trả về khi pageSize = string
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = 'rtyuio'
        page = None
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400

    def test_page_null(self):
        '''
        Kiểm tra response trả về khi page = null
        Step by step:
        Trả về currentPage = 1
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        print(json.dumps(result))
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['pageSize'] == 10
        assert result['result']['currentPage'] == 1

    def test_page_specific(self):
        '''
        Kiểm tra response trả về khi page = giá trị cụ thể = n
        Step by step:
        Trả về currentPage = n
        :return:
        '''
        pageSize = None
        page = 2
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['currentPage'] == 2

    def test_page_0(self):
        '''
        Kiểm tra response trả về khi page = 0
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = None
        page = 0
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400

    def test_page_am(self):
        '''
        Kiểm tra response trả về khi page < 0
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = None
        page = -10
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400

    def test_page_string(self):
        '''
        Kiểm tra response trả về khi page = string
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = None
        page = 'rtui'
        activate = None
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400

    def test_activate_true(self):
        '''
        Kiểm tra response trả về khi activate = True
        Step by step:
        Trả về các bản ghi có hiệu lực
        :return:
        '''
        pageSize = None
        page = None
        activate = True
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        print(json.dumps(result))
        record = db.get_data_all('select * from task_schedules where activate = 1')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)
    def test_activate_false(self):
        '''
        Kiểm tra response trả về khi activate = False
        Step by step:
        Trả về các bản ghi vô hiệu
        :return:
        '''
        pageSize = None
        page = None
        activate = False
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        print(json.dumps(result))
        record = db.get_data_all('select * from task_schedules where activate = 0')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)

    def test_activate_khac_true_false(self):
        '''
        Kiểm tra response trả về khi activate khác True/False
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = None
        page = None
        activate = 'rtyuiop'
        orderBy = None
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400
    def test_orderBy_id_asc(self):
        '''
        Kiểm tra response trả về khi orderBy = id
        Step by step:
        Trả về danh sách lịch được sắp xếp theo id asc
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = 'id'
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        record = db.get_data_all('select * from task_schedules order by id asc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)

        for i in range(len(result['result']['results'])):
            hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            minutes, seconds = divmod(remainder, 60)
            assert result['result']['results'][i]['id'] == record[i]['id']
            assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type']
            assert result['result']['results'][i]['scheduleType'] == record[i]['schedule_type']
            assert result['result']['results'][i]['state'] == record[i]['state']
            assert result['result']['results'][i]['scheduleSettings'] == converts_keys(data=json.loads(record[i]['schedule_settings']),
                                                                     case='camel')
            assert result['result']['results'][i]['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            assert result['result']['results'][i]['startDate'] == datetime.strftime(record[i]['start_date'], '%Y-%m-%d')

    def test_orderBy_id_desc(self):
        '''
        Kiểm tra response trả về khi orderBy = -id
        Step by step:
        Trả về danh sách lịch được sắp xếp theo id desc
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = '-id'
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        record = db.get_data_all('select * from task_schedules order by id desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)

        for i in range(len(result['result']['results'])):
            hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            minutes, seconds = divmod(remainder, 60)
            assert result['result']['results'][i]['id'] == record[i]['id']
            assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type']
            assert result['result']['results'][i]['scheduleType'] == record[i]['schedule_type']
            assert result['result']['results'][i]['state'] == record[i]['state']
            assert result['result']['results'][i]['scheduleSettings'] == converts_keys(
                data=json.loads(record[i]['schedule_settings']),
                case='camel')
            assert result['result']['results'][i]['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours),
                                                                                                int(minutes),
                                                                                                int(seconds))
            assert result['result']['results'][i]['startDate'] == datetime.strftime(record[i]['start_date'], '%Y-%m-%d')

    def test_orderBy_schedule_name_asc(self):
        '''
        Kiểm tra response trả về khi orderBy = schedule_name
        Step by step:
        Trả về danh sách lịch được sắp xếp theo schedule_name asc
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = 'schedule_name'
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        record = db.get_data_all('select * from task_schedules order by schedule_name asc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)

        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            # assert result['result']['results'][i]['id'] == record[i]['id']
            # assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            # assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type']
            # assert result['result']['results'][i]['scheduleType'] == record[i]['schedule_type']
            # assert result['result']['results'][i]['state'] == record[i]['state']
            # assert result['result']['results'][i]['scheduleSettings'] == converts_keys(data=json.loads(record[i]['schedule_settings']),
            #                                                          case='camel')
            # assert result['result']['results'][i]['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            # assert result['result']['results'][i]['startDate'] == datetime.strftime(record[i]['start_date'], '%Y-%m-%d')

    def test_orderBy_schedule_name_desc(self):
        '''
        Kiểm tra response trả về khi orderBy = -schedule_name
        Step by step:
        Trả về danh sách lịch được sắp xếp theo schedule_name desc
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = '-schedule_name'
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        record = db.get_data_all('select * from task_schedules order by schedule_name desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)

        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            # assert result['result']['results'][i]['id'] == record[i]['id']
            assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
    def test_orderBy_invalid(self):
        '''
        Kiểm tra response trả về khi orderBy không hợp lệ
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = 'tyuio'
        crawType = None
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400
    def test_crawlType_CRAWL_CATEGORY(self):
        '''
        Kiểm tra response trả về khi crawlType = CRAWL_CATEGORY
        Step by step:
        Trả về các bản ghi có crawlType = CRAWL_CATEGORY
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = 'CRAWL_CATEGORY'
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        record = db.get_data_all("select * from task_schedules where crawl_type = 'CRAWL_CATEGORY';")
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)
        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            # assert result['result']['results'][i]['id'] == record[i]['id']
            # assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type'] == 'CRAWL_CATEGORY'
    def test_crawlType_CRAWL_PRODUCT(self):
        '''
        Kiểm tra response trả về khi crawlType = CRAWL_PRODUCT
        Step by step:
        Trả về các bản ghi có crawlType = CRAWL_PRODUCT
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = 'CRAWL_PRODUCT'
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        record = db.get_data_all("select * from task_schedules where crawl_type = 'CRAWL_PRODUCT';")
        assert response.status_code == 200
        assert len(result['result']['results']) == 10 if len(record) > 10 else len(record)
        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            # assert result['result']['results'][i]['id'] == record[i]['id']
            # assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type'] == 'CRAWL_PRODUCT'

    def test_crawlType_invalid(self):
        '''
        Kiểm tra response trả về khi crawlType không hợp lệ
        Step by step:
        Trả về status_code == 400
        :return:
        '''
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = 'ưertyui'
        shopIds = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        assert response.status_code == 400

    def test_shopIds_ton_tai_active(self):
        '''
        Kiểm tra response trả về khi shopIds tồn tại, đang active
        Step by step:
        Trả về bản ghi có shopIds là giá trị truyền vào params
        :return:
        '''
        data = db.get_data_all("select * from schedule_targets")
        shopIds = random.choice([data[i]['target_shop_id'] for i in range(len(data))])
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        assert response.status_code == 200
        for j in range(len(result['result']['results'])):
            assert shopIds in [result['result']['results'][j]['scheduleTargets']['shops'][t]['id'] for t in range(len(result['result']['results'][j]['scheduleTargets']['shops']))]
    def test_many_shopIds_ton_tai_active(self):
        '''
        Kiểm tra response trả về khi truyền nhiều shopIds tồn tại, đang active
        Step by step:
        Trả về bản ghi có shopIds là giá trị truyền vào params
        :return:
        '''
        shopIds_list=[]
        data = db.get_data_all("select * from schedule_targets")
        id = [data[i]['target_shop_id'] for i in range(len(data))]
        shopIds_list = list(set(id))
        shopIds = str(shopIds_list[0])+","+str(shopIds_list[1])+","+str(shopIds_list[2])
        print(shopIds)
        pageSize = 1000
        page = None
        activate = None
        orderBy = None
        crawType = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        assert response.status_code == 200

        result_schedule_id = [result['result']['results'][j]['id'] for j in range(len(result['result']['results']))]
        result_schedule_id_clone = list(set(result_schedule_id))
        assert len(result_schedule_id) == len(result_schedule_id_clone)
        for j in range(len(result['result']['results'])):
            assert shopIds_list[0] or shopIds_list[1] or shopIds_list[2] in [
                result['result']['results'][j]['scheduleTargets']['shops'][t]['id'] for t in
                range(len(result['result']['results'][j]['scheduleTargets']['shops']))]

    def test_shopIds_khong_ton_tai(self):
        '''
        Kiểm tra response trả về khi shopIds không tồn tại
        Step by step:
        Trả về rỗng
        :return:
        '''
        data = db.get_data_all("select * from schedule_targets")
        id = [int(data[i]['target_shop_id']) for i in range(len(data))]
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = None
        shopIds = max(id) + 1
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        assert response.status_code == 200
        assert len(result['result']['results']) == 0

    def test_shopIds_ton_tai_inactive(self):
        '''
        Kiểm tra response trả về khi shopIds tồn tại, đang inactive
        Step by step:
        Trả về rỗng
        :return:
        '''
        data = db.get_data_all("select * from shops where activate = 0")
        shopIds = random.choice([data[i]['id'] for i in range(len(data))])
        pageSize = None
        page = None
        activate = None
        orderBy = None
        crawType = None
        response = self.call_api(pageSize, page, activate, orderBy, crawType, shopIds)
        result = response.json()
        assert response.status_code == 200
        assert len(result['result']['results']) == 0





