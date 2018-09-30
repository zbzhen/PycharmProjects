#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 111
@time: 2016-05-08 21:26
"""
import numpy as np
a = np.array([[1,0,0]])
b = np.array([[0,0,1]])
print a.T*b
print b.T*a
print b*a.T
print a*b.T

c = np.dot(a.T, b)
print 1.36226242742e-07**0.5