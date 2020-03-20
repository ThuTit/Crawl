import pytest
import pytz
from settings import PCR_URL_SHOP
import requests
from support.db.db_connection import DbConnectMysql
from datetime import datetime
import random
from support.Excel2Data import data_test_PCR_29_update

db = DbConnectMysql()

url_list = PCR_URL_SHOP + 'shops'
url = PCR_URL_SHOP + 'shops/'

def get_id():
    shop_id = []
    shop_list = db.get_data_all('select * from shops;')
    for i in range(len(shop_list)):
        shop_id.append(shop_list[i]['id'])
    return shop_id

class TestPCR29Update:
    ISSUE_KEY = 'PCR-35'
    FOLDER = '/QC/API/Cập nhật cửa hàng'
    def setup_class(self):
        print('setup')
        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(20):
            DbConnectMysql().execute_query(
                f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt_qc{i}', 'https://thunt_qc{i}.vn', {random.choice([0, 1])}, {random.choice([0, 1])});")

    def teardown_class(self):
        print('teardown')
        DbConnectMysql().execute_query("delete from schedule_targets;")
        DbConnectMysql().execute_query("delete from category_extractors;")
        DbConnectMysql().execute_query("delete from product_extractors;")
        DbConnectMysql().execute_query("delete from shops where name like 'thunt_qc%';")

    data = data_test_PCR_29_update()

    @pytest.mark.parametrize('Title,  Expected, name, domain, status_code, code, message',
                             data)
    def test_update(self, Title, Expected, name, status_code, domain, code, message):
        f'''
        {Title}
        Step by step:
        Expect: {Expected}
        :return:
        '''
        json = {
            'name': name,
            'domain': domain,
            'activate': random.choice([True, False]),
            'activeInProductPrice': random.choice([True, False])
        }

        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        # data = db.get_data_one(f"select * from shops where id = '{id}';")
        assert response.status_code == status_code
        assert result['code'] == code
        assert result['message'] == message
        if response.status_code == 200:
            # record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
            DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {id};")
        else:
            assert response.status_code == 400


    def test_not_exsit_shop_id(self):
        '''
        <Update>Kiểm tra response khi shop_id không có trong db
        Step by step:
        Expect: Status = 404
        :return:
        '''
        id = max(get_id()) + 1
        response = requests.get(url=url + str(id))
        result = response.json()
        assert response.status_code == 404
        assert result['code'] == 'shop_not_found'


    def test_shop_id_null(self):
        '''
        <Update>Kiểm tra response khi shop_id = null
        Step by step:
        Expect: Status = 404
        :return:
        '''
        response = requests.get(url=url)
        assert response.status_code == 404
    def test_activate_null(self):
        '''
        <Update>Kiểm tra response trả về khi nhập trường activate = null
        Step by step:
        code = bad_request
        :return:
        '''
        json = {
            'name': 'name',
            'domain': 'http://domain.vn',
            'activate': None,
            'activeInProductPrice': random.choice([True, False])
        }

        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'activate': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_activate_int(self):
        '''
        <Update>Kiểm tra response trả về khi nhập trường activate = int
        Step by step:
        code = bad_request
        :return:
        '''
        json = {
            'name': 'name',
            'domain': 'http://domain.vn',
            'activate': 123,
            'activeInProductPrice': random.choice([True, False])
        }

        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'activate': [ErrorDetail(string='Must be a valid boolean.', code='invalid')]}"

    def test_activate_string(self):
        '''
        <Update>Kiểm tra response trả về khi nhập trường activate = string khác True/False
        Step by step:
        code = bad_request
        :return:
        '''
        json = {
            'name': 'name',
            'domain': 'http://domain.vn',
            'activate': 'sdfgh',
            'activeInProductPrice': random.choice([True, False])
        }

        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'activate': [ErrorDetail(string='Must be a valid boolean.', code='invalid')]}"

    def test_activeInProductPrice_null(self):
        '''
        <Update>Kiểm tra response trả về khi nhập trường activeInProductPrice = null
        Step by step:
        code = bad_request
        :return:
        '''
        json = {
            'name': 'name',
            'domain': 'http://domain.vn',
            'activate': random.choice([True, False]),
            'activeInProductPrice': None
        }

        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'active_in_product_price': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_activeInProductPrice_int(self):
        '''
        <Update>Kiểm tra response trả về khi nhập trường activeInProductPrice = int
        Step by step:
        code = bad_request
        :return:
        '''
        json = {
            'name': 'name',
            'domain': 'http://domain.vn',
            'activate': random.choice([True, False]),
            'activeInProductPrice': 234
        }

        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'active_in_product_price': [ErrorDetail(string='Must be a valid boolean.', code='invalid')]}"

    def test_activeInProductPrice_string(self):
        '''
        <Update>Kiểm tra response trả về khi nhập trường activeInProductPrice = string khác True/False
        Step by step:
        code = bad_request
        :return:
        '''
        json = {
            'name': 'name',
            'domain': 'http://domain.vn',
            'activate': random.choice([True, False]),
            'activeInProductPrice': 'sdfg'
        }

        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result['message'] == "{'active_in_product_price': [ErrorDetail(string='Must be a valid boolean.', code='invalid')]}"

    def test_exist_name(self):
        '''
        <Update>Kiểm tra response trả về khi update khi đã tồn tại name
        Step by step:
        code = bad_request
        :return:
        '''
        payload = {
            'name': 'name',
            'domain': 'https://thuyhgy.com'

        }
        response = requests.post(url=url_list, json=payload)
        assert response.status_code == 200
        json = {
            'name': 'name',
            'domain': 'http://domain.vn',
            'activate': random.choice([True, False]),
            'activeInProductPrice': random.choice([True, False])

        }
        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'shop_overlapped_name'
        assert result['message'] == "Shop name name has already been used"
        record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {record['id']};")
    def test_not_name(self):
        '''
        <Update>Kiểm tra response trả về khi update không có trường name
        Step by step:
        code = bad_request
        :return:
        '''

        json = {
            # 'name': 'name',
            'domain': 'http://domain.vn',
            'activate': random.choice([True, False]),
            'activeInProductPrice': random.choice([True, False])
        }
        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['message'] == "Updated shop successful"
        # record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {id};")

    def test_exist_domain(self):
        '''
        <Update>Kiểm tra response trả về khi update không có trường domain
        Step by step:
        code = bad_request
        :return:
        '''
        payload = {
            'name': 'name',
            'domain': 'https://thuyhgy.com',
            'activeInProductPrice': True,
            'activate': random.choice([True, False]),
        }
        response = requests.post(url=url_list, json=payload)
        assert response.status_code == 200
        json = {
            'name': 'name1',
            'domain': 'https://thuyhgy.com',
            'activate': random.choice([True, False]),
            'activeInProductPrice': random.choice([True, False])
        }
        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'shop_overlapped_domain'
        assert result['message'] == "Shop domain https://thuyhgy.com has already been used"
        record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {record['id']};")
    def test_not_domain(self):
        '''
        <Update>Kiểm tra response trả về khi update không có trường domain
        Step by step:
        code = bad_request
        :return:
        '''

        json = {
            'name': 'name',
            # 'domain': 'http://domain.vn',
            'activate': random.choice([True, False]),
            'activeInProductPrice': random.choice([True, False])
        }
        id = random.choice(get_id())
        response = requests.patch(url=url + str(id), json=json)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['message'] == "Updated shop successful"
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {id};")

