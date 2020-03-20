from settings import PCR_URL_SHOP
import requests
from support.db.db_connection import DbConnectMysql
from datetime import datetime
import random

db = DbConnectMysql()

url_list = PCR_URL_SHOP + 'shops'
url = PCR_URL_SHOP + 'shops/'

def get_id():
    shop_id = []
    shop_list = db.get_data_all('select * from shops;')
    for i in range(len(shop_list)):
        shop_id.append(shop_list[i]['id'])
    return shop_id

class TestPCR29Del:
    ISSUE_KEY = 'PCR-34'
    FOLDER = '/QC/API/Xóa cửa hàng'
    def setup_class(self):
        print('setup')
        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(20):
            DbConnectMysql().execute_query(
                f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt_qc{i}', 'https://thunt_qc{i}.vn', {random.choice([0, 1])}, {random.choice([0, 1])});")

    def teardown_class(self):
        print('teardown')
        DbConnectMysql().execute_query("delete from shops where name like 'thunt_qc%';")
    def test_delete_success(self):
        '''
        <Del>Kiểm tra xóa shop thành công
        Step by step:
        Expect: Status = 200
        :return:
        '''
        id = random.choice(get_id())
        response = requests.delete(url=url + str(id))
        result = response.json()
        data = db.get_data_one(f"select * from shops where id = '{id}';")
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['message'] == 'Delete successful'
        assert data == None

    def test_not_exsit_shop_id(self):
        '''
        <Del>Kiểm tra response khi shop_id không có trong db
        Step by step:
        Expect: Status = 404
        :return:
        '''
        id = max(get_id()) + 1
        response = requests.get(url=url + str(id))
        result = response.json()
        data = db.get_data_one(f"select * from shops where id = '{id}';")
        assert response.status_code == 404
        assert result['code'] == 'shop_not_found'

    def test_shop_id_null(self):
        '''
        <Del>Kiểm tra response khi shop_id = null
        Step by step:
        Expect: Status = 404
        :return:
        '''
        response = requests.get(url=url)
        assert response.status_code == 404

