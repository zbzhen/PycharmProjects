#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 参数方程画圆锥曲线
@time: 2016-10-01 14:41
"""
import numpy as np
import matplotlib.pyplot as plt

a = 4
b = 3
#设置坐标轴的范围

theta = np.linspace(0,0.5*np.pi,40)
x = a*np.cos(theta)
y = b*np.sin(theta)
plt.plot(x, y)
plt.show()
