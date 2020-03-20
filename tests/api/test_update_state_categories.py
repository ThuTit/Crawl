
import random

import requests

from support.db.db_connection import DbConnect
from settings import PCR_URL_TEST1, db_connection_test1
url = PCR_URL_TEST1 + 'categories'
db = DbConnect(db_connection_test1)
class TestPCR57:
    ISSUE_KEY = 'PCR-57'
    FOLDER = "/QC/API/Update trạng thái danh mục sản phẩm"
    def call_api_update(self, id, active):
        params = {
            'categoryIds': id,
            'activate': active
        }
        return requests.patch(url=url, json=params)
    def get_id_active(self):
        '''
        Trả về danh sách id của danh mục ở trạng thái active
        :return:
        '''
        sql = 'select id from crawled_categories where activate = 1 limit 1000'
        data = db.get_all_data(sql)
        id_active = [data[i]['id'] for i in range(len(data))]
        return id_active
    def get_id_inactive(self):
        '''
        Trả về danh sách id của danh mục ở trạng thái inactive
        :return:
        '''
        sql = 'select id from crawled_categories where activate = 0'
        data = db.get_all_data(sql)
        id_inactive = [data[i]['id'] for i in range(len(data))]
        return id_inactive

    def test_true_false(self):
        '''
        Kiểm tra response khi chuyển trạng thái danh mục từ true -> false
        Step by step:
        Expect: code = success
        :return:
        '''
        id = [random.choice(self.get_id_active())]
        active = False
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        sql = f"select * from crawled_categories where id = '{id[0]}'";
        data = db.get_all_data(sql)
        assert len(data) == 1
        assert data[0]['activate'] == 0

    def test_false_true(self):
        '''
        Kiểm tra response khi chuyển trạng thái danh mục từ false -> true
        Step by step:
        Expect: code = success
        :return:
        '''
        id = [random.choice(self.get_id_inactive())]
        active = True
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        sql = f"select * from crawled_categories where id = '{id[0]}'";
        data = db.get_all_data(sql)
        assert len(data) == 1
        assert data[0]['activate'] == 1

    def test_true_true(self):
        '''
        Kiểm tra response khi chuyển trạng thái danh mục từ true -> true
        Step by step:
        Expect: code = success
        :return:
        '''
        id = [random.choice(self.get_id_active())]
        active = True
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        sql = f"select * from crawled_categories where id = '{id[0]}'";
        data = db.get_all_data(sql)
        assert len(data) == 1
        assert data[0]['activate'] == 1
    def test_false_false(self):
        '''
        Kiểm tra response khi chuyển trạng thái danh mục từ false -> false
        Step by step:
        Expect: code = success
        :return:
        '''
        id = [random.choice(self.get_id_inactive())]
        active = False
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        sql = f"select * from crawled_categories where id = '{id[0]}'";
        data = db.get_all_data(sql)
        assert len(data) == 1
        assert data[0]['activate'] == 0
    def test_id_object_or_string(self):
        '''
        Kiểm tra response khi categoryIds = str
        Step by step:
        Expect: code = bad_request
        :return:
        '''
        id = random.choice(self.get_id_inactive())
        active = False
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
    def test_categoryIds_empty(self):
        '''
        Kiểm tra response khi categoryIds = []
        Step by step:
        Expect: code = invalid_value
        :return:
        '''
        # id = random.choice(self.get_id_inactive())
        active = False
        response = self.call_api_update(id=[], active=active)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'invalid_value'
    def test_not_categoryIds(self):
        '''
        Kiểm tra response khi không có categoryIds
        Step by step:
        Expect: code = bad_request
        :return:
        '''
        params = {
            # 'categoryIds': id,
            'activate': False
        }
        response = requests.patch(url=url, json=params)
        # response = self.call_api_update(id=[], active=active)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_not_activate(self):
        '''
        Kiểm tra response khi không có activate
        Step by step:
        Expect: code = bad_request
        :return:
        '''
        id = random.choice(self.get_id_inactive())
        params = {
            'categoryIds': [id],
            # 'activate': False
        }
        response = requests.patch(url=url, json=params)
        # response = self.call_api_update(id=[], active=active)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_id_not_found(self):
        '''
        Kiểm tra response khi categoryIds = id không tồn tại
        Step by step:
        Expect: code = category_not_found
        :return:
        '''
        id = ['fkdjlfsdjdf']
        active = False
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 404
        assert result['code'] == 'category_not_found'

    def test_activate_Khac_true_false(self):
        '''
        Kiểm tra response khi activate khác true/false
        Step by step:
        Expect: code = bad_request
        :return:
        '''
        id = random.choices(self.get_id_inactive())
        active = 'fss'
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
    def test_many_id(self):
        '''
        Kiểm tra response khi categoryIds có nhiều giá trị hợp lệ
        Step by step:
        Expect: code = success
        :return:
        '''
        sql = 'select id from crawled_categories limit 1000;'
        data = db.get_all_data(sql)
        id = [data[i]['id'] for i in range(len(data))]

        # id = self.get_id_active()
        print(id)
        active = True
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        # for i in id:
        #     sql = f"select * from crawled_categories where id = '{i}'";
        #     data = db.get_all_data(sql)
        #     assert len(data) == 1
        #     assert data[0]['activate'] == 1

    def test_many_id_have_invalid(self):
        '''
        Kiểm tra response khi categoryIds có nhiều giá trị, trong đó có giá trị không hợp lệ
        Step by step:
        Expect: code = category_not_found
        :return:
        '''
        id = [random.choice(self.get_id_inactive()),'rtuio']
        active = True
        response = self.call_api_update(id=id, active=active)
        result = response.json()
        assert response.status_code == 404
        assert result['code'] == 'category_not_found'



