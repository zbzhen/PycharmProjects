#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mayaviexmp1
@time: 2018/5/1  18:58
"""
from mayavi import mlab
import numpy as np

x, y, z = np.mgrid[-2:2:20j, -2:2:20j, -2:2:20j]
# x, y, z = np.ogrid[-2:2:20j, -2:2:20j, -2:2:20j]
s = np.sin(x*y*z + x + y*z)/(x*y*z + x + y*z)

scr = mlab.pipeline.scalar_field(x,y,z,s)

# mlab.pipeline.glyph(scr, scale_mode='none', scale_factor=.1)
mlab.pipeline.delaunay3d(scr)
# mlab.pipeline.image_plane_widget(scr,
#                             plane_orientation='x_axes',plane_opacity=0.1,opacity=0.1,
#                             # slice_index=25,
#                         )
# mlab.pipeline.image_plane_widget(scr,
#                             plane_orientation='y_axes',plane_opacity=0.1,opacity=0.1,
#                             # slice_index=25,
#                         )
# mlab.pipeline.image_plane_widget(scr,
#                             plane_orientation='z_axes',plane_opacity=0.1,opacity=0.1,
#                             # slice_index=25,
#                         )
# mlab.outline()
mlab.show()