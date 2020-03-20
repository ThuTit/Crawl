import json
import pytest
from settings import PCR_URL_SHOP
import requests
from support.db.db_connection import DbConnectMysql
from support.Excel2Data import create_data_test
url=PCR_URL_SHOP+'shops'
class Testcreateshop:
    ISSUE_KEY = 'PCR-7'
    # ISSUE_KEY = 'DP-19'
    FOLDER = '/QC/API/Tạo mới cửa hàng'
    data = create_data_test()
    def setup_class(self):
        DbConnectMysql().execute_query("DELETE FROM shops;")
    def teardown_class(self):
        print("teardown")
    @pytest.mark.parametrize('Title, Expected, name, domain, activate, activateInProductPrice, code, message',
                             data)
    def test_validate(self, Title, Expected, name, domain, activate, activateInProductPrice, code, message):
        f'''
        {Title}
        Step by step:
        Expect: {Expected}
        :return:
        '''
        # DbConnectMysql().execute_query("DELETE FROM shops;")
        payload = {
            'name': name,
            'domain': domain,
            'activate': activate,
            'activeInProductPrice': activateInProductPrice
        }
        # print(payload)
        response = requests.post(url=url, json=payload)
        result = response.json()
        print(json.dumps(result))
        assert result['code'] == code
        assert result['message'] == message

        if response.status_code == 200:
            record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
            DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {record['id']};")
        else:
            assert response.status_code == 400

    def test_activate_null(self):
        '''
        Kiểm tra response trả về khi nhập activate = null

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://neqfsu.com',
            'activate': None,
            'activeInProductPrice': True
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'
        # assert result['extra'] == None
        # assert result['message'] == "{'name': [ErrorDetail(string='This field may not be null.', code='null')]}"

    def test_activate_int(self):
        '''
        Kiểm tra response trả về khi nhập activate = int

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://neqfsu.com',
            'activate': 123,
            'activeInProductPrice': True
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'

    def test_activate_string_different_True_False(self):
        '''
        Kiểm tra response trả về khi nhập activate = string khác True/False

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://neqfsu.com',
            'activate': 123,
            'activeInProductPrice': True
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'

    def test_not_activate(self):
        '''
        Kiểm tra response trả về khi không có trường activate

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = success, activate default = True
        :return:
        '''
        payload = {
            'name': 'test546qưertyu23',
            'domain': 'https://neqgggfsu.com',
            'activeInProductPrice': True
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'success'
        record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {record['id']};")


    def test_activeInProductPrice_null(self):
        '''
        Kiểm tra response trả về khi nhập activeInProductPrice = null

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://neqfsu.com',
            'activate': True,
            'activeInProductPrice': None
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'

    def test_activeInProductPrice_int(self):
        '''
        Kiểm tra response trả về khi nhập activeInProductPrice = int

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://neqfsu.com',
            'activate': True,
            'activeInProductPrice': 1234567
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'

    def test_activeInProductPrice_string_different_True_False(self):
        '''
        Kiểm tra response trả về khi nhập activeInProductPrice = string khác True/False

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://neqfsu.com',
            'activate': False,
            'activeInProductPrice': 'dfbfdsgad'
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'

    def test_not_activeInProductPrice(self):
        '''
        Kiểm tra response trả về khi không có trường activeInProductPrice

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = success
        :return:
        '''
        payload = {
            'name': 'test5ádfghj4623',
            'domain': 'https://nejjjqfsu.com',
            'activate' : True

        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'success'
        record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {record['id']};")

    def test_not_name(self):
        '''
        Kiểm tra response trả về khi không có trường name

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            # 'name': 'test54623',
            'domain': 'https://neqfsu.com',
            'activate' : True,
            'activeInProductPrice': True


        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'

    def test_not_domain(self):
        '''
        Kiểm tra response trả về khi không có trường domain

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = bad_request
        :return:
        '''
        payload = {
            'name': 'test54623',
            # 'domain': 'https://neqfsu.com',
            'activate' : True,
            'activeInProductPrice': True


        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'bad_request'

    def test_exist_name(self):
        '''
        Kiểm tra response trả về khi không có trường name

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = shop_overlapped_name
        :return:
        '''
        payload1 = {
            'name': 'test5qưer46ggg23',
            'domain': 'https://nennnnqfsu.com',
            'activate': True,
            'activeInProductPrice': True

        }
        payload = {
            'name': 'test5qưer46ggg23',
            'domain': 'https://neqmmmmfsu1234.com',
            'activate' : True,
            'activeInProductPrice': True


        }
        requests.post(url=url, json=payload1)
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'shop_overlapped_name'
        record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {record['id']};")

    def test_exist_domain(self):
        '''
        Kiểm tra response trả về khi không có trường domain

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = shop_overlapped_name
        :return:
        '''
        payload1 = {
            'name': 'test54ẻtyu623',
            'domain': 'https://neqfsu.com',
            'activate': True,
            'activeInProductPrice': True

        }
        payload = {
            'name': 'test546232df13432',
            'domain': 'https://neqfsu.com',
            'activate': True,
            'activeInProductPrice': True

        }
        requests.post(url=url, json=payload1)
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'shop_overlapped_domain'
        record = DbConnectMysql().get_data_one("select * from shops order by id desc;")
        DbConnectMysql().execute_query(f"DELETE FROM shops WHERE id = {record['id']};")


    def test_domain_have_special_character(self):
        '''
        Kiểm tra response trả về khi nhập Domain = kí tự đặc biệt

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = invalid_value
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://!!!!!!!!!!@com',
            'activate' : True,
            'activeInProductPrice': True


        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'invalid_value'
        assert result['message'] == '"https://!!!!!!!!!!@com" is not a valid URL'

    def test_domain_is_tieng_viet(self):
        '''
        Kiểm tra response trả về khi nhập Domain = tiếng việt có dấu

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = invalid_value
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'https://thế.com',
            'activate' : True,
            'activeInProductPrice': True


        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'invalid_value'
        assert result['message'] == '"https://thế.com" is not a valid URL'


    def test_domain_has_space(self):
        '''
        Kiểm tra response trả về khi nhập Domain có khoảng trắng ở giữa

        Step by step:
        - Nhập các trường tương ứng
        - Gọi api
        - Kiểm tra response trả về

        Expect: code = invalid_value
        :return:
        '''
        payload = {
            'name': 'test54623',
            'domain': 'http://neq fs.com',
            'activate' : True,
            'activeInProductPrice': True
        }
        response = requests.post(url=url, json=payload)
        result = response.json()
        # print(json.dumps(result))
        assert result['code'] == 'invalid_value'
        assert result['message'] == '"http://neq fs.com" is not a valid URL'

