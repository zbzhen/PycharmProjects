#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 15:26
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : femdiffusion2dT_test.py
# @version : Python 2.7.6

import sys
sys.path.append(r'..')
sys.path.append(r'../..')
import numpy as np
from pyGrid2D.Grid2D import Grid2D, plotblank

from Function.interp import Interp2DT
from femdiffusion2dT import CG2DT

class KnownFunc(object):
    def __init__(self):
        pass

    def beta(self, x):
        return np.exp(x[0]+x[1])

    def exactsolution(self, x):
        r = x[0]*x[0]+x[1]*x[1]
        return np.cos(np.pi*r)

    def rhf(self, x):
        r = x[0]*x[0]+x[1]*x[1]
        uPxx = -1*(np.cos(np.pi*r)*2*np.pi*x[0]*2*np.pi*x[0] + np.sin(np.pi*r)*2*np.pi)    #u_xx
        uPyy = -1*(np.cos(np.pi*r)*2*np.pi*x[1]*2*np.pi*x[1] + np.sin(np.pi*r)*2*np.pi)    #u_yy
        return -1*(uPxx+uPyy)

    def bc(self, x):
        return self.exactsolution(x)



# grid
grid = Grid2D()


Directoryname = "..//..//testmesh//triangle01//"
datafiles = ["zeromesh1.dat","zeromesh2.dat", "zeromesh2x2.dat", "zeromesh4x4.dat", "zeromesh8x8.dat", "zeromesh16x16.dat"]
datafile = datafiles[5]

grid.from_meshdat_get_pte(Directoryname + datafile)
grid.readGrid()
print Directoryname + datafile

# import matplotlib.pyplot as plt
# fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
# axes = plt.subplot(111)
# grid.plotmesh2d(axes)
# plotblank(axes)
# plt.show()


knownfunc = KnownFunc()
interp = Interp2DT()
# fem solve
cg2dt = CG2DT(knownfunc, grid, interp)
print cg2dt.interpL2error()
# print cg2dt.computeLocalMatricestest(0)
cg2dt.solve()
print "femSolution L2error for deg = ", 2
print cg2dt.L2error()

# print funcquad.femSolutionL2error(cg2dt.solution)

# from enthought.mayavi import mlab
# from Function.plotFunction import PlotFunction
# mlab.figure(bgcolor=(1.0, 1.0, 1.0), size=(400, 400))
# plotpoints = Quadrature(20)
# plotpoints.getLobattoPiontsWeights()
# plotInterp = Interp(interpquad.points, plotpoints)
# pf = PlotFunction(knownfunc.exactsolution, grid, plotInterp, mlab)
# # pf.plotInterpFunc()
# # pf.plotFEMSolution(shcg2d.solution, transparent=False)
# pf.plotFunc(transparent=True, vmax=1, vmin=-1.5)
# mlab.show()






