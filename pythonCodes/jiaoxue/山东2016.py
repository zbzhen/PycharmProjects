#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 山东2016
@time: 2016-07-09 17:51
"""
#from enthought.mayavi.scripts import mayavi2
import numpy as np
from mayavi import mlab

#为了显示透明效果，先画下面的图，再画上面的图

n = 5    #注意n=500的时候是标准错误答案！！
r = 0.5**0.5
p, a = np.mgrid[0:r:n+0j, 0:2*np.pi:n+0j]
x = p*np.cos(a)
y = p*np.sin(a)
zz = np.sqrt(x**2 + y**2)
mlab.mesh(x,y,-zz, transparent=True)


n = 500
r = 0.5
p, a = np.mgrid[0:r:n+0j, 0:2*np.pi:n+0j]
x = p*np.cos(a)
y = p*np.sin(a)
z = np.sqrt(r*r-x**2 - y**2)
#transparent=True
mlab.mesh(x,y,r-z,transparent=True)#上面的图像





#mlab.axes(xlabel='x', ylabel='y', zlabel='z')
mlab.show()