import json
from io import BytesIO
from PIL import Image
import requests
import re
from bs4 import BeautifulSoup

# [x for x in range(1)]

# 1. 印出所有頁面的 a 連結


def links_compile():
    arr = []
    for i in range(10):
        r = requests.get(
            'http://135zy.vip/?m=vod-index-pg-{}.html'.format(i+1))
        soup = BeautifulSoup(r.text)
        # 使用 keyword 參數，找出相關的 href
        links_compile = soup.find_all(href=re.compile("/?m=vod-detail-id"))
        arr.append(links_compile)
    return arr

# 2. 過濾所有連結，取得連結內的 id，並重組連結 http://135zy.vip/?m=vod-detail-id-19862.html


def pipe_links_id():
    kk = links_compile()
    dimension_list = ["http://135zy.vip" + y['href'] for x in kk for y in x]
    return dimension_list


All_innerPage_Links = pipe_links_id()
print(len(All_innerPage_Links))


def renderInfo():
    for i in All_innerPage_Links:
        r = requests.get(i)
        soup = BeautifulSoup(r.text)
        imgSrc = soup.select('.vodBox img')[0]['src']
        imgTitle = soup.select('.vodBox img')[0]['alt']
        infoName = soup.select('.vodinfobox ul li')[0]
        infoAuth = soup.select('.vodinfobox ul li')[1]
        infoActor = soup.select('.vodinfobox ul li')[2]
        infoType = soup.select('.vodinfobox ul li')[3]
        infoArea = soup.select('.vodinfobox ul li')[4]
        infoLang = soup.select('.vodinfobox ul li')[5]
        infoRelease = soup.select('.vodinfobox ul li')[6]
        infoUpdate = soup.select('.vodinfobox ul li')[7]
        yield {
            'imgUrl': str(r.url),
            'imgSrc': str(imgSrc),
            'imgTitle': str(imgTitle),
            'infoName': str(infoName),
            'infoAuth': str(infoAuth),
            'infoActor': str(infoActor),
            'infoType': str(infoType),
            'infoArea': str(infoArea),
            'infoLang': str(infoLang),
            'infoRelease': str(infoRelease),
            'infoUpdate': str(infoUpdate),
        }


infoDatas = renderInfo()

datas = []
for x in infoDatas:
    datas.append(x)


with open('data.json', 'w') as outfile:
    json.dump(datas, outfile)
