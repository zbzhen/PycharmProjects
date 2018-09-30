#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 17:40
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : Tcube.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-0.2,0.9)
plt.ylim(-0.7,1.3)

p1 = np.array([0,0])
p5 = np.array([0,1])
p4 = np.array([0.75,0.25])
p2 = np.array([0.5,-0.5])
p3 = 0.5*(p2+p4)
p8 = 0.5*(p4+p5)
p6 = 0.5*(p2+p5)
p7 = 0.33333333*(p2+p4+p5)
plt.plot(p1[0],p1[1],'bo')
plt.plot(p2[0],p2[1],'bo')
plt.plot(p3[0],p3[1],'bo')
plt.plot(p4[0],p4[1],'bo')
plt.plot(p5[0],p5[1],'bo')
plt.plot(p6[0],p6[1],'bo')
plt.plot(p7[0],p7[1],'bo')
plt.plot(p8[0],p8[1],'bo')

plt.text(p1[0],p1[1],"$P_1$",fontsize = 20, verticalalignment='top', horizontalalignment='right')
plt.text(p2[0],p2[1],"$P_2$",fontsize = 20, verticalalignment='top', horizontalalignment='right')
plt.text(p3[0],p3[1],"$P_3$",fontsize = 20, verticalalignment='top', horizontalalignment='left')
plt.text(p4[0],p4[1],"$P_4$",fontsize = 20, verticalalignment='top', horizontalalignment='left')
plt.text(p5[0],p5[1],"$P_5$",fontsize = 20, verticalalignment='top', horizontalalignment='right')
plt.text(p6[0],p6[1],"$P_6$",fontsize = 20, verticalalignment='top', horizontalalignment='right')
plt.text(p7[0],p7[1],"$P_7$",fontsize = 20, verticalalignment='bottom', horizontalalignment='left')
plt.text(p8[0],p8[1],"$P_8$",fontsize = 20, verticalalignment='top', horizontalalignment='right')


plt.plot([p1[0], p2[0], p4[0], p5[0], p1[0]], [p1[1], p2[1], p4[1], p5[1], p1[1]], "black")
plt.plot([p1[0], p4[0]], [p1[1], p4[1]], "--", color = "black")
plt.plot([p2[0], p5[0]], [p2[1], p5[1]], "black")
plt.plot([p7[0], p3[0]], [p7[1], p3[1]], "--", color = "red")
plt.plot([p7[0], p6[0]], [p7[1], p6[1]], "--", color = "red")
plt.plot([p7[0], p8[0]], [p7[1], p8[1]], "--", color = "red")

plt.savefig("Tcube.pdf",dip=120)
plt.show()