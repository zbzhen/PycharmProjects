#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 16:42
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 分段函数模板.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex, var, pi

fig_mpl, ax = plt.subplots(1,figsize=(8,8), facecolor='white')
ax.axis('off')
ax.set_xlim(-1.5,1.5)
ax.set_ylim(-1.5,1.5)


ax.arrow(-1.4, 0, 2.8, 0, head_width=0.08, head_length=0.1, fc='k', ec='k', overhang=0.8)
ax.arrow(0, -1.4, 0, 2.8, head_width=0.08, head_length=0.1, fc='k', ec='k', overhang=0.8)

plt.text(1.5, 0,r'$x$', color="black", fontsize=25, va='top', ha='right')
plt.text(0.05, 1.5,r'$y$', color="black", fontsize=25, va='top', ha='left')
h = 0.05
plt.text(0.5*h, 0-h, latex(0, mode='inline'), color="black", fontsize=20, va='top', ha='left')



# xticks = [-1, -0.5, 1.0/2.0, 1]  # 这个是设置x刻度
# yticks = [-pi/3, -pi/6, pi/6, pi/3]  # 这个是设置y刻度
# # 下面的两个for循环不要动
# for i in range(len(xticks)):
#     plt.plot([xticks[i],xticks[i]], [0,h],"k")
#     tex = '$'+latex(xticks[i])+'$'
#     plt.text(xticks[i], 0-h, tex, color="black", fontsize=20, ha="center", va='top')
# for i in range(len(yticks)):
#     plt.plot([0,h], [yticks[i],yticks[i]],"k")
#     tex = '$'+latex(yticks[i])+'$'
#     plt.text(0-h, yticks[i], tex, color="black", fontsize=20, va='center', ha='right')




# 二次函数 y = x*x,  x \in [-0.5, 0.5]
x = np.linspace(-0.5, 0.5, 100)  # the x vector
y = x*x
plt.plot(x, y, lw=4, color="blue")

# 一次函数 y = x - 0.5,   x \in (-0.5, 1]
x = np.linspace(0.5, 1, 3)  # the x vector
y = x - 0.5
plt.plot(x, y, lw=4, color="green")


plt.plot([0.5, 0.5],  [0,  0.5*0.5],"--")  # 虚线
plt.plot([0.5], [0],    "wo", ms=10)  # 白色空心点
plt.plot([0.5],[0.25], 'ro', ms=10)          # 红色实心点
plt.text(0.5, 0-h, r'$0.5$', color="black", fontsize=20, va='top', ha="center")
# plt.savefig("ercihanshu.png", dip=20)
plt.show()