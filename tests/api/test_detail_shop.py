import pytz
from settings import PCR_URL_SHOP
import requests
from support.db.db_connection import DbConnectMysql
from datetime import datetime
import random


db = DbConnectMysql()

url_list = PCR_URL_SHOP + 'shops'
url = PCR_URL_SHOP + 'shops/'

# def get_id():
    # shop_id = []
    # shop_list = db.get_data_all('select * from shops;')
    # for i in range(len(shop_list)):
    #     shop_id.append(shop_list[i]['id'])
    # return shop_id

class TestPCR29Detail:
    ISSUE_KEY = 'PCR-37'
    FOLDER = '/QC/API/Detail cửa hàng'
    def setup_class(self):
        print('setup')
        payload = {
            'name': 'test_detail',
            'domain': 'https://testdetail.com',
            'activate': True,
            'activeInProductPrice': True
        }
        requests.post(url=url_list, json=payload)


    def teardown_class(self):
        print('teardown')
        data = DbConnectMysql().get_data_one('select * from shops;')
        DbConnectMysql().execute_query(f"delete from shops where id = {data['id']};")

    def test_get_detail_success(self):
        '''
        <Detail>Kiểm tra xem detail của shop thành công
        Step by step:
        Expect: Status = 200
        :return:
        '''
        data = DbConnectMysql().get_data_one('select * from shops')
        print(data)
        id = data['id']
        response = requests.get(url=url + str(id))
        result = response.json()
        data = db.get_data_one(f"select * from shops where id = '{id}';")
        assert response.status_code == 200
        assert result['code'] == 'success'
        assert result['result']['id'] == id
        assert result['result']['name'] == data['name']
        assert result['result']['domain'] == data['domain']
        assert datetime.strptime(result['result']['createdAt'], '%Y-%m-%dT%H:%M:%S%z') == pytz.utc.localize(data['created_at'])
        assert datetime.strptime(result['result']['updatedAt'], '%Y-%m-%dT%H:%M:%S%z') == pytz.utc.localize(data['updated_at'])

        if data['activate'] == 0:
            assert result['result']['activate'] == False
        else:
            assert result['result']['activate'] == True
        if data['active_in_product_price'] == 0:
            assert result['result']['activeInProductPrice'] == False
        else:
            assert result['result']['activeInProductPrice'] == True

    def test_not_exsit_shop_id(self):
        '''
        <Detail>Kiểm tra response khi shop_id không có trong db
        Step by step:
        Expect: Status = 404
        :return:
        '''
        data = DbConnectMysql().get_data_one('select * from shops')
        id = data['id'] + 1
        response = requests.get(url=url + str(id))
        result = response.json()
        assert response.status_code == 404
        assert result['code'] == 'shop_not_found'

    def test_shop_id_null(self):
        '''
        <Detail>Kiểm tra response khi shop_id = null
        Step by step:
        Expect: Status = 404
        :return:
        '''
        response = requests.get(url=url)
        assert response.status_code == 404




