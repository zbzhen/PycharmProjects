#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 23:22
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : testtext.py
# @version : Python 2.7.6
from mayavi import mlab
import mayavi

# Figure specs
f = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(500, 500))

# Read a data file.
data = mlab.pipeline.open('image.vtu')

# Extract vec comp and plot
vecomp = mlab.pipeline.extract_vector_components(data)
vecomp.component = 'z-component'
surfc = mlab.pipeline.surface(vecomp, vmax=1, vmin=-1, colormap='hot')
mlab.view(elevation = 0)
t = mlab.text(0.8, 0.9, '00',  width=0.16, line_width = 1., color = (0, 0, 0))
# Save
f.scene.save('image_mayavi.png')
mlab.show()