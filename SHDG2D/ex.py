#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: ex
@time: 2018/5/15  16:25
"""
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
fn = get_sample_data("lena.png", asfileobj=False)
img = read_png(fn)
x, y = ogrid[0:img.shape[0], 0:img.shape[1]]
ax = gca(projection='3d')
ax.plot_surface(x, y, 10, rstride=5, cstride=5, facecolors=img)
show()