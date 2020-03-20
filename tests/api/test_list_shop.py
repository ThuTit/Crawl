from datetime import datetime
import random
from settings import PCR_URL_SHOP
import requests
from support.db.db_connection import DbConnectMysql
db = DbConnectMysql()

url_list = PCR_URL_SHOP + 'shops'
url = PCR_URL_SHOP + 'shops/'

def get_id():
    shop_id = []
    shop_list = db.get_data_all('select * from shops;')
    for i in range(len(shop_list)):
        shop_id.append(shop_list[i]['id'])
    return shop_id


class TestPCR29List:
    ISSUE_KEY = 'PCR-8'
    FOLDER = '/QC/API/Danh sách cửa hàng'

    def setup_class(self):
        print('setup')
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(20):
            DbConnectMysql().execute_query(
                f"insert into shops (created_at, updated_at, name, domain, activate, active_in_product_price ) values ('{time}', '{time}', 'thunt_qc{i}', 'https://thunt_qc{i}.vn', {random.choice([0, 1])}, {random.choice([0, 1])});")

    def teardown_class(self):
        print('teardown')
        DbConnectMysql().execute_query("delete from shops where name like 'thunt_qc%';")

    def call_api_get_list(self, pageSize, page, q, orderBy, activate, activeInProductPrice):
        params = {
            'pageSize': pageSize,
            'page': page,
            'q': q,
            'orderBy': orderBy,
            'activate': activate,
            'activeInProductPrice': activeInProductPrice
        }
        return requests.get(url=url_list, params=params)

    def test_valid(self):
        '''
        <Get_List>Kiểm tra response khi các trường hợp lệ
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 200
        assert len(data) == result['result']['totalItems']

    def test_pageSize_am(self):
        '''
        <Get_List>Kiểm tra response khi pageSize < 0
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=-1, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'pageSize': [ErrorDetail(string='Ensure this value is greater than or equal to 1.', code='min_value')]}"

    def test_pageSize_0(self):
        '''
        <Get_List>Kiểm tra response khi pageSize = 0
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=0, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'pageSize': [ErrorDetail(string='Ensure this value is greater than or equal to 1.', code='min_value')]}"

    def test_pageSize_1(self):
        '''
        <Get_List>Kiểm tra response khi pageSize = 1
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=1, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_one('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 1
        assert result['result']['results'][0]['id'] == data['id']
        assert result['result']['results'][0]['name'] == data['name']
        assert result['result']['results'][0]['domain'] == data['domain']

    def test_pageSize_float(self):
        '''
        <Get_List>Kiểm tra response khi pageSize = float
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=12.345, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'pageSize': [ErrorDetail(string='A valid integer is required.', code='invalid')]}"

    def test_pageSize_string(self):
        '''
        <Get_List>Kiểm tra response khi pageSize = string
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize='ưert', page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'pageSize': [ErrorDetail(string='A valid integer is required.', code='invalid')]}"

    def test_page_am(self):
        '''
        <Get_List>Kiểm tra response khi page< 0
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=-1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'page': [ErrorDetail(string='Ensure this value is greater than or equal to 1.', code='min_value')]}"

    def test_page_0(self):
        '''
        <Get_List>Kiểm tra response khi page = 0
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=0, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'page': [ErrorDetail(string='Ensure this value is greater than or equal to 1.', code='min_value')]}"

    def test_page_1(self):
        '''
        <Get_List>Kiểm tra response khi page = 1
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_page_999(self):
        '''
        <Get_List>Kiểm tra response khi page = 1
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=999, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 0
        # for i in range(10):
        #     assert result['result']['results'][i]['id'] == data[i]['id']
        #     assert result['result']['results'][i]['name'] == data[i]['name']
        #     assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_page_1000(self):
        '''
        <Get_List>Kiểm tra response khi page = 1
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1000, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'page': [ErrorDetail(string='Ensure this value is less than or equal to 999.', code='max_value')]}"

    def test_page_float(self):
        '''
        <Get_List>Kiểm tra response khi page = float
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=12.3456, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'page': [ErrorDetail(string='A valid integer is required.', code='invalid')]}"

    def test_page_string(self):
        '''
        <Get_List>Kiểm tra response khi page = string
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page='qưer', q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'page': [ErrorDetail(string='A valid integer is required.', code='invalid')]}"

    def test_q_int(self):
        '''
        <Get_List>Kiểm tra response khi q = int
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=123445, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_q_255(self):
        '''
        <Get_List>Kiểm tra response khi q = 255 kí tự
        Expect: Báo lỗi
        :return:
        '''
        q = 'nequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsi'
        response = self.call_api_get_list(pageSize=10, page=1, q=q, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'

    def test_q_maxlength(self):
        '''
        <Get_List>Kiểm tra response khi q > 255 kí tự
        Expect: Báo lỗi
        :return:
        '''
        q = 'nequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsitamdfghetnequeporroquisquamestquidoloremipsumquiadolorsitametnequeporroquisquamestquidoloremipsumquiadolorsi'
        response = self.call_api_get_list(pageSize=10, page=1, q=q, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        # data = DbConnectMysql().get_data_all('select * FROM shops;')
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == "{'q': [ErrorDetail(string='Ensure this field has no more than 255 characters.', code='max_length')]}"

    def test_orderBy_int(self):
        '''
        <Get_List>Kiểm tra response khi orderBy = int
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=1234, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'


    def test_orderBy_null(self):
        '''
        <Get_List>Kiểm tra response khi orderBy = null
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_orderBy_name_asc(self):
        '''
        <Get_List>Kiểm tra response khi orderBy = name
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy='name', activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by name asc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_orderBy_name_desc(self):
        '''
        <Get_List>Kiểm tra response khi orderBy = -name
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy='-name', activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by name desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_orderBy_domain_asc(self):
        '''
        <Get_List>Kiểm tra response khi orderBy = domain
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy='domain', activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by domain asc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_orderBy_domain_desc(self):
        '''
        <Get_List>Kiểm tra response khi orderBy = -domain
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy='-domain', activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by domain desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_orderBy_different(self):
        '''
        <Get_List>Kiểm tra response khi orderBy khác (name, -name, domain, -domain)
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy='sdfgh', activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_activate_all(self):
        '''
        <Get_List>Kiểm tra response khi activate = all
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate='all',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activate_activate(self):
        '''
        <Get_List>Kiểm tra response khi activate = active
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate='active',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops where activate = 1 order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activate_inactivate(self):
        '''
        <Get_List>Kiểm tra response khi activate = inactive
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate='inactive',
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops where activate = 0 order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activate_different(self):
        '''
        <Get_List>Kiểm tra response khi activate khác (all, activate, inactivate)
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate='ádfgh',
                                          activeInProductPrice='all')
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == '''{'activate': [ErrorDetail(string='\"ádfgh\" is not a valid choice.', code='invalid_choice')]}'''

    def test_activate_int(self):
        '''
        <Get_List>Kiểm tra response khi activate = int
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=12345,
                                          activeInProductPrice='all')
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == '''{'activate': [ErrorDetail(string='\"12345\" is not a valid choice.', code='invalid_choice')]}'''

    def test_activeInProductPrice_all(self):
        '''
        <Get_List>Kiểm tra response khi activeInProductPrice = all
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice='all')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        assert len(result['result']['results']) == 10
        for i in range(10):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activeInProductPrice_activate(self):
        '''
        <Get_List>Kiểm tra response khi activeInProductPrice = active
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice='active')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops where active_in_product_price = 1 order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activeInProductPrice_inactivate(self):
        '''
        <Get_List>Kiểm tra response khi activeInProductPrice = inactive
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice='inactive')
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops where active_in_product_price = 0 order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activeInProductPrice_different(self):
        '''
        <Get_List>Kiểm tra response khi activeInProductPrice khác (all, activate, inactivate)
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice='alla')
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == '''{'activeInProductPrice': [ErrorDetail(string='\"alla\" is not a valid choice.', code='invalid_choice')]}'''

    def test_activeInProductPrice_int(self):
        '''
        <Get_List>Kiểm tra response khi activeInProductPrice = int
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice=12345)
        result = response.json()
        assert response.status_code == 400
        assert result['code'] == 'bad_request'
        assert result[
                   'message'] == '''{'activeInProductPrice': [ErrorDetail(string='\"12345\" is not a valid choice.', code='invalid_choice')]}'''

    def test_pageSize_null(self):
        '''
        <Get_List>Kiểm tra response khi pageSize = null
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=None, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice=None)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result[
        #            'message'] == "{'pageSize': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_page_null(self):
        '''
        <Get_List>Kiểm tra response khi page = null
        Expect: Báo lỗi
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=None, q=None, orderBy=None, activate=None,
                                          activeInProductPrice=None)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result[
        #            'message'] == "{'page': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_q_null(self):
        '''
        <Get_List>Kiểm tra response khi q = null
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice=None)
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activate_null(self):
        '''
        <Get_List>Kiểm tra response khi activate = null
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice=None)
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_activeInProductPrice_null(self):
        '''
        <Get_List>Kiểm tra response khi activeInProductPrice = null
        Expect: status = 200
        :return:
        '''
        response = self.call_api_get_list(pageSize=10, page=1, q=None, orderBy=None, activate=None,
                                          activeInProductPrice=None)
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_not_pageSize(self):
        '''
        <Get_List>Kiểm tra response khi không nhập pageSize
        Expect: Báo lỗi
        :return:
        '''
        params1 = {
            # 'pageSize' : 10,
            'page': 1,
            'q': 'test',
            'orderBy': 'name',
            'activate': 'all',
            'activeInProductPrice': 'all'
        }
        response = requests.get(url=url_list, params=params1)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result[
        #            'message'] == "{'pageSize': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_page(self):
        '''
        <Get_List>Kiểm tra response khi không nhập page
        Expect: Báo lỗi
        :return:
        '''
        params1 = {
            'pageSize': 10,
            # 'page':1,
            'q': 'test',
            'orderBy': 'name',
            'activate': 'all',
            'activeInProductPrice': 'all'
        }
        response = requests.get(url=url_list, params=params1)
        result = response.json()
        assert response.status_code == 200
        assert result['code'] == 'success'
        # assert result[
        #            'message'] == "{'page': [ErrorDetail(string='This field is required.', code='required')]}"

    def test_not_q(self):
        '''
        <Get_List>Kiểm tra response khi không nhập q
        Expect: status = 200
        :return:
        '''
        params1 = {
            'pageSize': 10,
            'page': 1,
            # 'q': None,
            'orderBy': None,
            'activate': 'all',
            'activeInProductPrice': 'all'
        }
        response = requests.get(url=url_list, params=params1)
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_not_activate(self):
        '''
        <Get_List>Kiểm tra response khi không nhập activate
        Expect: status = 200
        :return:
        '''
        params1 = {
            'pageSize': 10,
            'page': 1,
            'q': None,
            'orderBy': None,
            # 'activate': 'all',
            'activeInProductPrice': 'all'
        }
        response = requests.get(url=url_list, params=params1)
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_not_activeInProductPrice(self):
        '''
        <Get_List>Kiểm tra response khi không nhập activeInProductPrice
        Expect: status = 200
        :return:
        '''
        params1 = {
            'pageSize': 10,
            'page': 1,
            'q': None,
            'orderBy': None,
            'activate': 'all',
            # 'activeInProductPrice': 'all'
        }
        response = requests.get(url=url_list, params=params1)
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']

    def test_not_orderBy(self):
        '''
        <Get_List>Kiểm tra response khi không nhập orderBy
        Expect: status = 200
        :return:
        '''
        params1 = {
            'pageSize': 10,
            'page': 1,
            'q': None,
            # 'orderBy': None,
            'activate': 'all',
            'activeInProductPrice': 'all'
        }
        response = requests.get(url=url_list, params=params1)
        result = response.json()
        data = DbConnectMysql().get_data_all('select * FROM shops order by id desc ;')
        assert response.status_code == 200
        # assert len(result['result']['results']) == 10
        for i in range(len(result['result']['results'])):
            assert result['result']['results'][i]['id'] == data[i]['id']
            assert result['result']['results'][i]['name'] == data[i]['name']
            assert result['result']['results'][i]['domain'] == data[i]['domain']



