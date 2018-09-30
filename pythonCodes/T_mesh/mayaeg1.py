#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: mayaeg1
@time: 2016-04-22 00:06
"""
import numpy
from mayavi.mlab import *

#def test_triangular_mesh():
"""An example of a cone, ie a non-regular mesh defined by its
    triangles.
"""
n = 5
t = numpy.linspace(-numpy.pi, numpy.pi, n)
z = numpy.exp(1j * t)

x = z.real.copy()
y = z.imag.copy()
z = numpy.zeros_like(x)

triangles = [(0, i, i + 1) for i in range(1, n)]
triangles = [[1,2,3],[2,3,4],[0,1,2]]
x = numpy.r_[0, x]
y = numpy.r_[0, y]
z = numpy.r_[1, z]
t = numpy.r_[20, t] #调节颜色
print x, y, z, triangles
triangular_mesh(x, y, z, triangles, scalars=t, representation="wireframe",line_width=1.0)
axes(xlabel='x', ylabel='y', zlabel='z')
outline()
show()