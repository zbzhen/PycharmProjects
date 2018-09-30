#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:03
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : femdiffusionVector2dT_test.py
# @version : Python 2.7.6
import sys
sys.path.append(r'..')
sys.path.append(r'../..')
import numpy as np
from pyGrid2D.Grid2D import Grid2D, plotblank

from Function.interp import Interp2DT
from femdiffusionVector2dT import CG2DT

class KnownFunc(object):
    def __init__(self):
        pass
    def exactsolution(self, x):
        r = x[0]*x[0]+x[1]*x[1]
        return np.cos(np.pi*r), np.sin(np.pi*r)

    def rhf(self, x):
        # return self.exactsolution(x)
        r = x[0]*x[0]+x[1]*x[1]
        uPxx = -1*(np.cos(np.pi*r)*2*np.pi*x[0]*2*np.pi*x[0] + np.sin(np.pi*r)*2*np.pi)    #u_xx
        uPyy = -1*(np.cos(np.pi*r)*2*np.pi*x[1]*2*np.pi*x[1] + np.sin(np.pi*r)*2*np.pi)    #u_yy
        uP1xx = -1*np.sin(np.pi*r)*2*np.pi*x[0]*2*np.pi*x[0] + np.cos(np.pi*r)*2*np.pi
        uP1yy = -1*np.sin(np.pi*r)*2*np.pi*x[1]*2*np.pi*x[1] + np.cos(np.pi*r)*2*np.pi
        return -1*(uPxx+uPyy), -1*(uP1xx+uP1yy)

    def bc(self, x):
        return self.exactsolution(x)



# grid
grid = Grid2D()

#
Directoryname = "..//..//testmesh//triangle01//"
datafiles = ["zeromesh1.dat","zeromesh2.dat", "zeromesh2x2.dat",
             "zeromesh4x4.dat", "zeromesh8x8.dat", "zeromesh16x16.dat", "zeromesh16x16.dat"]
datafile = datafiles[3]
# ei = [1.2767941181632623, 0.21935798845340007, 0.029828146797621767, 0.0038089447096181757, 0.00047867391058364976]
# eh = [1.248156850951234, 0.1965103332873122, 0.028488517494611728, 0.0037489738270144366, 0.0004759774821982502]
# Directoryname = "..//..//testmesh//Tdumbbell//"
# datafiles = ["newdumbbell_mesh1.dat","Add_1_newdumbbell_mesh1.dat", "Add_2_newdumbbell_mesh1.dat",
#              "Add_3_newdumbbell_mesh1.dat", "Add_4_newdumbbell_mesh1.dat"]
# datafile = datafiles[0]

grid.from_meshdat_get_pte(Directoryname + datafile)
grid.readGrid()
print Directoryname + datafile




knownfunc = KnownFunc()
interp = Interp2DT()
# fem solve
cg2dt = CG2DT(knownfunc, grid, interp)
print "Interp L2error for deg = ", 2
print cg2dt.interpL2error()

cg2dt.solve()
print "femSolution L2error for deg = ", 2
print cg2dt.L2error()


import matplotlib.pyplot as plt
# fig = plt.figure(figsize=(10,4.5), dpi=72,facecolor="white")
fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
axes = plt.subplot(111)
# grid.plotmesh2d(axes)
# plt.axis([-0.2, 3.2, -0.4, 1])
plt.axis([-0.2, 1.2, -0.2, 1.2])
cg2dt.plotuh(axes)
plotblank(axes)
plt.savefig("diffusiontest.pdf")
plt.show()


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




