import os
import xlrd
from settings import BASE_DIR
def create_data_test():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint1.xlsx'))
    sheet = wb.sheet_by_name('PCR-10 API tạo mới shop')
    data_user = list()
    for rownum in range(9, 28):
        row_value = sheet.row_values(rownum)
        Title = row_value[1]
        Expected = row_value[4]
        name = row_value[12]
        domain = row_value[13]
        activate = row_value[14]
        activateInProductPrice = row_value[15]
        code = row_value[16]
        message = row_value[17]
        data_user.append((Title, Expected, name, domain, bool(activate), bool(activateInProductPrice), code, message))
    # print(data_user)
    return data_user
def data_test_PCR_29_update():
    wb = xlrd.open_workbook(os.path.join(BASE_DIR, 'PCR_CheckList_Sprint1.xlsx'))
    sheet = wb.sheet_by_name('PCR-29 shop_update')
    data_user = list()
    for rownum in range(12, 33):
        row_value = sheet.row_values(rownum)
        Title = row_value[1]
        Expected = row_value[4]
        name = row_value[12]
        domain = row_value[13]
        status_code = row_value[14]
        code = row_value[15]
        message = row_value[16]
        data_user.append((Title, Expected, name, domain, int(status_code), code, message))
    # print(data_user)
    return data_user

