import json
import string
import pytest
from settings import PCR_URL_SHOP
import requests
from support.db.db_connection import DbConnectMysql
from datetime import datetime
import random

# from support.Excel2Data import data_test_PCR_29_update

db = DbConnectMysql()

url_shop = PCR_URL_SHOP + 'shops/'


def get_id():
    shop_id = []
    shop_list = db.get_data_all('select * from shops;')
    for i in range(len(shop_list)):
        shop_id.append(shop_list[i]['id'])
    return shop_id


class TestPCR41Update:
    ISSUE_KEY = 'PCR-41'
    FOLDER = '/QC/API/Config extractor'

    def setup_class(self):
        print('setup')
        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(20):
            DbConnectMysql().execute_query(
                f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt_qc{i}', 'https://thunt-qc{i}.vn', {random.choice([0, 1])}, {random.choice([0, 1])});")

    def teardown_class(self):
        print('teardown')
        DbConnectMysql().execute_query("delete from category_extractors ;")
        DbConnectMysql().execute_query("delete from product_extractors;")
        DbConnectMysql().execute_query("delete from shops where name like 'thunt_qc%' or name like '%update extractor%';")
    def text(self, length=None):
        length = 10 if length is None else length
        return ''.join(
            random.choice(string.ascii_lowercase) for i in range(length)
        )

    def call_api(self, url, catSet, catPay, proSet, proPay):
        json = {
            'name': self.text(),
            'domain': 'https://'+self.text()+'.com',
            'activate': random.choice([True, False]),
            'activeInProductPrice': random.choice([True, False]),
            'categoryCustomUrl': url,
            'categorySettings': catSet,
            'categoryPayload': catPay,
            'productSettings': proSet,
            'productPayload': proPay
        }
        id = random.choice(get_id())
        print(id)
        return requests.patch(url=url_shop + str(id), json=json)

    def test_valid(self):
        '''
        Kiểm tra response khi nhập các trường hợp lệ
        Step by step:
        Status_code =200, code = success
        :return:
        '''
        url = 'https://updateextractor.com'
        catSet = '''{

            "meta_title": "mjhiaqgjag"
           }'''
        catPay = '''{

            "meta_title": "mjhiaqgjag"
           }'''
        proSet = '''{

            "meta_title": "mjhiaqgjag"
           }'''
        proPay = '''{

            "meta_title": "mjhiaqgjag"
           }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        print(result['message'])
        assert response.status_code == 200
        assert result['code'] == 'success'


    def test_2(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL không bắt đầu với http(s)
        Step by step:
        Status_code =400, code = invalid_value
        :return:
        '''
        url = 'updateextractor.com'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_value'

    def test_3(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL có khoảng trắng ở giữa
        Step by step:
        Status_code =400, code = invalid_value
        :return:
        '''
        url = 'https://update  extractor.com'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_value'

    def test_4(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = khoảng trắng
        Step by step:
        Status_code =200, code = success
        :return:
        '''
        url = ' '
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_5(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = text có space đầu cuối
        Step by step:
        Status_code =200, code = success
        :return:
        '''
        url = ' https://updateextractor.com '
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_6(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = kí tự đặc biệt
        Step by step:
        Status_code =400, code = invalid_value
        :return:
        '''
        url = ' https://!@#$^^^^.com '
        catSet = '''{

               "meta_title": "mjhiaqgjag",
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag",
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag",
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag",
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_value'

    def test_7(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = maxlength
        Step by step:
        Status_code =200, code = success
        :return:
        '''
        url = 'https://nequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsum.vn'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 200
        assert result['code'] == 'success'
    def test_8(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL > maxlength
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = 'https://nequeporroquisquamestquidolorqrtemipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsum.vn'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_9(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = chữ in hoa, in thường
        Step by step:
        Status_code =200, code = success, url được giữ nguyên
        :return:
        '''
        url = 'https://configextractor.com/QASDFsdfghj'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 200
        assert result['code'] == 'success'
        data = db.get_data_one("select * from category_extractors order by id desc;")
        assert data['custom_url'] == url
    def test_10(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = tiếng việt có dấu
        Step by step:
        Status_code =400, code = invalid_value
        :return:
        '''
        url = 'https://wthuuô.com'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_value'

    def test_11(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = chữ số
        Step by step:
        Status_code =200, code = success
        :return:
        '''
        url = 'https://12345.com'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_12(self):
        '''
        Kiểm tra thêm shop khi nhập Custom URL = html, javascript
        Step by step:
        Status_code =400, code = invalid_value
        :return:
        '''
        url = 'https://<h4>test</h4>.com'
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_value'

    def test_13(self):
        '''
        Kiểm tra thêm shop khi edit Custom URL = null
        Step by step:
        Status_code =200, code = success
        :return:
        '''
        url = None
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_14(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới categorySettings = int
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        catSet = 12345
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_json'
    def test_15(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới categorySettings = null
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        catSet = None
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
    def test_16(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới categorySettings =''
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        catSet = ''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_17(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới categoryPayload = int
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        catPay = 12345
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_json'

    def test_18(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới categoryPayload = null
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        catPay = None
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_19(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới categoryPayload =''
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        catPay = ''
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
    def test_20(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới productSettings = int
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        proSet = 12345
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_json'

    def test_21(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới productSettings = null
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        proSet = None
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_22(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới productSettings =''
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        proSet = ''
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
    def test_23(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới productPayload = int
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        proPay = 12345
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'invalid_json'

    def test_24(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới productPayload = null
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        proPay = None
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_25(self):
        '''
        Kiểm tra hiển thị thông báo khi thêm mới productPayload =''
        Step by step:
        Status_code =400, code = bad_request
        :return:
        '''
        url = None
        proPay = ''
        catSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        proSet = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        catPay = '''{

               "meta_title": "mjhiaqgjag"
              }'''
        response = self.call_api(url=url, catSet=catSet, catPay=catPay, proSet=proSet, proPay=proPay)
        result = response.json()
        print(result['message'])
        assert response.status_code == 400
        assert result['code'] == 'bad_request'




