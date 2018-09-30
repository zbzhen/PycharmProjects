#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: rehsape
@time: 2016-02-28 16:01
"""
import  numpy as np
a = np.array(range(9))
b = a.reshape((3,3))
c = np.arange(16).reshape((4,4))
print c
d = c[0:3, 0:3]
e = c[-3:,-3:]
print e
N = 11
print range(1, N/3)
print np.exp(2)
print np.linspace(0,1,3)
K = [[1,0,0],[0,1,0],[0,0,1]]
F = [2,3,0]
KK = np.append(K, np.zeros((3, 3)),axis=0)
print KK