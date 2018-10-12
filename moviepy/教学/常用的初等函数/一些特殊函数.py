#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/5 15:07
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 一些特殊函数.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex, var, pi
x = var('x')


fig_mpl, ax = plt.subplots(1,figsize=(8,8), facecolor='white')
ax.axis('off')
ax.set_xlim(-7,7)
ax.set_ylim(-7,7)
h = 0.05

ax.arrow(-6, 0, 12, 0, head_width=0.3, head_length=0.3, fc='k', ec='k', overhang=0.8, lw=2)
plt.text(6, 0,r'$x$', color="black", fontsize=30, va='top', ha='left')




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


# fig1
# ax.arrow(0, -2, 0, 8, head_width=0.3, head_length=0.3, fc='k', ec='k', overhang=0.8, lw=2)
# plt.text(0+h, 6,r'$y$', color="black", fontsize=30, va='center', ha='left')
# xx = np.linspace(-5, 5, 100)
# yy = abs(xx+1) + abs(xx-1)
# plt.plot(xx, yy, lw=3, color="blue")
# plt.plot(xx, yy, lw=3, color="blue")
# plt.plot([1, 1], [0, 2], "--", lw=2, color="g")
# plt.plot([-1, -1], [0, 2], "--", lw=2, color="g")
# plt.text(1, 0-h, latex(1, mode='inline'), color="black", fontsize=20, ha="center", va='top')
# plt.text(-1, 0-h, latex(-1, mode='inline'), color="black", fontsize=20, ha="center", va='top')
# plt.text(0-h, 2-h, latex(2, mode='inline'), color="black", fontsize=20, ha="right", va='top')
# plt.text(0, -3, r'$f(x) = |x-1|+|x+1|$', color="blue", fontsize=40, va='center', ha='center')
# plt.savefig("teshuhanshu1.png", dip=20)



# # fig3
# ax.arrow(0, -2, 0, 5, head_width=0.3, head_length=0.3, fc='k', ec='k', overhang=0.8, lw=2)
# plt.text(0+h, 3,r'$y$', color="black", fontsize=30, va='center', ha='left')
# xx = np.linspace(-5, 5, 100)
# yy = 1.0*xx/(1+xx*xx)
# plt.plot(xx, yy, lw=3, color="blue")
# plt.text(0, -3, r'$f(x) = \frac{x}{1+x^2}$', color="blue", fontsize=40, va='center', ha='center')
# plt.savefig("teshuhanshu3.png", dip=20)


# # fig4
# ax.arrow(0, -6, 0, 12, head_width=0.3, head_length=0.3, fc='k', ec='k', overhang=0.8, lw=2)
# plt.text(0+h, 6,r'$y$', color="black", fontsize=30, va='center', ha='left')
# xx = np.linspace(-5, 5, 100)
# yy = xx
# plt.plot(xx, yy, lw=3, color="blue")
# plt.plot([1],[1], "wo", ms=10)
# plt.text(1+0.2, 1, r'$(1,1)$', color="red", fontsize=30, va='center', ha='left')
# plt.text(3, -3, r'$f(x) = \frac{x^2-x}{x-1}$', color="blue", fontsize=40, va='center', ha='center')
# plt.savefig("teshuhanshu4.png", dip=20)

plt.show()