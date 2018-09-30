#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 18:25
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 能力图谱.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.style.use("ggplot")
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

ability_label = [u"进攻", u"防守", u"盘带", u"速度", u"体力", u"突破"]
ability_size = len(ability_label)
y = np.random.randint(size = ability_size, low= 0, high= 99)
y = np.append(y, y[0])
theta = np.linspace(0, 2 * np.pi, ability_size, endpoint=False)
# 6边形，首尾相连，形成闭合图形，需要7个点
theta = np.append(theta, theta[0])





ax1 = plt.subplot(121, projection = "polar")
ax1.plot(theta, y, "r")
ax1.fill(theta, y, "r", alpha = 0.3)
# 把角度对应6等分
ax1.set_xticks(theta)
# 设置6个位置的显示内容
# y 用来设置距离极坐标图的距离
ax1.set_xticklabels(ability_label, fontproperties = font, y = 0.1)
# 设置标题
ax1.set_title(u"梅西", position = (0.5, 1.01), fontproperties = font, color = "r", size = 20)
# 设置弧度显示的内容
ax1.set_yticks(np.arange(0, 101, 20))
plt.show()