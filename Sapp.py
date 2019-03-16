# -*- coding: utf-8 -*-
import json
from io import BytesIO
from PIL import Image
import requests
import re
from bs4 import BeautifulSoup
import os
import scrapy
# [x for x in range(1)]

# 1. 印出所有頁面的 a 連結


def links_compile():
    arr = []
    for i in range(20):
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

if os.path.exists("res.json"):
    os.remove("res.json")


class richardSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = [All_innerPage_Links[0]]

    def parse(self, response):
        yield{
            'imgUrl': response.url,
            'imgSrc': response.css('.vodBox img::attr("src")').get(),
            'imgTitle': response.css('.vodBox img::attr("alt")').get(),
            'infoName': [response.css('.vodinfobox ul li')[0].xpath('text()').get(), response.css('.vodinfobox ul li')[0].xpath('span/text()').get()],
            'infoAuth': [response.css('.vodinfobox ul li')[1].xpath('text()').get(), response.css('.vodinfobox ul li')[1].xpath('span/text()').get()],
            'infoActor': [response.css('.vodinfobox ul li')[2].xpath('text()').get(), response.css('.vodinfobox ul li')[2].xpath('span/text()').get()],
            'infoType': [response.css('.vodinfobox ul li')[3].xpath('text()').get(), response.css('.vodinfobox ul li')[3].xpath('span/text()').get()],
            'infoArea': [response.css('.vodinfobox ul li')[4].xpath('text()').get(), response.css('.vodinfobox ul li')[4].xpath('span/text()').get()],
            'infoLang': [response.css('.vodinfobox ul li')[5].xpath('text()').get(), response.css('.vodinfobox ul li')[5].xpath('span/text()').get()],
            'infoRelease': [response.css('.vodinfobox ul li')[6].xpath('text()').get(), response.css('.vodinfobox ul li')[6].xpath('span/text()').get()],
            'infoUpdate': [response.css('.vodinfobox ul li')[7].xpath('text()').get(), response.css('.vodinfobox ul li')[7].xpath('span/text()').get()]
        }
        for next_page in All_innerPage_Links:
            yield response.follow(next_page, self.parse)
