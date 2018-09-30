#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 北京2015
@time: 2016-07-09 19:24
"""
#from enthought.mayavi.scripts import mayavi2
import numpy as np
from mayavi import mlab

#注意这个三棱锥的画法
x = np.array([0,2,0,2])
y = np.array([0,1,2,1])
z = np.array([0,0,0,1])
triangles = np.array([[0,1,2],[1,2,3],[0,1,3],[0,2,3]])
#mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=0.1)
mlab.triangular_mesh(x, y, z, triangles, transparent=True)
# mlab.outline()
mlab.show()