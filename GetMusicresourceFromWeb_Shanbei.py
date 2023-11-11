# -*- coding: utf-8 -*-
import requests
import os
import re
from bs4 import BeautifulSoup
import json
import pandas as pd

# 在详情页爬取文本内容
url = "http://47.93.2.237:8080/user/getSongById?sid="  # http://47.93.2.237:8080/user/getHtml?sid=155
folder_path = r"E:\pythonProject\folkmusic\革命"
sid_list = range(118,161,)
excluded_numbers=[119,120,131,137152,154,155,156,157,158,159]
sid_result=[num for num in sid_list if num  not in excluded_numbers]
for sid in sid_result:
    sid = str(sid)
    try:
        wb_data = requests.get(url + sid, stream=True)
        wb_data_l = json.loads(wb_data.text).get('extend').get('song').get('wenUrl')
        print(wb_data_l)
        print(type(wb_data_l))
        filename = json.loads(wb_data.text).get('extend').get('song').get('wenName')
        print(filename)
        file_path = os.path.join(folder_path, filename+'.mp3')
        with open(file_path, 'wb') as file:
            response=requests.get(wb_data_l,stream=True)
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)



    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
