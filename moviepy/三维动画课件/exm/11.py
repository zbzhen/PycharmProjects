#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 15:58
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 11.py
# @version : Python 2.7.6
from PIL import Image
import numpy as np
from mayavi import mlab
im = Image.open('11.png')
# 显示图片
# im.show()

width,height = im.size
im = im.convert("L")
data = im.getdata()
print data
data = np.matrix(data,dtype='float')

new_data = np.reshape(data,(height,width))/255.
print im.size
for i in range(20):
    new_data[i*5:(i+1)*5]=0.05*i


# print new_data
# newim =  Image.fromarray(new_data)
# newim.show()
fig =mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(400, 400))
# mlab.pipeline.array2d_source(new_data, figure=fig)
mlab.imshow(new_data, vmin=0, vmax=1)
# mlab.points3d(0, 0, 0, scale_factor=8, figure=fig)
# mlab.points3d(1, 1, 0, scale_factor=8, figure=fig)
# mlab.imshow(1, 1, new_data, colormap='gist_earth')
mlab.show()