#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 222.py
@time: 2016-05-02 11:51
"""
from mayavi import mlab
import numpy as np

# my dataset -simplified-
x,y,z = np.mgrid[-3:3:100j, -3:3:100j, -3:3:100j]
values = np.sqrt(x**2 + y**2 + z **2)

# my color values : the volume is divided in 3 sub-volumes along x taking
colorvalues=np.empty(values.shape)
colorvalues[0:33,:,:]=0.
colorvalues[33:66,:,:]=2.
colorvalues[66:,:,:]  =1.

src = mlab.pipeline.scalar_field(values)
src.image_data.point_data.add_array(colorvalues.T.ravel())
src.image_data.point_data.get_array(1).name = 'myID'
src.image_data.point_data.update()

# the surface i am interested on
contour = mlab.pipeline.contour(src)
contour.filter.contours= [2.8,]

# to map the ID
contour2 = mlab.pipeline.set_active_attribute(contour, point_scalars='myID')

# And we display the surface The colormap is the current attribute: the ID.
mySurf=mlab.pipeline.surface(contour2)

# I change my colormap to a discrete one : R-G-B
mySurf.module_manager.scalar_lut_manager.lut.table = np.array([[255,0,0,255],[0,255,0,255],[0,0,255,255]])

mlab.colorbar(title='ID', orientation='vertical', nb_labels=3)
mlab.show()