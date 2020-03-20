import datetime
import json
import os
import random
import xlrd
from collections import OrderedDict
from settings import BASE_DIR
from datetime import datetime

def create_data_json_pcr_39():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_5.xlsx'))
    sheet = wb.sheet_by_name('PCR-39 API Create schedule')
    payload = []
    Expect = list()

    for rownum in range(1, 21):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        expect = row_value[11]
        code = row_value[12]
        descripton = row_value[2]
        user['crawlType'] = row_value[5]
        user['scheduleName'] = row_value[6]
        user['scheduleSettings'] = row_value[7]
        user['scheduleType'] = row_value[8]
        date = int(row_value[9]) if isinstance(row_value[9], float) else datetime.now().strftime('%Y-%m-%d')
        if isinstance(date, str):
            user['startDate'] = date
        else:
            user['startDate'] = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + date - 2).strftime('%Y-%m-%d')
        user['scheduleTime'] = row_value[10]
        user['activate'] = random.choice([True, False])
        payload.append(user)
        Expect.append((user ,int(expect), code, descripton))

    return Expect
def create_data_json_pcr_39():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_5.xlsx'))
    sheet = wb.sheet_by_name('PCR-39 API Create schedule')
    payload = []
    Expect = list()

    for rownum in range(1, 21):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        expect = row_value[11]
        code = row_value[12]
        descripton = row_value[2]
        user['crawlType'] = row_value[5]
        user['scheduleName'] = row_value[6]
        user['scheduleSettings'] = row_value[7]
        user['scheduleType'] = row_value[8]
        date = int(row_value[9]) if isinstance(row_value[9], float) else datetime.now().strftime('%Y-%m-%d')
        if isinstance(date, str):
            user['startDate'] = date
        else:
            user['startDate'] = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + date - 2).strftime('%Y-%m-%d')
        user['scheduleTime'] = row_value[10]
        user['activate'] = random.choice([True, False])
        payload.append(user)
        Expect.append((user ,int(expect), code, descripton))

    return Expect
def create_data_json_pcr_39_2():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_5.xlsx'))
    sheet = wb.sheet_by_name('PCR-39 API Create schedule')
    payload = []

    for rownum in range(21, 58):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        user['crawlType'] = row_value[5]
        user['scheduleName'] = row_value[6]
        user['scheduleSettings'] = row_value[7]
        user['scheduleType'] = row_value[8]
        date = int(row_value[9]) if isinstance(row_value[9], float) else datetime.now().strftime('%Y-%m-%d')
        if isinstance(date, str):
            user['startDate'] = date
        else:
            user['startDate'] = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + date - 2).strftime('%Y-%m-%d')
        user['scheduleTime'] = row_value[10]
        user['activate'] = random.choice([True, False])
        payload.append(user)

    return payload
def create_data_json_pcr_53():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('API-POST_product-suggestions')
    payload = []
    Expect = list()

    for rownum in range(1, 53):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[11]
        code = row_value[12]
        user['pageSize'] = row_value[1]
        user['page'] = row_value[2]
        user['state'] = row_value[3]
        user['name'] = row_value[4]
        user['brand'] = row_value[5]
        user['shopIds'] = row_value[6]
        user['categoryIds'] = row_value[7]
        user['orderBy'] = row_value[8]
        user['skus'] = row_value[9]
        user['sellerId'] = row_value[10]

        payload.append(user)
        Expect.append((des, user ,int(expect), code))

    return Expect

def create_data_json_pcr_53_2():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('API-POST_product-suggestions')
    payload = []
    # Expect = list()

    for rownum in range(1, 2):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        # des = row_value[0]
        expect = row_value[11]
        code = row_value[12]
        user['pageSize'] = row_value[1]
        user['page'] = row_value[2]
        user['state'] = row_value[3]
        user['name'] = row_value[4]
        user['brand'] = row_value[5]
        user['shopIds'] = row_value[6]
        user['categoryIds'] = row_value[7]
        user['orderBy'] = row_value[8]
        user['skus'] = row_value[9]
        user['sellerId'] = int(row_value[10])

        payload.append(user)
        # Expect.append(( user ,int(expect), code))

    return payload

def create_data_json_pcr_54():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('API-PATCH_ONE-product_suggestio')
    payload = []
    Expect = list()

    for rownum in range(1, 17):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[3]
        code = row_value[4]
        user['state'] = row_value[1]
        suggestion_id = row_value[2]
        payload.append(user)
        Expect.append((des, user ,int(expect), code, suggestion_id))

    return Expect

def create_data_json_pcr_54_1():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('API-PATCH_ALL-product_suggestio')
    payload = []
    Expect = list()

    for rownum in range(1, 17):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[3]
        code = row_value[4]
        user['state'] = row_value[1]
        suggestion_id = row_value[2]
        payload.append(user)
        Expect.append((des, user ,int(expect), code, suggestion_id))

    return Expect
def create_data_json_pcr_79():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('Schedulers Create')
    payload = []
    Expect = list()

    for rownum in range(1, 69):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[10]
        code = row_value[11]
        user['name'] = row_value[1]
        user['taskId'] = row_value[2]
        user['sellerId'] = row_value[3]
        user['active'] = row_value[4]
        user['settings'] = row_value[5]
        user['scheduleType'] = row_value[6]
        # user['startDate'] = row_value[7]
        date = int(row_value[7]) if isinstance(row_value[7], float) else datetime.now().strftime('%d-%m-%Y')
        if isinstance(date, str):
            user['startDate'] = date
        else:
            user['startDate'] = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + date - 2).strftime('%d-%m-%Y')
        user['scheduleTime'] = row_value[8]
        user['variables'] = row_value[9]
        payload.append(user)
        Expect.append((des, user ,int(expect), code))

    return Expect

def create_data_json_pcr_78():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('Schedulers List')
    payload = []
    Expect = list()

    for rownum in range(1, 34):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[7]
        code = row_value[8]
        pageSize = int(row_value[1]) if isinstance(row_value[1], float) else row_value[1]
        user['pageSize'] = pageSize
        page = int(row_value[2]) if isinstance(row_value[2], float) else row_value[2]
        user['page'] = page
        user['searchText'] = row_value[3]
        user['active'] = row_value[4]
        sellerId = int(row_value[5]) if isinstance(row_value[5], float) else row_value[5]
        user['sellerId'] = sellerId
        user['variables'] = row_value[6]
        payload.append(user)
        Expect.append((des, user ,int(expect), code))

    return Expect

def create_data_json_pcr_84():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('Filter task')
    payload = []
    Expect = list()

    for rownum in range(1, 11):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[3]
        code = row_value[4]
        user['type'] = row_value[1]
        user['active'] = row_value[2]
        payload.append(user)
        Expect.append((des, user ,int(expect), code))

    return Expect

def create_data_json_pcr_99():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_6.xlsx'))
    sheet = wb.sheet_by_name('Send report now')
    payload = []
    Expect = list()

    for rownum in range(1, 44):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[5]
        code = row_value[6]
        user['name'] = row_value[1]
        taskId = int(row_value[2]) if isinstance(row_value[2], float) else row_value[2]
        user['taskId'] = taskId
        sellerId = int(row_value[3]) if isinstance(row_value[3], float) else row_value[3]
        user['sellerId'] = sellerId
        user['variables'] = row_value[4]
        payload.append(user)
        Expect.append((des, user ,int(expect), code))

    return Expect

def create_data_json_pcr_93():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint_7.xlsx'))
    sheet = wb.sheet_by_name('GET-List  brand')
    payload = []
    Expect = list()

    for rownum in range(1, 25):
        user = OrderedDict()
        row_value = sheet.row_values(rownum)
        des = row_value[0]
        expect = row_value[5]
        code = row_value[6]
        # user['pageSize'] = row_value[1]
        pageSize = int(row_value[1]) if isinstance(row_value[1], float) else row_value[1]
        user['pageSize'] = pageSize
        page = int(row_value[2]) if isinstance(row_value[2], float) else row_value[2]
        user['page'] = page
        user['q'] = str(row_value[3])
        shopId = int(row_value[4]) if isinstance(row_value[4], float) else row_value[4]
        user['shopId'] = shopId
        payload.append(user)
        Expect.append((des, user ,int(expect), code))

    return Expect


if __name__ == '__main__':
    data = create_data_json_pcr_79()
    _json = dict()
    _json= data[0][1]
    print(_json)
    print(type(_json))