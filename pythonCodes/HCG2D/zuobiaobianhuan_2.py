#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: zuobiaobianhuan_2
@time: 2017-01-23 10:34
"""
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-0.2,1.5)
plt.ylim(-0.2,1.5)

#画出坐标轴

plt.annotate("",(1.3,0),(-0.1,0),arrowprops={"arrowstyle": "->"},color="black",fontsize = 20)
plt.annotate("",(0,1.3),(0,-0.1),arrowprops={"arrowstyle": "->"},color="black",fontsize = 20)
t=0

plt.plot([0.2,0.7,0.9,0.3,0.2],[0.4,0.2,0.6,0.9,0.4])


plt.text(0.06,0.25,'$ P_1(x_1,y_1) $',fontsize = 20)
plt.text(0.6,0.13,'$ P_2(x_2,y_2) $',fontsize = 20)
plt.text(0.9,0.6,'$ P_3(x_3,y_3) $',fontsize = 20)
plt.text(0.1,0.95,'$ P_4(x_4,y_4) $',fontsize = 20)
plt.text(1.26,-0.08,'$ x$',fontsize = 20)
plt.text(0.03,1.53-0.26,"$y $",fontsize = 20)

plt.savefig("qxy.pdf",dip=120)
plt.show()