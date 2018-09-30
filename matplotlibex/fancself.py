#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: fancself
@time: 2018/7/7  9:07
"""
import numpy as np
import matplotlib.pyplot as plt
figheight = 8
fig = plt.figure(2, figsize=(9, figheight), dpi=80, facecolor="white")
fontsize = 0.4 * fig.dpi
ax = fig.add_subplot(111, frameon=False, xticks=[], yticks=[])
stylename = "square"
# ax.text(2, 2.5, stylename+"hhhhhhhhhhhh$\sum_{k=0}^n$" ,ha="center",
#               size=fontsize,
#               # transform=ax.transAxes,
#               bbox=dict(boxstyle=stylename, fc="w", ec="k"))
ax.annotate('$\sum_{k=0}^x$', (1, 1), (300, 300),
            xycoords='data',size=fontsize,
            textcoords='offset points',
            bbox=dict(boxstyle="round", fc="1"),
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="angle,angleA=90,angleB=0,rad=10"))

ax.annotate( '$\sum_{k=0}^n$',
            xytext=(-300, -300), xycoords='data',size=fontsize,
            xy=(4.1, 4.4), textcoords='offset points',
            bbox=dict(boxstyle="round4", fc="1"),
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="angle,angleA=90,angleB=0,rad=10"))
ax.set(xlim=(0, 5), ylim=(0, 5))
# c = plt.Circle((0.5,0.5), 1)
# ax.plot(c)
ax.set_aspect('equal', 'box')
# x = np.linspace(0,np.pi,30)
# ax.plot(x, np.sin(x))
# ax.plot([0.1,0.3],[0.2,0.4])
plt.show()