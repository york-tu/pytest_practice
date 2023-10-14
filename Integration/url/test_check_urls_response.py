import datetime
import os
import pytest
import requests
import openpyxl
import openpyxl.worksheet.worksheet
import query_urls

# 執行query_urls.export_urls(), 過濾sitemap內資料, 擷取URL, excel內對應之工作表下
query_urls.export_urls()
'''
工作表sheet_index對應網址
sheet_index  0:      "/personal",
sheet_index  1:      "/personal/deposit",
sheet_index  2:      "/personal/loan", 
sheet_index  3:      "/personal/credit-card",
sheet_index  4:      "/personal/wealth", 
sheet_index  5:      "/personal/trust", 
sheet_index  6:      "/personal/insurance",
sheet_index  7:      "/personal/lifefin", 
sheet_index  8:      "/personal/apply", 
sheet_index  9:      "/personal/event",
sheet_index  10:     "/small-business", 
sheet_index  11:     "/corporate", 
sheet_index  12:     "/digital", 
sheet_index  13:     "/about", 
sheet_index  14:     "/marketing"3,
sheet_index  15:     "/iframe/widget", 
sheet_index  16:     "/error", 
sheet_index  17:     "/bank-en",
sheet_index  18:     "/preview";
'''

test_sheet = [ [16, 19]]


@pytest.mark.parametrize("start_sheet_index, end_sheet_index", test_sheet)
# @pytest.mark.xfail
def test_check_url_response(start_sheet_index, end_sheet_index):
    # 獲取_testdata 資料夾內 sitemap_export_Urls_list檔的絕對路徑
    excel_file_path = f'{get_mainpy_directory_path()}\\_testdata\\sitemap_export_Urls_list_{str(datetime.date.today())}.xlsx'
    excel_wb = openpyxl.load_workbook(excel_file_path)

    # 遍歷指定範圍內的工作表
    for sheet_index in range(start_sheet_index, end_sheet_index):
        sheet_name = excel_wb.sheetnames[sheet_index]

        print(f'工作表名稱: {sheet_name}')
        i = 1
        flag = False
        for row in excel_wb[sheet_name]:
            for cell in row:
                # 獲取指定工作表內指定行數下之資料 = url
                url = cell.value
                try:
                    response = requests.get(url, allow_redirects=False, timeout=30)
                    if response.status_code == 200:
                        print(f'<span style="color: green;">URL_{i}: {url} ==> Response: {response.status_code}</span>')
                        i += 1
                    else:
                        if response.is_redirect:
                            print(
                                f'<span style="color: orange;">URL_{i}: {url} ==> Redirect_to: {response.url}</span>')
                            i += 1
                            break
                        print(
                            f'<span style="color: brown;">URL_{i}: {url} ==> Response: {response.status_code}, Reason: {response.reason}</span>')
                        flag = True
                        i += 1
                except requests.exceptions.RequestException as e:
                    print(f'<span style="color: red;">URL_{i}: {url} ==> [異常] {e}</span>')
                    flag = True
                    i += 1
        # report內資料換行用
        print('')
        # 判斷當flag變為true ==> 代表迴圈進入response非200與非redirect的判斷式中, 即網頁結果非預期 ==> fail
        if flag:
            pytest.fail()
    excel_wb.close()


def get_mainpy_directory_path():
    # 获取当前脚本文件的绝对路径
    current_script_path = os.path.abspath(__file__)
    # 获取当前脚本文件所在目录的路径
    script_directory = os.path.dirname(current_script_path)
    # 获取 main.py 同一层目录的路径
    parent_directory = os.path.dirname(script_directory)
    return os.path.dirname(parent_directory)
