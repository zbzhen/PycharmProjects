#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: readpng
@time: 2018/5/16  14:18
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

plt.figure(dpi=100,facecolor="white")
axes = plt.subplot(111)
axes.set_xticks([])
axes.set_yticks([])
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['bottom'].set_color('none')
axes.spines['left'].set_color('none')

fig = mpimg.imread('111.png')
plt.imshow(fig)

plt.savefig("111.pdf")
plt.show()