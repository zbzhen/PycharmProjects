#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 19:12
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 坐标轴和箭头.py
# @version : Python 2.7.6
from mpl_toolkits.axisartist.axislines import SubplotZero
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号
fig = plt.figure(1, (10, 6))

ax = SubplotZero(fig, 1, 1, 1)
fig.add_subplot(ax)

"""新建坐标轴"""
ax.axis["xzero"].set_visible(True)
ax.axis["xzero"].label.set_text(u"新建y=0坐标")
ax.axis["xzero"].label.set_color('green')
ax.axis['yzero'].set_visible(True)
ax.axis["yzero"].label.set_text(u"新建x=0坐标")

"""坐标箭头"""
ax.axis["yzero"].set_axisline_style("->")
ax.axis["xzero"].set_axisline_style("->")

"""隐藏坐标轴"""

ax.axis["top", 'right', 'left', 'bottom'].set_visible(False)

"""设置刻度"""
ax.set_ylim(-3, 3)
ax.set_yticks([-2, -1, 1, 2])
ax.set_xlim([-5, 8])
ax.set_xticks([-4,-3,-2,-1,1,2,3,4])



#设置网格样式
# ax.grid(True, linestyle='-.')


xx = np.arange(-4, 2*np.pi, 0.01)
ax.plot(xx, np.sin(xx))
plt.show()
