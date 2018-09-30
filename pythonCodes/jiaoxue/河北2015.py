#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 河北2015
@time: 2016-07-09 20:08
"""
#from enthought.mayavi.scripts import mayavi2
import numpy as np
from mayavi import mlab

#绘制半球
n = 500
r = 1
p, a = np.mgrid[0:r:n+0j, 0:2*np.pi:n+0j]
x = p*np.cos(a)
y = p*np.sin(a)
z = np.sqrt(r*r-x**2 - y**2)
mlab.mesh(z+1,x,y,transparent=True)


#绘制半柱面
x, y = np.mgrid[-1:1:100j,-1:1:100j]
z = (1-x**2)**0.5+0*y
mlab.mesh(y,x,-z,transparent=True)


x = [[-1,1],[-1,1]]
y = [[1,1],[-1,-1]]
z = [[0,0],[0,0]]
mlab.mesh(x,y,z,transparent=True)
#绘制半圆
n = 500
r = 1
p, a = np.mgrid[0:r:n+0j, np.pi:2*np.pi:n+0j]
x = p*np.cos(a)
y = p*np.sin(a)
z = x*0
#transparent=True
mlab.mesh(z-1,x,y,transparent=True)
mlab.mesh(z+1,x,y,transparent=True)
mlab.show()