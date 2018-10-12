#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/5 11:30
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 对勾函数.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex, var, pi
x = var('x')

import imageio
import os
fig_mpl, ax = plt.subplots(1,figsize=(8,8), facecolor='white')
ax.axis('off')
ax.set_xlim(-7,7)
ax.set_ylim(-7,7)
h = 0.05
# plt.annotate("",(1.4,0),(-1.4,0), arrowprops={"arrowstyle": "->"},color="black")

ax.arrow(-6, 0, 12, 0, head_width=0.3, head_length=0.3, fc='k', ec='k', overhang=0.8, lw=2)
ax.arrow(0, -6, 0, 12, head_width=0.3, head_length=0.3, fc='k', ec='k', overhang=0.8, lw=2)


# ax.arrow(0,-0.3, 0.5, 0, head_width=0.08, head_length=0.1, fc='k', ec='k', overhang=0.8)
# ax.arrow(0,-0.5, 0.5, 0, head_width=0.08, head_length=0.1, fc='k', ec='k', overhang=0)
# ax.arrow(0,-0.7, 0.5, 0, head_width=0.08, head_length=0.2, fc='k', ec='k', overhang=0)
# ax.arrow(0,-0.9, 0.5, 0, head_width=0.08, head_length=0.2, fc='k', ec='k', overhang=0.7,shape='right')
# ax.arrow(0,-1.1, 0.5, 0, head_width=0.08, head_length=0.1, fc='k', ec='k', overhang=1,lw=2)

# plt.annotate("",(0,1.4),(0,-1.4), arrowprops={"arrowstyle": "->"},color="black")
plt.text(6, 0,r'$x$', color="black", fontsize=30, va='top', ha='left')
plt.text(0+h, 6,r'$y$', color="black", fontsize=30, va='center', ha='left')

plt.text(1, 6,r'$f(x) = x + \frac{1}{x}$', color="blue", fontsize=40, va='center', ha='left')

# xticks = [-1, -0.5, 1.0/2.0, 1]  # 这个是设置x刻度
# yticks = [-pi/3, -pi/6, pi/6, pi/3]  # 这个是设置y刻度
# # 下面的两个for循环不要动
# for i in range(len(xticks)):
#     plt.plot([xticks[i],xticks[i]], [0,h],"k")
#     tex = '$'+latex(xticks[i])+'$'
#     plt.text(xticks[i], 0-h, tex, color="black", fontsize=20, ha="center", verticalalignment='top')
# for i in range(len(yticks)):
#     plt.plot([0,h], [yticks[i],yticks[i]],"k")
#     tex = '$'+latex(yticks[i])+'$'
#     plt.text(0-h, yticks[i], tex, color="black", fontsize=20, verticalalignment='center', horizontalalignment='right')

plt.text(0.5*h, 0-h, latex(0, mode='inline'), color="black", fontsize=20, ha="center", verticalalignment='top', horizontalalignment='left')

# xx = np.linspace(-1.3, 1.3, 100)  # the x vector
# yy = xx*xx
# yy = xx
# yy = np.sqrt(xx*xx)
xx = np.linspace(0.2, 5, 100)
yy = 1.0/xx + xx
plt.plot(xx, yy, lw=3, color="blue")

xx = np.linspace(-0.2, -5, 100)
yy = 1.0/xx + xx
plt.plot(xx, yy, lw=3, color="blue")

plt.plot([1,1], [0,2], "--", lw=2, color="g")
plt.text(1, 0-h, r"1", color="black", fontsize=25, ha="center", va="top")

plt.plot([0, 1], [2, 2], "--", lw=2, color="g")
plt.text(0-h, 2, r"2", color="black", fontsize=25, ha="right", va="center")



# 绘制渐近线
plt.plot([-5,5], [-5,5], "--", lw=2, color="red")
plt.text(2.5, 1.6,r'$y = x $', color="red", fontsize=40, va='center', ha='left')


plt.plot([1],[2], "ro", ms=10)
# plt.plot([0.2],[-1.1], "wo", ms=10)
# plt.plot([0.5,0.5],[0,0.5*0.5],"--")

# plt.text(0.5, 0.5*0.5,r'$(x,\, x^2\!)$', color="blue", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')
# plt.plot([0.5],[0.25], 'ro')
# plt.savefig("ercihanshu.png", dip=20)
# plt.savefig("yicihanshu.png", dip=20)
# plt.savefig("jueduizhi.png", dip=20)
plt.savefig("duigou.png", dip=20)
plt.show()