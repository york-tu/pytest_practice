import codecs
import re

import requests
"""
0. KKBOX app:
        KKBOXAPITest
            Name
                KKBOXAPITest
            Description
                PythonAPITest
            ID
                c8f4a496d98e2708f28ad06c2814bf3e
            Secret
                2282b6eacea5b9c1327f7a959ff80c82
1. 詳細說明參考:
        a. https://docs-en.kkbox.codes/docs#overview--create-application-credentials
        b. https://www.learncodewithmike.com/2020/02/python-kkbox-open-api.html
"""


# 取得Token
def get_access_token():
    """
    KKBOX Authorization Server: The server for authorizing an application or a user.
    For OAuth 2.0 authorization, the URL will be https://account.kkbox.com/oauth2/token.
    """
    # API網址 (KKBOX Authorization Server)
    url = 'https://account.kkbox.com/oauth2/token'

    # 標題
    headers = {
        "Host": "account.kkbox.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 參數
    data = {
        "grant_type": "client_credentials",
        "client_id": "c8f4a496d98e2708f28ad06c2814bf3e",
        "client_secret": "2282b6eacea5b9c1327f7a959ff80c82"
    }

    access_token = requests.post(url, headers=headers, data=data)
    return access_token.json()["access_token"]


territory = "JP"  # territory可選區域: HK(香港), JP(日本), MY(馬來西亞), SG(新加坡), TW(台灣)


# 取得各種音樂排行榜列表
def get_chart_playlists():
    """
    GET /v1.1/charts?territory=TW
    Authorization: Bearer my_access_token
    Host: api.kkbox.com
    API Server: https://api.kkbox.com/v1.1
    """

    url =f"https://api.kkbox.com/v1.1/charts?territory={territory}"
    access_token = get_access_token()
    headers = {
        'accept': "application/json",
        "authorization": "Bearer " + access_token  #帶著存取憑證
        }
    response = requests.get(url, headers=headers)
    result = response.json()["data"]
    title_id_list=[]
    i = 0
    for item in result:
        each_item =[]
        print(i, item["title"], item["url"])
        each_item.append(i)
        each_item.append(item["id"])
        each_item.append(item["title"])
        title_id_list.append(each_item)
        i += 1
    return title_id_list


# 取得指定專輯裡的歌曲列表
def get_tracks_of_a_chart_playlist():
    """
    GET /charts/{playlist_id}/tracks
    Authorization: Bearer my_access_token
    Host: api.kkbox.com
    API Server: https://api.kkbox.com/v1.1
    """
    track_id_list = get_chart_playlists()
    list_lenght= len(track_id_list)
    flag = True
    # 當輸入非數字 & 專輯index不在音樂排行榜列表列表中 >>> 重新輸入直到符合預期
    while flag:
        user_select_index = input("請選擇專輯: ")
        if re.match(r'^\d+$',user_select_index) and 0 <= int(user_select_index) <= list_lenght-1:
            flag=False
        else:
            print("輸入有誤, 重新輸入")
    url = f'https://api.kkbox.com/v1.1/charts/{track_id_list[int(user_select_index)][1]}/tracks/?territory={territory}'
    access_token = get_access_token()
    headers = {
        'accept': "application/json",
        "authorization": "Bearer " + access_token  # 帶著存取憑證
    }
    response = requests.get(url, headers=headers)
    result = response.json()["data"]
    i =0
    for item in result:
        print(i, item['name'],item['url'])
        i+=1



get_tracks_of_a_chart_playlist()