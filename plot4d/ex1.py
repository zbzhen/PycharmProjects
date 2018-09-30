#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: ex1
@time: 2018/4/26  9:34
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(100, projection='4d')
# ax = fig.add_subplot(100)

a =  np.random.standard_normal(50)
b =  np.random.standard_normal(50)
c =  np.random.standard_normal(50)
cc = np.random.standard_normal(50)

ax.scatter(a, b, c, cc=cc, cmap=plt.hot())
plt.show()