import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import json
from lxml import etree
import re

def get_image_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    image_urls = []
    for img in img_tags:
        if 'src' in img.attrs:  # 检查是否有src属性
            image_urls.append(img.get('src'))
    print(image_urls)
    return image_urls


def get_music_name(url):
    response = requests.get(url)
    response = json.loads(response.text)
    extend = response['extend']
    html = etree.tostring(element_or_tree=etree.HTML(extend['html']), encoding='utf-8').decode('utf-8')
    content = list(filter(lambda x: x, re.findall('>(.*?)<', html)))
    print(content)
    music_name = str(content)  # music_name = content[0][1:-1]
    start_index = music_name.find("《")
    end_index = music_name.find("》")
    music_name = music_name[start_index+1:end_index]
    music_name = music_name.replace("'","")
    music_name = music_name.replace(",","")
    music_name = music_name.replace(" ","")
    print(music_name)
    return music_name


sid_list = range(180,221)  # +108
excluded_numbers = []
sid_result=[num for num in sid_list if num not in excluded_numbers]
for sid in sid_result:
    url = 'http://47.93.2.237:8080/user/getHtml?sid='
    url = url + str(sid)
    image_urls = get_image_urls(url)[0]
    image_urls = str(image_urls)
    image_urls = image_urls.replace('"', '')
    image_urls = image_urls.replace('\\', '')
    print(image_urls)  # 输出图片URL列表
    path = 'E:/pythonProject/folkmusic/lyrics_pic/酸曲'
    music_name = str(get_music_name(url)) + '.jpg'
    print("music name is " + music_name)
    response = requests.get(image_urls)
    with open(os.path.join(path, music_name), 'wb') as f:
        f.write(response.content)
        print("--------------------"+str(sid)+"----------------------"+music_name + " is finished")
