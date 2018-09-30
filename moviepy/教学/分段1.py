#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 18:24
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 分段1.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex, var, pi

fig_mpl, ax = plt.subplots(1,figsize=(8,8), facecolor='white')
ax.axis('off')
ax.set_xlim(-8.5,5.5)
ax.set_ylim(-2.5,11.5)


ax.arrow(-8, 0, 12, 0, head_width=0.2, head_length=0.2, fc='k', ec='k', overhang=0.8)
ax.arrow(0, -2, 0, 12, head_width=0.08, head_length=1, fc='k', ec='k', overhang=0.8)

plt.text(1.5, 0,r'$x$', color="black", fontsize=25, va='top', ha='right')
plt.text(0.05, 1.5,r'$y$', color="black", fontsize=25, va='top', ha='left')
h = 0.05
plt.text(0.5*h, 0-h, latex(0, mode='inline'), color="black", fontsize=20, va='top', ha='left')


# 二次函数 y = x*x,  x \in [-0.5, 0.5]
x = np.linspace(-8, 0, 2)  # the x vector
y = x + 6
plt.plot(x, y, lw=4, color="blue")

# 一次函数 y = x - 0.5,   x \in (-0.5, 1]
x = np.linspace(0, 4.5, 100)  # the x vector
y = x*x - 4*x + 6
plt.plot(x, y, lw=4, color="green")


# plt.plot([0.5, 0.5],  [0,  0.5*0.5],"--")  # 虚线
# plt.plot([0.5], [0],    "wo", ms=10)  # 白色空心点
# plt.plot([0.5],[0.25], 'ro', ms=10)          # 红色实心点
# plt.text(0.5, 0-h, r'$0.5$', color="black", fontsize=20, va='top', ha="center")
# plt.savefig("ercihanshu.png", dip=20)
plt.show()