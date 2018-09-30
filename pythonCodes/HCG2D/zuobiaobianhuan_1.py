#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: zuobiaobianhuan_1
@time: 2017-01-22 22:57
"""
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-0.2,1.5)
plt.ylim(-0.2,1.5)

#画出坐标轴

plt.annotate("",(1.3,0),(-0.1,0),arrowprops={"arrowstyle": "->"},color="black")
plt.annotate("",(0,1.3),(0,-0.1),arrowprops={"arrowstyle": "->"},color="black")
plt.annotate("hang edge",(0.4,0.6),(0.5,0.8),arrowprops={"arrowstyle": "->"},color="blue",fontsize = 20)
t=0
plt.plot([0,1-t],[t,t],color="black")
plt.plot([t,t],[1-t,0],color="black")
plt.plot([0,1],[1,0],color="red")
plt.plot([0.5],[0.5],"*",color="black")
plt.plot([0],[1],"*",color="black")
plt.plot([1],[0],"*",color="black")
plt.plot([0],[0],"*",color="black")
plt.text(0.02,-0.08,'$ P_1(0,0) $',fontsize = 20)
plt.text(0.92,-0.08,'$ P_2(1,0) $',fontsize = 20)
plt.text(0.52,0.52,'$ P_3(\\frac{1}{2},\;\\frac{1}{2}) $',fontsize = 20)
plt.text(0.02,1.02,'$ P_4(0,1) $',fontsize = 20)
plt.text(1.26,-0.08,'$ x $',fontsize = 20)
plt.text(0.03,1.53-0.26,"$y$",fontsize = 20)
plt.savefig("xy.pdf",dip=120)
plt.show()
