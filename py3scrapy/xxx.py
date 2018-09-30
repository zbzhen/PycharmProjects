#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/28 18:34
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : xxx.py
# @version : Python 2.7.6
import requests
from bs4 import BeautifulSoup
from PIL import Image
import os
from io import BytesIO
import time

url = "http://www.yestone.com/gallery/1501754333627"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
items = soup.find_all('img', class_='img-responsive')

folder_path = './photo'

if os.path.exists(folder_path) == False:
   os.makedirs(folder_path)

for index, item in enumerate(items):
    if item:
        html = requests.get(item.get('data-src'))
        img_name = folder_path + str(index + 1) + '.png'
        image = Image.open(BytesIO(html.content))
        image.save(img_name)
        print('第%d张图片下载完成' % (index + 1))
        time.sleep(1)  # 自定义延时
print('抓取完成')
df.to_excel('news.xlsx')