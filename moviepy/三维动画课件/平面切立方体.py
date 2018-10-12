#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 20:40
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 平面切立方体.py
# @version : Python 2.7.6

import numpy as np
from enthought.mayavi import mlab
x, y, z = np.mgrid[0:1:2j, 0:1:2j, 0:1:2j]
mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(0, 0, 0), size=(700, 700))
src = mlab.pipeline.vector_field(x, y, z, x*0, y*0, z*0)
mlab.pipeline.vector_cut_plane(src, mask_points=1, scale_factor=1)
mlab.show()
