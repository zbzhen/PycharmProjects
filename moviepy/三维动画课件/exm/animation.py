#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 22:12
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : animation.py
# @version : Python 2.7.6
import numpy as np
from mayavi import mlab
# x, y = np.mgrid[0:3:1,0:3:1]
# s = mlab.surf(x, y, np.asarray(x*0.1, 'd'))

import numpy as np
from mayavi import mlab
x, y = np.mgrid[0:3:1,0:3:1]
s = mlab.surf(x, y, np.asarray(x*0.1, 'd'))

@mlab.animate
def anim():
    for i in range(10):
        s.mlab_source.scalars = np.asarray(x*0.1*(i+1), 'd')
        yield

anim()
mlab.show()