import json
import os

import requests

from support.db.db_connection import DbConnect
from settings import db_connection_test1, PCR_URL_TEST1, BASE_DIR
import pytest
from support.Excel2Json import create_data_json_pcr_54, create_data_json_pcr_54_1
from support.schema import get_api_schema, validate

db = DbConnect(db_connection_test1)
data = create_data_json_pcr_54()
data1 = create_data_json_pcr_54_1()
url = PCR_URL_TEST1 + 'product-suggestions/'
url1 = PCR_URL_TEST1 + 'product-suggestions'

SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')
class TestPCR54:
    ISSUE_KEY = 'PCR-54'
    FOLDER = "/QC/API/PATCH-PCR54"

    @pytest.mark.parametrize('des, data, expect, code, suggestion_id ', data)
    def test_checklist(self, des, data, expect, code, suggestion_id):
        f'''
        '{des}'
        :param data:
        :param expect:
        :param code:
        :return:
        '''
        _payload = data
        # print(json.dumps(_payload))
        id=db.get_one_data(suggestion_id)
        response = requests.patch(url=url+str(id['id']), json=_payload)
        result = response.json()
        print(result)
        assert response.status_code == expect
        assert result['code'] == code
    def test_suggestion_id_not_exist(self):
        '''
        Kiểm tra response khi suggestion_id không tồn tại
        Step by step:
        Expect: status_code = 404
        :return:
        '''
        payload = {
            'state':'PENDING'
        }
        response = requests.patch(url=url + 'dfgh678', json=payload)
        # result = response.json()
        # print(result)
        assert response.status_code == 404
        # assert result['code'] == 'record_does_not_exist'

    def test_state_not_exist(self):
        '''
        Kiểm tra response khi state không tồn tại
        Step by step:
        Expect: status_code = 400
        :return:
        '''
        payload = {
            'state':'PENDINGs'
        }
        response = requests.patch(url=url + '678', json=payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_not_state(self):
        '''
        Kiểm tra response khi state không tồn tại
        Step by step:
        Expect: status_code = 400
        :return:
        '''
        payload = {
        }
        response = requests.patch(url=url + '678', json=payload)
        result = response.json()
        print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_not_suggestion_id(self):
        '''
        Kiểm tra response khi suggestion_id không tồn tại
        Step by step:
        Expect: status_code = 404
        :return:
        '''
        payload = {
            'state':'PENDING'
        }
        response = requests.patch(url=url, json=payload)
        # result = response.json()
        # print(result)
        assert response.status_code == 404
        # assert result['code'] == 'bad_request'
    def test_veryfi_response(self):
        '''
        Kiểm tra schema của response trả về khi các field valid
        :return:
        '''
        payload = {
            'state': 'APPROVED'
        }
        id=db.get_one_data("select id from matching_suggestions where state = 'PENDING';")
        response = requests.patch(url=url + str(id['id']), json=payload)
        result = response.json()
        print(result)
        assert response.status_code == 200
        # assert result['code'] == 'record_does_not_exist'
        api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_patch_suggestion_success'))
        is_valid, message, error_path = validate(result, api_schema)
        assert is_valid, (error_path + ': ' + message)

    @pytest.mark.parametrize('des, data, expect, code, suggestion_id ', data1)
    def test_checklist_all(self, des, data, expect, code, suggestion_id):
        f'''
           '{des}'
           :param data:
           :param expect:
           :param code:
           :return:
           '''
        _payload = data
        # print(json.dumps(_payload))
        id = db.get_all_data(suggestion_id)
        list_ids = [id[i]['id'] for i in range(len(id))]
        # print(list_ids)
        # print(type(list_ids))
        _payload['suggestionIds'] = list_ids
        # print(_payload)

        response = requests.patch(url=url1, json=_payload)
        result = response.json()
        print(result)
        assert response.status_code == expect
        assert result['code'] == code

    def test_not_state1(self):
        '''
        Kiểm tra response api update nhiều khi state không tồn tại
        Step by step:
        Expect: status_code = 400
        :return:
        '''
        payload = {
            'suggestionIds':[1,2,3,4,5,6,7]
        }
        response = requests.patch(url=url1 , json=payload)
        result = response.json()
        # print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_not_suggestion_id1(self):
        '''
        Kiểm tra response api update nhiều khi suggestion_id không tồn tại
        Step by step:
        Expect: status_code = 400
        :return:
        '''
        payload = {

            'state': 'PENDING',
            # 'suggestionIds': [1234567890, 21234567890, 3123456789, 4, 5, 6, 7]
        }
        response = requests.patch(url=url1, json=payload)
        result = response.json()
        # print(result)
        assert response.status_code == 400
        assert result['code'] == 'bad_request'

    def test_suggestion_id_not_exist(self):
        '''
        Kiểm tra response api update nhiều khi suggestion_id không tồn tại
        Step by step:
        Expect: status_code = 400
        :return:
        '''
        payload = {

            'state': 'PENDING',
            'suggestionIds': [1234567890, 21234567890, 3123456789, 4, 5, 6, 7]
        }
        response = requests.patch(url=url1, json=payload)
        result = response.json()
        # print(result)
        assert response.status_code == 400
        assert result['code'] == 'suggestion_list_id_is_not_valid'

    def test_veryfi_response1(self):
        '''
        Kiểm tra schema của response api update nhiều records khi các field valid
        :return:
        '''
        payload = {
            'state': 'APPROVED'
        }
        id = db.get_all_data("select id from matching_suggestions where state = 'PENDING' limit 100;")
        # print(id)
        list_ids = [id[i]['id'] for i in range(len(id))]
        print(list_ids)
        print(type(list_ids))
        payload['suggestionIds'] = list_ids
        response = requests.patch(url=url1, json=payload)
        result = response.json()
        print(json.dumps(result))
        assert response.status_code == 200
        # assert result['code'] == 'record_does_not_exist'
        api_schema = get_api_schema(os.path.join(SCHEMA_BASE_URL, 'response_patch_all_suggestion_success'))
        is_valid, message, error_path = validate(result, api_schema)
        assert is_valid, (error_path + ': ' + message)



