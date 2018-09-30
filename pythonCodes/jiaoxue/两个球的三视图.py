#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 两个球的三视图
@time: 2016-09-11 21:59
"""

#from enthought.mayavi.scripts import mayavi2
import numpy as np
from mayavi import mlab


def plotball(core, r, n = 500):
    theta, phi = np.mgrid[0:np.pi:n+0j, 0:2*np.pi:n+0j]
    x = r*np.sin(theta)*np.cos(phi) + core[0]
    y = r*np.sin(theta)*np.sin(phi) + core[1]
    z = r*np.cos(theta) + core[2]
    mlab.mesh(x,y,z,transparent=True)
    return



"""

r = 0.1
R = 0.5*(3 - np.sqrt(3))-r
plotball([r-1,r-1,1-r], r)
plotball([1-R,1-R,R], -R)
"""
r = 1

#plotball([-r,0,0],r)
#plotball([R,0,0],R)
#plotball([0,0,0],r)
r = 1
R = 3 - np.sqrt(3) - r
plotball([r-1,r-1,r-1], r)
plotball([1-R,1-R,1-R], R)
x = np.array([[-1,1,1,-1,-1],[-1,1,1,-1,-1]])
y = np.array([[-1,-1,-1,-1,-1],[1,1,1,1,1]])
z = np.array([[1,1,-1,-1,1],[1,1,-1,-1,1]])
mlab.mesh(x,y,z,transparent=True)


mlab.show()