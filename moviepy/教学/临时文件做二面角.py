#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/25 22:03
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 临时文件做二面角.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

c1=np.array([-0.1, -0.5])
c2=np.array([0.3, 0.5])
r = 1.1
xx = lambda t:[r*np.cos(t)+c1[0], r*np.cos(t)+c2[0],  r*np.cos(t+np.pi)+c2[0], r*np.cos(t+np.pi)+c1[0], r*np.cos(t)+c1[0]]
yy = lambda t:[r*np.sin(t)+c1[1], r*np.sin(t)+c2[1],  r*np.sin(t+np.pi)+c2[1], r*np.sin(t+np.pi)+c1[1], r*np.sin(t)+c1[1]]

xt = lambda t:[r*np.cos(t)+c1[0], r*np.cos(t)+c2[0],  c2[0], c1[0], r*np.cos(t)+c1[0]]
yt = lambda t:[r*np.sin(t)+c1[1], r*np.sin(t)+c2[1],  c2[1], c1[1], r*np.sin(t)+c1[1]]

print xx(0)
print yy(0)
filename = "tmp.png"
images = []
num = 20
for i in range(0,num):
    # 下面的一大段代码是绘制直角坐标的标准代码
    fig_mpl, ax = plt.subplots(1,figsize=(8,8), facecolor='white')
    ax.axis('off')
    ax.set_xlim(-1.8,1.8)
    ax.set_ylim(-1.8,1.8)

    t = (1.0*i)/(1.0*num)*np.pi
    plt.plot([c1[0], c2[0]], [c1[1], c2[1]], "--")  # lw 就是线宽 line width
    plt.plot(xx(0), yy(0), lw=1, color="k")  # lw 就是线宽 line width
    plt.fill(xx(0), yy(0), 'r', alpha = 0.5)
    plt.fill(xt(t), yt(t), 'b', alpha = 0.5)

    # plt.show()
    plt.savefig(filename, dip=20)  # dip表示图片的质量，数值越大图片质量越高
    images.append(imageio.imread(filename))


imageio.mimsave('ermianjiao.gif', images, duration=0.2)
if os.path.exists(filename):
    os.remove(filename)
