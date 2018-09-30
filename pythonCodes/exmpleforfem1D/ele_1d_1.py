#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: ele_1d_1
@time: 2016-05-20 19:41
"""
import numpy as np
import matplotlib.pyplot as plt

#--------------------------这一步是标准区域插值与坐标变换-------------------
#插值基函数
#标准三次插值
def baseinter():
    def f(x):
        return [(3*x-1)*(3*x+1)*(x-1), (x+1)*(3*x-1)*(x-1), (x+1)*(x-1)*(3*x+1), (x+1)*(3*x+1)*(3*x-1)]
    def ff(x):
        ans = [f(x)[0]*1.0/f(-1)[0], f(x)[1]*1.0/f(-1.0/3)[1], f(x)[2]*1.0/f(1.0/3)[2], f(x)[3]*1.0/f(1)[3]]
        return np.array(ans)
    return ff

#坐标变换
def coordtransform(D, x):
    s = (2*x - (D[0]+D[-1]))*1.0/(D[-1]-D[0])
    return s

def coordtansform_v(D, s):
    x = 0.5*(D[0]+D[-1]) + 0.5*s*(D[-1]-D[0])
    return x

def putongchazhi(D, x):
    s = coordtransform(D, x)
    return baseinter()(s)

#------------------------这一步是画图--------------------------------------

