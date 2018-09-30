#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: sanjiaoxing2
@time: 2016-04-21 13:00
"""
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
#空间分形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

v=np.array( [[0,0,0.6],[-0.3,-0.5,-0.2],[-0.3,0.5,-0.2],[0.6,0,-0.2]] )
s=0
r=[]
for i in range(10**4):
    s=(s + random.choice(v))/2.0
    r.append(s)
x,y,z=zip(*r)

ax.scatter(x, y, z,  s=1, c='k')

plt.show()