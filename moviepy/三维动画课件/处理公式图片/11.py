#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 18:54
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 11.py
# @version : Python 2.7.6

from PIL import Image
import numpy as np
from mayavi import mlab
from matplotlib import pyplot as plt
from matplotlib import mathtext
parser = mathtext.MathTextParser("bitmap")
tmp,x = parser.to_mask(r'$\alpha$', dpi=120, fontsize=20)
tmp = np.where(tmp>0,1,0)
print np.shape(tmp)
# 生成公式图片再插入这个公式图片，最后删除图片
# parser.to_png('test2.jpg',r'$\alpha$'
#               , color=u'blue', fontsize=20, dpi=120)
# im = Image.open('test2.jpg')
plt.imshow(tmp*255)
plt.show()
print tmp
newim = Image.fromarray(tmp*255)
newim.show()

# im.show()
# width,height = im.size
# im = im.convert("L")
# data = im.getdata()
#
# data = np.matrix(data,dtype='float')
# new_data = np.reshape(data,(height,width))
# print new_data
# newim =  Image.fromarray(new_data)
# # newim.show()
# print width,height