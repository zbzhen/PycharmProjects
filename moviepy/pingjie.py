#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: pingjie
@time: 2018/5/4  21:02
"""
from os import listdir
from PIL import Image

imfiles = []
ims = []
for i in range(20):
    imfiles+=["sinc"+str(i)+".png"]
    ims += [Image.open(imfiles[i])]


w, h = ims[0].size
result = Image.new(ims[0].mode, (w, h*len(ims)))
for i, im in enumerate(ims):
    result.paste(im, box=(0, i*h))
result.save("result.png")



