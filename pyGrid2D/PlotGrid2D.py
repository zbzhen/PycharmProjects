#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: PlotGrid2D
@time: 2018/5/2  17:19
"""

import numpy as np
import re
from mayavi import mlab
class PlotGrid3D(object):
    def __init__(self):
        pass
    def from_plotdat_get_pte(self, datafile):
        with open(datafile) as f:
            lines = f.readlines()
            index = 2
            while index < len(lines):
                tmp = re.findall(r"\d+\d*", str(lines[index: index+1]))
                npoints, nelements = map(int, tmp)
                index += 1
                points = np.loadtxt(lines[index:index+npoints], float)
                index += npoints
                index += nelements
                per = int(np.rint(np.cbrt(npoints)))
                z,y,x,u = points.T.reshape((4,per,per,per))
                sca = mlab.pipeline.scalar_field(x,y,z,u)
                mlab.pipeline.image_plane_widget(sca,
                                            plane_orientation='x_axes',
                                            slice_index=0,
                                        )
                mlab.pipeline.image_plane_widget(sca,
                                            plane_orientation='y_axes',
                                            slice_index=0,
                                        )
                mlab.pipeline.image_plane_widget(sca,
                                            plane_orientation='z_axes',
                                            slice_index=0,
                                        )
                mlab.pipeline.image_plane_widget(sca,
                                            plane_orientation='x_axes',
                                            slice_index=per,
                                        )
                mlab.pipeline.image_plane_widget(sca,
                                            plane_orientation='y_axes',
                                            slice_index=per,
                                        )
                mlab.pipeline.image_plane_widget(sca,
                                            plane_orientation='z_axes',
                                            slice_index=per,
                                        )
                mlab.pipeline.glyph(sca, scale_mode='none', scale_factor=.01)
                # mlab.pipeline.delaunay3d(sca)
            mlab.show()
        return

mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
a = PlotGrid3D()
a.from_plotdat_get_pte("uplot.dat")







