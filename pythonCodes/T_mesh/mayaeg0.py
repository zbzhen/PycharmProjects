#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: mayaeg0.py
@time: 2016-04-22 11:21
"""
import numpy
from mayavi.mlab import *

#def test_triangular_mesh():
"""An example of a cone, ie a non-regular mesh defined by its
    triangles.
"""
n = 4
#triangles = [[0,0,0],[1,1,1],[2,2,2]]
triangles = [(0, 1, 2), (0, 2, 1), (0, 3, 1)]
x = [ 1. , -1.  , 0.5 , 0.5, -1. ]
y = [0,0,-0.8,0.8,0]
z = [3,0,0,0,0]

triangular_mesh(x, y, z, triangles, representation="wireframe",line_width=1.0)
axes(xlabel='x', ylabel='y', zlabel='z')
outline()
show()