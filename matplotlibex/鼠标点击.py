#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 10:20
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 鼠标点击.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,RadioButtons

fig, ax = plt.subplots()
text = ax.text(0.5, 0.5, 'event', ha='center', va='center', fontdict={'size': 20})
A, = plt.plot(0.5,0.5,'bo')
print A
def call_back(event):
    info = 'name:{}\n button:{}\n x,y:{},{}\n xdata,ydata:{}{}'.format(event.name, event.button,event.x, event.y,event.xdata, event.ydata)
    text.set_text(info)
    A.set_xdata(event.xdata)
    A.set_ydata(event.ydata)
    text.set_x(event.xdata)
    text.set_y(event.ydata)
    fig.canvas.draw_idle()

# fig.canvas.mpl_connect('button_press_event', call_back)
# fig.canvas.mpl_connect('button_release_event', call_back)

class Para:
    p = 0
    r = 0
    m = 0



def main():
    Para.p += 1
    def event(s):
        fig.canvas.mpl_connect(s, call_back)
        return s
    s = event('motion_notify_event')

    return
main()


plt.show()