#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 16:57
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : test.py
# @version : Python 2.7.6
import mayavi.mlab as mlab

black = (0,0,0)
white = (1,1,1)
mlab.figure(bgcolor=white)
mlab.plot3d([0, 1000], [0, 0], [0, 0], color=black, tube_radius=10.)
mlab.plot3d([0, 0], [0, 1500], [0, 0], color=black, tube_radius=10.)
mlab.plot3d([0, 0], [0, 0], [0, 1500], color=black, tube_radius=10.)
mlab.text3d(1050, -50, +50, 'X', color=black, scale=100.)
mlab.text3d(0, 1550, +50, 'Y', color=black, scale=100.)
mlab.text3d(0, -50, 1550, 'Z', color=black, scale=100.)
mlab.axes()

mlab.outline()
mlab.colorbar()
mlab.show()
