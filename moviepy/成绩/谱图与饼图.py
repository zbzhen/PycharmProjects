#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 18:44
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 谱图与饼图.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pylab import mpl
# 字体https://blog.csdn.net/u010758410/article/details/71743225
mpl.rcParams['font.sans-serif'] = ['FangSong']
plt.style.use("ggplot")
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20)


plt.figure(figsize=(13, 5), facecolor='white')

ability_label = [u"进攻", u"防守", u"盘带", u"速度", u"体力", u"突破"]
num = len(ability_label)
y = np.array([88,68,96,80,84,99])*0.01
yy = np.append(y, y[0])
theta = np.linspace(0, 2 * np.pi, num, endpoint=False)
# 6边形，首尾相连，形成闭合图形，需要7个点
theta = np.append(theta, theta[0])

ax1 = plt.subplot(121, projection = "polar")
ax1.plot(theta, yy, "r")
ax1.fill(theta, yy, "r", alpha = 0.3)
ax1.set_xticks(theta)
ax1.set_xticklabels(ability_label, fontproperties = font, y = 0.1)
# 设置标题
#ax1.set_title(u"梅西", position = (0.5, 1.01), fontproperties = font, color = "r", size = 20)
# 设置弧度显示的内容
ax1.set_yticks(np.linspace(0,1,num,endpoint=True))
for tick in ax1.yaxis.get_major_ticks():
    tick.label1.set_fontsize(0)

for i in range(num):
    # text = '$' + str(y[i]*100) + '\% $'
    text = '$' + str(y[i]) + '$'
    ax1.text(theta[i], y[i], text, fontsize=13, ha='left', va='top', color='g')



ax2 = plt.subplot(122)
myfont = FontProperties(size=20)
explode = [0.05]*num
patches,l_text,p_text = ax2.pie(y, explode=explode, labels=ability_label,
                                autopct='%1.2f%%', shadow=True, startangle=0)
for text in l_text:
    text.set_fontsize(18)
for text in p_text:
    text.set_fontsize(20)
    text.set_color("w")
ax2.axis('equal')
plt.show()