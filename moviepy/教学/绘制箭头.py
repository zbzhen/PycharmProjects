#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 18:20
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 绘制箭头.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.axisartist as axisartist

plt.figure(1,figsize=(4,8))


xticks = np.linspace(-3,3,7)
plt.xticks(xticks)  #设置坐标点
yticks = np.linspace(-6,8,15)
plt.yticks(yticks)


#挪动坐标位置
ax = plt.gca()
#去掉边框
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
#移位置 设为原点相交
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
ax.set_xlim(-3.2, 3.2)
ax.set_ylim(-6.2, 7.2)
# plt.xlabel("x")
# plt.ylabel("y")
x = np.linspace(-3,3,50)
y = 2*x + 1
plt.plot(x,y)

x0 = 1
y0 = 2*x0 + 1
plt.plot([x0,x0,],[0,y0],'k--',linewidth=2.5)
plt.scatter([x0], [y0], s=50, color='r') #在这点加个蓝色的原点 原点大小50
plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30),
             textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))

plt.show()
