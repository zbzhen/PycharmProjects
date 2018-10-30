#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 20:45
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 鼠标简单拾取.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on points')

line, = ax.plot(np.random.rand(100), 'o', picker=5)  # 5 points tolerance

def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    points = tuple(zip(xdata[ind], ydata[ind]))
    print('onpick points:', xdata[ind][0], ydata[ind][0])

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()