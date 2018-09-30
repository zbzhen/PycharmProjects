 #!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 球与立方体
@time: 2016-12-31 16:33
"""

#from enthought.mayavi.scripts import mayavi2
import numpy as np
from mayavi import mlab


def plotball(core, r, n = 500):
    theta, phi = np.mgrid[0:np.pi:n+0j, 0:2*np.pi:n+0j]
    x = r*np.sin(theta)*np.cos(phi) + core[0]
    y = r*np.sin(theta)*np.sin(phi) + core[1]
    z = r*np.cos(theta) + core[2]
    mlab.mesh(x,y,z,transparent=True)
    return

R=2**0.5
#R=1

x = np.array([[-1,1,1,-1,-1],[-1,1,1,-1,-1]])
y = np.array([[-1,-1,-1,-1,-1],[1,1,1,1,1]])
z = np.array([[1,1,-1,-1,1],[1,1,-1,-1,1]])


plotball([0,0,0], R)
mlab.mesh(x,y,z,transparent=True)
mlab.show()