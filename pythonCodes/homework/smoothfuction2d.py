#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: smoothfuction2d
@time: 2016-03-03 23:11
"""
from _1_Intergral_8 import Intergral_2
import  numpy as np
from enthought.mayavi import mlab

def smoothfuc_2d(x, y):
    normx = x**2 + y**2
    if normx < 1:
        return np.e**(1.0/(normx - 1))
    return 0*x
c2d = Intergral_2().guass_leg_2_comp(smoothfuc_2d, (-1, 1), (-1, 1), mx=20, my=20)

def b2d(g2d):
    def bb(x, y):
        def f(s, t):
            return g2d(s, t)*smoothfuc_2d(x - s, y - t)
        return Intergral_2().guass_leg_2_comp(f, (-2, 2), (-2, 2), mx=4, my=4, n=4)/c2d
    return bb

def g2d(x, y):
    return int(x + y)



x2d, y2d = np.mgrid[-2:2:41j, -2:2:41j]
(m, n) = x2d.shape
z2d = np.zeros((m, n))
for i in range(m):
    for j in range(n):
        z2d[i][j] = b2d(g2d)(x2d[i][j], y2d[i][j]) #1times
        #z2d[i][j] = g2d(x2d[i][j], y2d[i][j]) #ture
        #z2d[i][j] = smoothfuc_2d(x2d[i][j], y2d[i][j])/c2d

pl = mlab.mesh(x2d, y2d, z2d)
mlab.axes(xlabel='x', ylabel='y', zlabel='z')
mlab.outline(pl)
#mlab.title( "Graph of z=e^(1.0/(x^2+y^2 - 1))/c")
mlab.title( "Graph of smmoth z=int(x+y)")
mlab.show()