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

# from pylab import *



plt.figure(dpi=100,facecolor="white")
axes = plt.subplot(111)
axes.set_xticks([])
axes.set_yticks([])
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['bottom'].set_color('none')
axes.spines['left'].set_color('none')

fig = mpimg.imread('test3.png')
plt.imshow(fig)

plt.rcParams['font.sans-serif'] = ['SimHei','FangSong','Kaiti'][-1]
plt.rcParams['axes.unicode_minus'] = False
plt.text(245, 413, u"您好", color="b", fontsize=20, rotation=-40)
# plt.text(245, 413, r"$K_1$", color="b", fontsize=20, rotation=-40)

plt.text(24, 176, r"$u_h^p|_{K_1}$", color="b", fontsize=20)
plt.text(374, 495, r"$K_2$", color="r", fontsize=24, rotation=-40)
plt.text(413, 344, r"$u_h^p|_{K_2}$", color="r", fontsize=24)

plt.annotate(r'$\widehat u_h^p|_{K_1\!\cap K_2}$',xy=(50,240),xytext=(10,372), fontsize=24,arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=-1.4"))



plt.savefig("test3.pdf")
plt.show()