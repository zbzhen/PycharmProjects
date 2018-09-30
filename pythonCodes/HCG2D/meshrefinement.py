#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: meshrefinement
@time: 2017-01-22 21:53
"""
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-0.1,1.1)
plt.ylim(-0.1,1.1)
#箭头
n = 4

for i in range(n):
    t = 1.0*i/n
    plt.plot([0,1-t],[t,t],color="black")
    plt.plot([t,t],[1-t,0],color="black")
    plt.plot([0,t],[t,0],color="red")
plt.plot([0,1],[1,0],color="red")

plt.savefig("add_"+str(n-1)+".pdf",dip=120)
plt.show()