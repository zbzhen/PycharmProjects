#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 2dmayavi
@time: 2016-02-25 22:04
"""
from enthought.mayavi import mlab
import numpy as np
from enthought.mayavi.scripts import mayavi2
#@mayavi2.standalone
def main():
    x, y = np.mgrid[0:1:21j, 0:1:21j]
    #z = 10*x*np.exp( - x**2 - y**2)
    z = 10*x*y*(x-1)*(y-1)
    pl = mlab.mesh(x, y, z)
    mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    mlab.outline(pl)
    mlab.show()
    return
if __name__ == '__main__':
     main()