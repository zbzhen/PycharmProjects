#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 10:22
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 键盘操作.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np


def on_key_press(event):
    if event.key in 'rgbcmyk':
        line.set_color(event.key)
    fig.canvas.draw_idle()#重新绘制整个图表，



fig, ax = plt.subplots()
x = np.linspace(0, 10, 1000)
y = np.sin(x)
line = ax.plot(x, y)[0]

fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)#取消默认快捷键的注册
fig.canvas.mpl_connect('key_press_event', on_key_press)
plt.show()

