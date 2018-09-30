#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 15:36
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 球员能力图谱.py
# @version : Python 2.7.6

#!/usr/bin/python
#coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.style.use("ggplot")
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
# from pylab import mpl
# mpl.rcParams['font.sans-serif'] = ['SimHei']

# 类别数量
ability_size = 6
# 6种类别
ability_label = [u"进攻", u"防守", u"盘带", u"速度", u"体力", u"突破"]
ability_size = len(ability_label)
# 球员能力值
player = {
    "M" : np.random.randint(size = ability_size, low= 0, high= 99),
    "H" : np.random.randint(size = ability_size, low= 0, high= 99),
    "P" : np.random.randint(size = ability_size, low= 0, high= 99),
    "Q" : np.random.randint(size = ability_size, low= 0, high= 99)
}

theta = np.linspace(0, 2 * np.pi, ability_size, endpoint=False)
# 6边形，首尾相连，形成闭合图形，需要7个点
theta = np.append(theta, theta[0])
# 运动员的这一个也增加一项
player["M"] = np.append(player['M'], player['M'][0])
player["H"] = np.append(player['H'], player['H'][0])
player["P"] = np.append(player['P'], player['P'][0])
player["Q"] = np.append(player['Q'], player['Q'][0])

ax1 = plt.subplot(221, projection = "polar")
ax1.plot(theta, player['M'], "r")
ax1.fill(theta, player['M'], "r", alpha = 0.3)
# 把角度对应6等分
ax1.set_xticks(theta)
# 设置6个位置的显示内容
# y 用来设置距离极坐标图的距离
ax1.set_xticklabels(ability_label, fontproperties = font, y = 0.1)
# 设置标题
ax1.set_title(u"梅西", position = (0.5, 1.01), fontproperties = font, color = "r", size = 20)
# 设置弧度显示的内容
ax1.set_yticks(np.arange(0, 101, 20))

ax2 = plt.subplot(222, projection = "polar")
ax2.plot(theta, player['H'], "g")
ax2.fill(theta, player['H'], 'g', alpha = 0.3)
ax2.set_xticks(theta)
ax2.set_xticklabels(ability_label, fontproperties = font, y = 0.1)
ax2.set_title(u"哈维", position = (0.5, 1.01), fontproperties = font, color = "g", size = 20)
ax2.set_yticks(np.arange(0, 101, 20))

ax3 = plt.subplot(223, projection = "polar")
ax3.plot(theta, player['P'], "y")
ax3.fill(theta, player['P'], 'y', alpha = 0.3)
ax3.set_xticks(theta)
ax3.set_xticklabels(ability_label, fontproperties = font, y = 0.1)
ax3.set_title(u"匹克", position = (0.5, 1.01), fontproperties = font, color = "y", size = 20)
ax3.set_yticks(np.arange(0, 101, 20))

ax4 = plt.subplot(224, projection = "polar")
ax4.plot(theta, player['Q'], "b")
ax4.fill(theta, player['Q'], 'b', alpha = 0.3)
ax4.set_xticks(theta)
ax4.set_xticklabels(ability_label, fontproperties = font, y = 0.1)
ax4.set_title(u"切赫", position = (0.5, 1.01), fontproperties = font, color = "b", size = 20)
ax4.set_yticks(np.arange(0, 101, 20))

plt.show()