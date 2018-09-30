#coding=utf-8
import urllib
import re
import os
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html, ss):
    reg = r'src="(.+?\.(jpg|jpeg|gif|eps|pdf|png))" pic_ext'#这个只是抓大图
    reg = r'src="(.+?\.jpg)" pic_ext'#这个只是抓大图
    #reg = r'src="(http://imgsrc.*?\.jpg)"'#这个会抓取小图片
    #reg = 'src="([^ >]+\.(?:jpeg|jpg))"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    print len(imglist)
    x = 0
    newdir = str('figs_')+ss[-3:]
    if not os.path.exists(newdir):
        os.mkdir(newdir)
    for imgurl in imglist:
        local = os.path.join('.//'+str(newdir)+'//%s.jpg' % x)
        urllib.urlretrieve(imgurl, local)
        x+=1
    return x

ss = "http://tieba.baidu.com/p/2460150866"
#ss = "http://placekitten.com/500/800"

html = getHtml(ss)
#print html
print getImg(html, ss)