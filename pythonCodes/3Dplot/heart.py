#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: heart.py
@time: 2016-04-21 19:32
"""
import numpy as np
import matplotlib.pyplot as plt

X = np.arange(-5.0, 5.0, 0.1)
Y = np.arange(-5.0, 5.0, 0.1)

x, y = np.meshgrid(X, Y)
f = 17 * x ** 2 - 16 * np.abs(x) * y + 17 * y ** 2 - 225

fig = plt.figure()
cs = plt.contour(x, y, f, 0, colors ="red")
plt.show()