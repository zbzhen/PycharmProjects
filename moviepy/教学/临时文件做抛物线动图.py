#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/25 21:28
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 临时文件做抛物线动图.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
xx = np.linspace(-1.2, 1.2, 50) # the x vector
zz = lambda t,xx: t*xx*xx # the (changing) z vector
pp = lambda t: t*0.6*0.6


filename = "tmp.png"
images = []
for i in range(10):
    # 下面的一大段代码是绘制直角坐标的标准代码
    fig_mpl, ax = plt.subplots(1,figsize=(8,8), facecolor='white')
    ax.axis('off')
    ax.set_xlim(-1.5,1.5)
    ax.set_ylim(-1.5,1.5)
    plt.annotate("",(1.4,0),(-1.4,0), arrowprops={"arrowstyle": "->"},color="black")
    plt.annotate("",(0,1.4),(0,-1.4), arrowprops={"arrowstyle": "->"},color="black")
    plt.text(1.4, 0,r'$x$', color="black", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='right')
    plt.text(0, 1.4,r'$y$', color="black", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')
    plt.text(0, 0,r'$0$', color="black", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')
    plt.text(-1, 0,u'你好', color="black", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')



    t = 0.2*i
    plt.plot(xx, zz(t, xx), lw=1, color="blue")


    plt.plot(0.6, pp(t), 'ro')
    plt.text(0.6, pp(t), r'$(x, \,ax^2\!)$', color="r", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')


    plt.savefig(filename, dip=20)  # dip表示图片的质量，数值越大图片质量越高
    images.append(imageio.imread(filename))



imageio.mimsave('gif.gif', images, duration=0.2)
if os.path.exists(filename):
    os.remove(filename)
# plt.show()