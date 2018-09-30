#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: pyped
@time: 2016-04-22 15:23
"""

from enthought.mayavi.scripts import mayavi2
import scipy.io as sio
import numpy as np
from mayavi import mlab

#@mayavi2.standalone
def main():
    datap = sio.loadmat("2_20p.mat")   #点
    pp = np.array(datap['p'])
    #print pp
    datat = sio.loadmat("4_24t.mat")
    tt =  datat['t'][0:-1,:]
    tt = np.array(tt) - 1
    triangles = tt.T
    #print tt
    x = pp[0]
    y = pp[1]
    z = np.zeros_like(x)
    z1 = 10*x*y*(1-x)*(1-y)
    z2 = np.zeros_like(x)
    z2[17] = 0.5
    t = np.linspace(-np.pi, np.pi, len(x)-1)  #调颜色
    t = np.r_[0, t]



    f = np.mean(t[np.array(triangles)], axis=1)

    # Plot it
    mesh = mlab.triangular_mesh(x, y, z, triangles,
                                representation='wireframe',
                                opacity=0)
    cell_data = mesh.mlab_source.dataset.cell_data
    cell_data.scalars = f
    cell_data.scalars.name = 'Cell data'
    cell_data.update()

    mesh2 = mlab.pipeline.set_active_attribute(mesh,
            cell_scalars='Cell data')
    mlab.pipeline.surface(mesh2)


    #mlab.triangular_mesh(x, y, z2, triangles, representation="wireframe",transparent=True,line_width=1.0)
    mlab.triangular_mesh(x, y, z2, triangles,transparent=True)
    #mlab.triangular_mesh(x, y, z1, triangles)
    mlab.show()
    return

if __name__ == '__main__':
     main()