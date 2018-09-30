#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: zuobiaobianhuan
@time: 2017-01-22 22:37
"""
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)

#画出坐标轴

plt.annotate("",(1.4,0),(-1.4,0),arrowprops={"arrowstyle": "->"},color="black")
plt.annotate("",(0,1.4),(0,-1.4),arrowprops={"arrowstyle": "->"},color="black")
plt.plot([-1,1,1,-1,-1],[-1,-1,1,1,-1],color="black")
plt.text(-1.2,-1.2,"$\widehat{P_1}$",fontsize = 20)
plt.text(-1.2,1.03,"$\widehat{P_4}$",fontsize = 20)
plt.text(1.03,-1.2,"$\widehat{P_2}$",fontsize = 20)
plt.text(1.03,1.03,"$\widehat{P_3}$",fontsize = 20)

plt.text(1.03,-0.13,"$1$",fontsize = 20)
plt.text(1.33,-0.13,'$ \\xi $',fontsize = 20)
plt.text(-1.03+0.06,-0.13,"$-1$",fontsize = 20)
plt.text(0.03,-1.13,"$-1$",fontsize = 20)
plt.text(0.03,1.13-0.26,"$1$",fontsize = 20)
plt.text(0.03,1.53-0.26,"$\eta$",fontsize = 20)
plt.savefig("xieta.pdf",dip=120)
plt.show()
