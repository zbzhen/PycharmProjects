#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: test
@time: 2018/6/6  19:08
"""
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
#
# plt.figure(dpi=600,facecolor="white")
# fig = mpimg.imread('tmp-0.png')
# plt.imshow(fig)
#
# plt.savefig("test1.jpg")

from PIL import Image



im = Image.open('tmp-0.png')
x, y = im.size
# 使用白色来填充背景 from：www.outofmemory.cn
# (alpha band as paste mask).
num = 16
p = Image.new('RGBA', (x, y*num), (255,255,255))
for i in range(num):
    im = Image.open('tmp-'+str(i)+'.png')
    p.paste(im, (0, i*y, x, (i+1)*y))
p.save('yy.png')

