#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: sancihanshu
@time: 2016-04-21 10:36
"""
import matplotlib.pyplot as plt
import numpy as np
#研究三次函数的性质
x = np.linspace(1, 3, 1025)
y = (x-1)*(x-2)*(x-3)
y1 = (x-1)*(x-2)*(-3)+(x-1)*(-2)*(x-3)+(-1)*(x-2)*(x-3)
y2 = (-3)*(2*x -3) + (-2)*(2*x - 4) + (-1)*(2*x - 5)
plt.plot(x, y)
#plt.plot(x, y1)
#plt.plot(x, y2)
plt.show()