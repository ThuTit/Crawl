from datetime import timedelta, datetime
import requests
import random
from numpy.random import choice
from any_case import converts_keys
from support.db.db_connection import DbConnectMysql
import json

from settings import PCR_URL_SHOP

url = PCR_URL_SHOP + 'categories'
db = DbConnectMysql()


class TestPCR33:
    ISSUE_KEY = 'PCR-33'
    FOLDER = '/QC/API/Danh sách danh mục'

    def call_api(self, pageSize, page, orderBy, q, shopIds):
        params = {
            'pageSize': pageSize,
            'page': page,
            'q': q,
            'orderBy': orderBy,
            'shopIds': shopIds,
        }
        return requests.get(url=url, params=params)

    def test_pageSize_null(self):
        '''
        Kiểm tra response trả về khi pageSize = null
        Step by step:
        Trả về 10 bản ghi
        :return:
        '''
        pageSize = None
        page = None
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
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
        orderBy = None
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        assert response.status_code == 400

    def test_orderBy_name_asc(self):
        '''
        Kiểm tra response trả về khi orderBy = schedule_name
        Step by step:
        Trả về danh sách lịch được sắp xếp theo schedule_name asc
        :return:
        '''
        pageSize = 1000
        page = None
        orderBy = 'name'
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        result = response.json()
        record = db.get_data_all('select * from crawled_categories where mptt_level = 0 order by name asc;')
        assert response.status_code == 200
        assert len(result['result']['results']) == len(record)

        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            assert result['result']['results'][i]['categories']['name'] == record[i]['name']
            # assert result['result']['results'][i]['id'] == record[i]['id']
            # assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            # assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type']
            # assert result['result']['results'][i]['scheduleType'] == record[i]['schedule_type']
            # assert result['result']['results'][i]['state'] == record[i]['state']
            # assert result['result']['results'][i]['scheduleSettings'] == converts_keys(data=json.loads(record[i]['schedule_settings']),
            #                                                          case='camel')
            # assert result['result']['results'][i]['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            # assert result['result']['results'][i]['startDate'] == datetime.strftime(record[i]['start_date'], '%Y-%m-%d')

    def test_orderBy_name_desc(self):
        '''
        Kiểm tra response trả về khi orderBy = -name
        Step by step:
        Trả về danh sách lịch được sắp xếp theo name desc
        :return:
        '''
        pageSize = 1000
        page = None
        orderBy = '-name'
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        result = response.json()
        record = db.get_data_all('select * from crawled_categories where mptt_level = 0 order by name desc;')
        assert response.status_code == 200
        assert len(result['result']['results']) == len(record)

        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            # assert result['result']['results'][i]['id'] == record[i]['id']
            assert result['result']['results'][i]['categories']['name'] == record[i]['name']

    def test_orderBy_url_asc(self):
        '''
        Kiểm tra response trả về khi orderBy = url
        Step by step:
        Trả về danh sách lịch được sắp xếp theo url asc
        :return:
        '''
        pageSize = 1000
        page = None
        orderBy = 'url'
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        result = response.json()
        record = db.get_data_all('select * from crawled_categories where mptt_level = 0 order by url asc;')
        assert response.status_code == 200
        assert len(result['result']['results']) == len(record)

        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            assert result['result']['results'][i]['categories']['url'] == record[i]['url']
            # assert result['result']['results'][i]['id'] == record[i]['id']
            # assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
            # assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type']
            # assert result['result']['results'][i]['scheduleType'] == record[i]['schedule_type']
            # assert result['result']['results'][i]['state'] == record[i]['state']
            # assert result['result']['results'][i]['scheduleSettings'] == converts_keys(data=json.loads(record[i]['schedule_settings']),
            #                                                          case='camel')
            # assert result['result']['results'][i]['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            # assert result['result']['results'][i]['startDate'] == datetime.strftime(record[i]['start_date'], '%Y-%m-%d')

    def test_orderBy_url_desc(self):
        '''
        Kiểm tra response trả về khi orderBy = -url
        Step by step:
        Trả về danh sách lịch được sắp xếp theo url desc
        :return:
        '''
        pageSize = 1000
        page = None
        orderBy = '-url'
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        result = response.json()
        record = db.get_data_all('select * from crawled_categories where mptt_level = 0 order by url desc;')
        assert response.status_code == 200
        assert len(result['result']['results']) == len(record)

        for i in range(len(result['result']['results'])):
            # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
            # minutes, seconds = divmod(remainder, 60)
            # assert result['result']['results'][i]['id'] == record[i]['id']
            assert result['result']['results'][i]['categories']['url'] == record[i]['url']

    # def test_orderBy_id_asc(self):
    #     '''
    #     Kiểm tra response trả về khi orderBy = id
    #     Step by step:
    #     Trả về danh sách lịch được sắp xếp theo id asc
    #     :return:
    #     '''
    #     pageSize = 1000
    #     page = None
    #     orderBy = 'id'
    #     q = None
    #     shopIds = None
    #     response = self.call_api(pageSize, page, orderBy, q, shopIds)
    #     result = response.json()
    #     record = db.get_data_all('select * from crawled_categories where mptt_level = 0 order by id asc;')
    #     assert response.status_code == 200
    #     assert len(result['result']['results']) == len(record)
    #
    #     for i in range(len(result['result']['results'])):
    #         # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
    #         # minutes, seconds = divmod(remainder, 60)
    #         assert result['result']['results'][i]['categories']['id'] == record[i]['id']
    #         # assert result['result']['results'][i]['id'] == record[i]['id']
    #         # assert result['result']['results'][i]['scheduleName'] == record[i]['schedule_name']
    #         # assert result['result']['results'][i]['crawlType'] == record[i]['crawl_type']
    #         # assert result['result']['results'][i]['scheduleType'] == record[i]['schedule_type']
    #         # assert result['result']['results'][i]['state'] == record[i]['state']
    #         # assert result['result']['results'][i]['scheduleSettings'] == converts_keys(data=json.loads(record[i]['schedule_settings']),
    #         #                                                          case='camel')
    #         # assert result['result']['results'][i]['scheduleTime'] == '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    #         # assert result['result']['results'][i]['startDate'] == datetime.strftime(record[i]['start_date'], '%Y-%m-%d')
    #
    # def test_orderBy_id_desc(self):
    #     '''
    #     Kiểm tra response trả về khi orderBy = -id
    #     Step by step:
    #     Trả về danh sách lịch được sắp xếp theo id desc
    #     :return:
    #     '''
    #     pageSize = 1000
    #     page = None
    #     orderBy = '-id'
    #     q = None
    #     shopIds = None
    #     response = self.call_api(pageSize, page, orderBy, q, shopIds)
    #     result = response.json()
    #     record = db.get_data_all('select * from crawled_categories where mptt_level = 0 order by id desc;')
    #     assert response.status_code == 200
    #     assert len(result['result']['results']) == len(record)
    #
    #     for i in range(len(result['result']['results'])):
    #         # hours, remainder = divmod(timedelta.total_seconds(record[i]['schedule_time']), 3600)
    #         # minutes, seconds = divmod(remainder, 60)
    #         # assert result['result']['results'][i]['id'] == record[i]['id']
    #         assert result['result']['results'][i]['categories']['id'] == record[i]['id']

    def test_orderBy_invalid(self):
        '''
        Kiểm tra response trả về khi orderBy không hợp lệ
        Step by step:
        Trả về status_code = 400
        :return:
        '''
        pageSize = None
        page = None
        orderBy = 'tyuio'
        q = None
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        assert response.status_code == 400

    def test_shopIds_ton_tai_crawled(self):
        '''
        Kiểm tra response trả về khi shopIds tồn tại, đã được crawl
        Step by step:
        Trả về bản ghi có shopIds là giá trị truyền vào params
        :return:
        '''
        data = db.get_data_all("select shop_id from crawled_categories")
        list_id = [data[i]['shop_id'] for i in range(len(data))]
        list_id_crawled = list(set(list_id))
        id = choice(list_id_crawled, size=3, replace=False)
        shopIds = str(id[0]) + "," + str(id[1]) + "," + str(id[2])
        pageSize = None
        page = None
        orderBy = None
        q = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        result = response.json()
        assert response.status_code == 200
        assert len(id) == len(result['result']['results']) == result['result']['totalItems']
        for j in range(len(result['result']['results'])):
            assert id[0] or id[1] or id[2] in result['result']['results'][j]['shops']['id']

    def test_shopIds_ton_tai_not_yet_crawled(self):
        '''
        Kiểm tra response trả về khi shopIds tồn tại, chưa được crawl
        Step by step:
        Trả về rỗng
        :return:
        '''
        data1 = db.get_data_all("select shop_id from crawled_categories")
        list_id = [data1[i]['shop_id'] for i in range(len(data1))]
        list_id_crawled = list(set(list_id))
        data2 = db.get_data_all("select id from shops;")
        list_id_shop = [data2[i]['id'] for i in range(len(data2))]
        id_shop_not_yet_crawled = list(set(list_id_shop) - set(list_id_crawled))
        id = choice(id_shop_not_yet_crawled, size=2, replace=False)
        shopIds = str(id[0]) + "," + str(id[1])
        pageSize = None
        page = None
        orderBy = None
        q = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        result = response.json()
        assert response.status_code == 200
        assert result['result']['results'] == []

    def test_shopIds_khong_ton_tai(self):
        '''
        Kiểm tra response trả về khi shopIds không tồn tại
        Step by step:
        Trả về 404
        :return:
        '''
        data = db.get_data_all("select id from shops;")
        id = [int(data[i]['id']) for i in range(len(data))]
        pageSize = None
        page = None
        orderBy = None
        q = None
        shopIds = max(id) + 1
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        result = response.json()
        assert response.status_code == 404

    def test_search_have_result(self):
        '''
        Kiểm tra response trả về khi search có kết quả
        Step by step:
        Trả về danh sách danh mục có name hoặc url chứa keyword
        :return:
        '''
        pageSize = 1000
        page = None
        orderBy = None
        q = 'camera'
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        data = db.get_data_all("select * from crawled_categories where name like '%camera%' or url like '%camera%';")
        result = response.json()
        assert response.status_code == 200
        assert result['result']['totalItems']== len(data)

    def test_search_have_not_result(self):
        '''
        Kiểm tra response trả về khi search không có kết quả
        Step by step:
        Trả về []
        :return:
        '''
        pageSize = 1000
        page = None
        orderBy = None
        q = 'ưertyuiojhgfd'
        shopIds = None
        response = self.call_api(pageSize, page, orderBy, q, shopIds)
        data = db.get_data_all("select * from crawled_categories where name like '%ưertyuiojhgfd%' or url like '%ưertyuiojhgfd%';")
        result = response.json()
        assert response.status_code == 200
        assert len(result['result']['results']) == len(data)
