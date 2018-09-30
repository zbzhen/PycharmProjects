#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mayaviunstructedgrid
@time: 2018/5/1  19:37
"""
from mayavi import mlab
import numpy as np


# x, y, z = np.ogrid[0:1:20j, 0:1:20j, 0:1:20j]
x, y, z = np.mgrid[0:1:20j, 0:1:20j, 0:1:20j]
s = np.sin(x*y*z + x + y*z)*(x*y*z + x + y*z)
mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='x_axes',
                            slice_index=20,line_width = 0.01,opacity=0.1,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='y_axes',
                            slice_index=20,line_width = 0.01,opacity=0.1,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='z_axes',
                            slice_index=20,line_width = 0.01,opacity=0.1,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='x_axes',
                            slice_index=0,line_width = 0.01,opacity=0.1,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='y_axes',
                            slice_index=0,line_width = 0.01,opacity=0.1,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='z_axes',
                            slice_index=0,line_width = 0.01,opacity=0.1,
                        )
x, y, z = np.mgrid[-1:0:20j, 0:1:20j, 0:1:20j]
s = np.sin(x*y*z + x + y*z)*(x*y*z + x + y*z)
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x,y,z,s),
                            plane_orientation='x_axes',
                            slice_index=20,line_width = 0.01,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x,y,z,s),
                            plane_orientation='y_axes',
                            slice_index=20,line_width = 0.01,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x,y,z,s),
                            plane_orientation='z_axes',
                            slice_index=20,line_width = 0.01,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='x_axes',
                            slice_index=0,line_width = 0.01,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='y_axes',
                            slice_index=0,line_width = 0.01,
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(x, y, z, s),
                            plane_orientation='z_axes',
                            slice_index=0,
                            line_width = 0.01,
                        )

# mlab.outline()
mlab.show()
# print help(mlab.pipeline.image_plane_widget)