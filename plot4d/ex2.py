#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: ex2
@time: 2018/4/26  9:51
"""
import matplotlib.pyplot as plt
import numpy as np
x, y, z = np.random.standard_normal(50), np.random.standard_normal(50), np.random.standard_normal(50)
fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=np.random.standard_normal(50))
plt.show()