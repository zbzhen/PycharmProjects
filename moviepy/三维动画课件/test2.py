#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 17:12
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : test2.py
# @version : Python 2.7.6
from mayavi import mlab
import numpy as np
xx = yy = zz = np.arange(-0.6,0.7,0.1)
xy = xz = yx = yz = zx = zy = np.zeros_like(xx)
lensoffset = 0.3
mlab.plot3d(yx,yy+lensoffset,yz,line_width=0.01,tube_radius=0.01)
mlab.plot3d(zx,zy+lensoffset,zz,line_width=0.01,tube_radius=0.01)
mlab.plot3d(xx,xy+lensoffset,xz,line_width=0.01,tube_radius=0.01)
mlab.show()
