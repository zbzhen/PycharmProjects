#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/9 19:56
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : space3d.py
# @version : Python 2.7.6
import numpy
from mayavi import mlab
# mlab.test_flow_anim()

# x, y, z = numpy.ogrid[-5:5:64j, -5:5:64j, -5:5:64j]
#
# scalars = x+y+z
#
# obj = mlab.contour3d(scalars, contours=4, transparent=True)
# mlab.test_contour3d()
# mlab.test_fancy_mesh()  # good
# mlab.test_molecule()  # good
# mlab.test_quiver3d()
# mlab.test_simple_surf()
# mlab.test_simple_surf_anim()
# mlab.test_surf()
# mlab.test_quiver3d_2d_data()
x, y, z = numpy.mgrid[-4:4:2j, -4:4:2j, 0:4:2j]
r = numpy.sqrt(x ** 2 + y ** 2  + 0.1)
u = y * numpy.sin(r) / r
v = -x * numpy.sin(r) / r
w = numpy.ones_like(z)*0.05
obj = mlab.flow(u, v, w)
mlab.show()
# print len(2)

# INPUT = [(1,2),(1,),(1,2,3)]
# import itertools
# import operator as op
# a = list(itertools.chain.from_iterable(INPUT))
# print a
# def space(*args):
#     # a = list(itertools.chain.from_iterable([args]))
#     a = reduce(op.add, map(list, args))
#     print a
#     return
#
# space(1,2,3)
# space(1,(2),(3,4),(3,(3,4),5))