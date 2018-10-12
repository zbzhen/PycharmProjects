#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/9 10:33
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : test54.py
# @version : Python 2.7.6
import numpy as np
from mayavi import mlab
fig = mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))

a = 4
b = -3
c = -5
t = lambda x: 1.0*x/abs(x)
mlab.quiver3d(0, 0, 0, a-t(a), 0, 0,extent=[0,a-t(a),0,0,0,0], color=(1,0,0), mode='2ddash')
mlab.quiver3d(a-t(a), 0, 0, a, 0, 0,extent=[a-t(a),a,0,0,0,0], color=(1,0,0), mode='arrow')

mlab.quiver3d(0, 0, 0, 0, b-t(b), 0, extent=[0,0,0,b-t(b),0,0], color=(0,1,0), mode='2ddash')
mlab.quiver3d(0, b-t(b), 0, 0, b, 0, extent=[0,0,b-t(b),b,0,0], color=(0,1,0), mode='arrow')

mlab.quiver3d(0, 0, 0, 0, 0, c-t(c), extent=[0,0,0,0,0,c-t(c)], color=(0,0,1), mode='2ddash')
mlab.quiver3d(0, 0, c-t(c), 0, 0, c, extent=[0,0,0,0,c-t(c),c], color=(0,0,1), mode='arrow')

mlab.text(a, 0, 'X', z=0, width=0.03)
mlab.text(0, b, 'Y', z=0, width=0.03)
mlab.text(0, 0, 'Z', z=c, width=0.03)
mlab.show()