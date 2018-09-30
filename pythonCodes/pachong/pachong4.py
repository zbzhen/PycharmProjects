#!/usr/bin/env python
# encoding: utf-8
import urllib
#导入request
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

html = getHtml('http://imgsrc.baidu.com/forum/w%3D580/sign=294db374d462853592e0d229a0ee76f2/e732c895d143ad4b630e8f4683025aafa40f0611.jpg')
#打卡这个网址
#读取图片
with open('img.jpg','wb') as f:
    f.write(html)
    f.close()
#创建并保存关闭文件