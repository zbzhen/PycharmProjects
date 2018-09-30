#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: sanjiaoxing1
@time: 2016-04-21 12:58
"""
#三角形分形1
import random
import numpy as np
import matplotlib.pyplot as plt

#v=np.array( [[0,0],[1,0],[0.5,0.8]] )
v=np.array( [[0,0],[1,0],[0,1]] )
s=0
r=[]
for i in range(10):
    print random.choice(v)
    s=(s + random.choice(v))/2.0
    r.append(s)
    print s
x,y=zip(*r)

plt.plot(x, y, 'ko',ms=2)
plt.show()