import requests
import json
from lxml import etree
import re
from pymongo import MongoClient
# django(re),flask(轻量)(http服务器)（需要自己配置）,tournado(多并发)

url='http://47.93.2.237:8080/user/getHtml?sid='

i = 1
sid_list = range(180,221)  # +108
excluded_numbers = []
sid_result=[num for num in sid_list if num not in excluded_numbers]
sid_result = [108]
for sid in sid_result:
    sid=str(sid)
    response = requests.get(url=url + sid)

    response = json.loads(response.text)

    extend = response['extend']

    html = etree.tostring(element_or_tree=etree.HTML(extend['html']), encoding='utf-8').decode('utf-8')

    content = list(filter(lambda x: x, re.findall('>(.*?)<', html)))
    print(content)
    music_name = content  # music_name = content[0]
    music_name = str(content)  # music_name = music_name[1:-1]
    start_index = music_name.find("《")
    end_index = music_name.find("》")
    music_name = music_name[start_index + 1:end_index]
    music_name = music_name.replace("'","")
    music_name = music_name.replace(",","")
    music_name = music_name.replace(" ","")
    print('music_name:', music_name)

    if '歌曲介绍：' in content:
        mbId = content.index('歌曲介绍：')
    else:
        mbId = content.index('歌曲介绍')

    if '演唱者：' in content:
       singerId = content.index('演唱者：')
    else:
        singerId = content.index('演唱者')
    #  singerId = content.index('演唱者：')
    music_briefs = content[mbId + 1:singerId]
    result_music_briefs = ''.join(music_briefs)
    result_music_briefs = result_music_briefs.replace("：","")
    print('music_briefs:', music_briefs)
    print(result_music_briefs)

    singer_name = re.split(',|，', content[singerId + 1], 1)
    singer_name = singer_name[0]
    print('singer_name:', singer_name)

    sbId = content.index('艺术履历：')
    singer_briefs = content[singerId + 1:sbId]
    print('singer_briefs:', singer_briefs)
    result_singer_briefs = ''.join(singer_briefs)
    print(result_singer_briefs)

    singer_prizes = content[sbId + 1:-1]
    print('singer_prizes:', singer_prizes)

    client = MongoClient('mongodb://localhost:27017/')
    print(client.list_database_names())
    db = client['folkmusicdb']
    collection = db['music']

    music_id=42110282+i
    i=i+1

    mu = {
        "music_detail":
             {"music_id": music_id, "music_name": music_name, "music_brief": result_music_briefs,"music_type":["酸曲"]},
        "singer_detail":
             {"singer_name": singer_name, "singer_brief": result_singer_briefs, "singer_prize": singer_prizes}
    }

    try:
        result = collection.insert_one(mu)
        print("输入成功")
    except Exception as e:
        print(f"发生错误:{e}")
