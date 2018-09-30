#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 浙江2015
@time: 2016-07-09 17:50
"""
from enthought.mayavi.scripts import mayavi2
import numpy as np
from mayavi import mlab

#为了显示透明效果，先画下面的图，再画上面的图
x = np.array([[-1,1,1,-1,-1],[-1,1,1,-1,-1]])
y = np.array([[-1,-1,-1,-1,-1],[1,1,1,1,1]])
z = np.array([[1,1,-1,-1,1],[1,1,-1,-1,1]])
mlab.mesh(x,y,z-1)

xx = np.array([-1,1,1,-1,0])
yy = np.array([-1,-1,1,1,0])
zz = np.array([0,0,0,0,2])
triangles = np.array([[0,1,4],[1,2,4],[2,3,4],[3,0,4]])
mlab.triangular_mesh(xx, yy, zz, triangles, transparent=True)
mlab.show()