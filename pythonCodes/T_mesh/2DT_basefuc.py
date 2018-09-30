#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 2DT_basefuc.py
@time: 2016-04-22 23:04
"""

import numpy as np
from mayavi import mlab

#########三角形插值基
#求出三角形面积
def tradet(D):
    ans = (D[0][0] - D[-1][0])*(D[1][1] - D[-1][1]) - (D[1][0] - D[-1][0])*(D[0][1] - D[-1][1])
    return abs(ans)

#求出坐标变换
def coordtransfm(D, s, t):
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    return (x, y)

def coordtransfm_v(D, x, y):
    s = (D[1][0] - x)*(D[2][1] - y) - (D[2][0] - x)*(D[1][1] - y)
    t = (D[2][0] - x)*(D[0][1] - y) - (D[0][0] - x)*(D[2][1] - y)
    s *= 1.0/tradet(D)
    t *= 1.0/tradet(D)
    return  s, t

#标准三角形一次基函数
def base_1_():
    def bf0(s, t):
        return s
    def bf1(s, t):
        return t
    def bf2(s, t):
        return 1 - s - t
    return [bf0, bf1, bf2]

#标准三角形二次基函数
def base_2_():
    def bf0(s, t):
        return s*(s - 0.5)*2
    def bf1(s, t):
        return t*(t - 0.5)*2
    def bf2(s, t):
        return (1 - s - t)*(0.5 - s - t)*2
    return [bf0, bf1, bf2]

def exchangef(f, D):
    def ff(s, t):
        (x, y) = coordtransfm(D, s, t)
        return f(x, y)
    return ff

def tpltbasef_2_(f, D, bh=1, n=9):
    x, y = np.mgrid[0:1:n+0j, 0:1:n+0j]

    #这种坐标变换是将等腰直角三角形斜边的中点变成正方形的一个角
    if bh == 1:
        s = x - 0.5*x*y
        t = y - 0.5*x*y

    #这种变换是将正方形的其中两点变换成为同一个点：直角三角形的直角顶点
    else:
        s = x*y
        t = y*(1 - x)

    (x,  y) = coordtransfm(D, s, t)
    #下面是建立标准三角形与普通三角形之间的坐标变换
    z = f(s, t)
    mlab.mesh(x, y, z, transparent=True)
    return

def tplt(f, D, bh=1, n=9):
    x, y = np.mgrid[0:1:n+0j, 0:1:n+0j]

    #这种坐标变换是将等腰直角三角形斜边的中点变成正方形的一个角
    if bh == 1:
        s = x - 0.5*x*y
        t = y - 0.5*x*y

    #这种变换是将正方形的其中两点变换成为同一个点：直角三角形的直角顶点
    else:
        s = x*y
        t = y*(1 - x)

    #下面是建立标准三角形与普通三角形之间的坐标变换
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    z = f(x, y)
    mlab.mesh(x, y, z, transparent=True)
    return

if __name__ == '__main__':
    def f(x, y):
        return 0*x*y*(x-1)*(y-1)
    #D1 = [[1, 0], [0, 1], [0, 0]]
    D1 = [[0, 0], [0.7, 0.3], [0.3, 0.7]]
    def g(x, y):
        (s, t) = coordtransfm_v(D1, x, y)
        return base_1_()[1](s, t)
    tpltbasef_2_(g, D1, n=65)
    #tpltbasef_2_(exchangef(f, D1), n=4)
    tplt(f, D1, bh=1, n=9)
    mlab.show()
