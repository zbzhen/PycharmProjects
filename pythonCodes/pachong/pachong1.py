#coding=utf-8
import urllib
import numpy as np
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

html = getHtml("http://placekitten.com/500/800")

#print html
with open("cat.jpg","w") as f:
    f.write(html)
