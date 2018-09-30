#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 绘制圆锥曲线
@time: 2016-09-11 11:55
"""
import numpy as np
import matplotlib.pyplot as plt
a = 3
b = 4
#设置坐标轴的范围
plt.xlim(-1.3*a,1.3*a)
plt.ylim(-1.3*b,1.3*b)

plt.annotate("",(-1.2*a,0),(1.2*a,0),arrowprops={"arrowstyle": "<-"})
plt.annotate("",(0,-1.2*b),(0,1.2*b),arrowprops={"arrowstyle": "<-"})


t = np.linspace(-2, 2,50)
x = 1 - 2**0.5*t
y = 2 + 2**0.5*t

theta = np.linspace(0, 1.5*np.pi,150)
xx = 10**0.5*np.cos(theta)+3
yy = 10**0.5*np.sin(theta)+1
"""
#设置坐标轴的范围
theta = np.linspace(0, 1.5*np.pi,150)

x = a*np.cos(theta)+1
y = b*np.sin(theta)-1
"""
plt.plot(x, y)
plt.plot(xx, yy)

plt.show()