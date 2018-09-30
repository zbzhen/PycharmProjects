#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 16:14
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : femNS2dT_test.py
# @version : Python 2.7.6
import sys
sys.path.append(r'..')
sys.path.append(r'../..')
import numpy as np
from pyGrid2D.Grid2D import Grid2D, plotblank

from Function.interp import Interp2DT
from femNS2dT import CG2DT

class KnownFunc(object):
    def __init__(self):
        pass
    def exactsolutionp(self, x):
        # return 0*x[0]
        # return np.sin(2*np.pi*x[0]) + np.sin(2*np.pi*x[1])
        # return np.exp(x[0]+x[1])
        return (x[0]-0.5)**3*(x[1]-0.5)**3

    def exactsolution(self, x):
        # return 0*x[0], 0*x[0]
        return np.exp(x[0]-x[1]), np.exp(x[0]-x[1])

    def rhf(self, x):
        # return self.exactsolution(x)
        uPxx = np.exp(x[0]-x[1])    #u_xx
        uPyy = np.exp(x[0]-x[1])    #u_yy
        uP1xx = np.exp(x[0]-x[1])
        uP1yy = np.exp(x[0]-x[1])
        dpx = 10*(1-2*x[0])*x[1]*(1-x[1])
        dpy = 10*x[0]*(1-x[0])*(1-2*x[1])
        dpx = 2*np.pi*np.cos(2*np.pi*x[0])
        dpy = 2*np.pi*np.cos(2*np.pi*x[1])
        dpx = np.exp(x[0]+x[1])
        dpy = np.exp(x[0]+x[1])
        dpx = 3*(x[0]-0.5)**2*(x[1]-0.5)**3
        dpy = 3*(x[0]-0.5)**3*(x[1]-0.5)**2
        # return dpx, dpy
        return -1*(uPxx+uPyy) + dpx, -1*(uP1xx+uP1yy) + dpy

    def bc(self, x):
        return self.exactsolution(x)

class KnownFunc1(object):
    def __init__(self):
        pass
    def exactsolutionp(self, x):
        return 0*x[0]

    def exactsolution(self, x):
        r = np.pi*(x[0]+x[1])
        return np.cos(r), np.sin(r)

    def rhf(self, x):
        return 0*x[0], 0*x[0]
        r = np.pi*(x[0]+x[1])
        uPxx = -np.pi*np.pi*np.cos(r)   #u_xx
        uPyy = -np.pi*np.pi*np.cos(r)    #u_yy
        uP1xx = -np.pi*np.pi*np.sin(r)
        uP1yy = -np.pi*np.pi*np.sin(r)
        dp = 0
        return -1*(uPxx+uPyy) + dp, -1*(uP1xx+uP1yy) + dp

    def bc(self, x):
        u2 = 0*x[0]
        f1 = 0*x[0]
        f2 = 0*x[0] + 1
        u1 = np.where(x[1]==1, f2, f1)
        return u1, u2
        return self.exactsolution(x)

# grid
grid = Grid2D()

#
ui = [0.24274544331941067]
uh = [2.9367610693918063]
Directoryname = "..//..//testmesh//triangle01//"
datafiles = ["zeromesh1.dat","zeromesh2.dat", "zeromesh2x2.dat",
             "zeromesh4x4.dat", "zeromesh8x8.dat", "zeromesh16x16.dat", "zeromesh32x32.dat","zeromesh64x64.dat"]
datafile = datafiles[6]
##----------------------------------------------
# ei = [1.2767941181632623, 0.21935798845340007, 0.029828146797621767, 0.0038089447096181757, 0.00047867391058364976]
# Directoryname = "..//..//testmesh//Tdumbbell//"
# datafiles = ["newdumbbell_mesh1.dat","Add_1_newdumbbell_mesh1.dat", "Add_2_newdumbbell_mesh1.dat",
#              "Add_3_newdumbbell_mesh1.dat", "Add_4_newdumbbell_mesh1.dat"]
# datafile = datafiles[0]
##----------------------------------------------
grid.from_meshdat_get_pte(Directoryname + datafile)
grid.readGrid()
print Directoryname + datafile




knownfunc = KnownFunc()
interp = Interp2DT()
# fem solve
cg2dt = CG2DT(knownfunc, grid, interp)

print "Interp u L2error for deg = ", 2
print cg2dt.interpL2errorU()
print "Interp p L2error for deg = ", 1
print cg2dt.interpL2errorp()
cg2dt.solve()
# print cg2dt.solution
print "femSolution uh L2error for deg = ", 2
print cg2dt.L2errorU()
print "femSolution ph L2error for deg = ", 1
print cg2dt.L2errorp()

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,8), dpi=72,facecolor="white")
axes = plt.subplot(111)
# grid.plotmesh2d(axes)
plt.axis([-0.2, 1.2, -0.2, 1.2])
cg2dt.plotuh(axes)
plotblank(axes)
plt.savefig("NStest.pdf")
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



