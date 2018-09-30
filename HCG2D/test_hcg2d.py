#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: test_hcg2d
@time: 2018/2/18  21:11
"""
import sys
sys.path.append(r'..')
import numpy as np
from Function.functionQuad import Quadrature, FuncQuad
from pyGrid2D.Grid2D import Grid2D, plotblank

from Function.interp import Interp
from hcg2d import SHCG2D



class KnownFunc(object):
    def __init__(self):
        pass

    def beta(self, x):
        return np.exp(x[0]+x[1])

    # def rhf(self, x):
    #     return 2.0*np.exp(-x[0]*x[0] - x[1]*x[1])

    # def exactsolution(self, x):
    #     return -8.0*(x[0]*x[0] + x[1]*x[1]-1.0)*np.exp(-x[0]*x[0] - x[1]*x[1])

    def exactsolution(self, x):
        r = x[0]*x[0]+x[1]*x[1]
        return np.cos(np.pi*r)

    def rhf(self, x):
        r = x[0]*x[0]+x[1]*x[1]
        uPxx = -1*(np.cos(np.pi*r)*2*np.pi*x[0]*2*np.pi*x[0] + np.sin(np.pi*r)*2*np.pi)    #u_xx
        uPyy = -1*(np.cos(np.pi*r)*2*np.pi*x[1]*2*np.pi*x[1] + np.sin(np.pi*r)*2*np.pi)    #u_yy
        u = np.cos(np.pi*r)
        return -1*(uPxx+uPyy)


    #
    # def rhf(self, x):
    #     r = x[0]*x[0]+x[1]*x[1]
    #     beta = np.exp(x[0]+x[1])
    #     betaPx = np.exp(x[0]+x[1])
    #     betaPy = np.exp(x[0]+x[1])
    #     uPx = -1*np.sin(np.pi*r)*2*np.pi*x[0];
    #     uPy = -1*np.sin(np.pi*r)*2*np.pi*x[1];
    #     uPxx = -1*(np.cos(np.pi*r)*2*np.pi*x[0]*2*np.pi*x[0] + np.sin(np.pi*r)*2*np.pi)    #u_xx
    #     uPyy = -1*(np.cos(np.pi*r)*2*np.pi*x[1]*2*np.pi*x[1] + np.sin(np.pi*r)*2*np.pi)    #u_yy
    #     u = np.cos(np.pi*r)
    #     return -1*(uPx*betaPx + uPy*betaPy + beta*(uPxx+uPyy)) + u


    def bc(self, x):
        return self.exactsolution(x)



deg = 12
# grid
grid = Grid2D()
# datafiles = ["meshRT.dat", "AddDensity_1_meshRT.dat",
#             "AddDensity_2_meshRT.dat", "AddDensity_3_meshRT.dat", "AddDensity_4_meshRT.dat"]
# datafile = datafiles[1]
# Directoryname = "..//testmesh//RT11//"

# datafile = "meshRT_0.dat"
# # datafile = "meshRTx.dat"
# Directoryname = "..//testmesh//RT01//"

Directoryname = "..//testmesh//RTdumbbell//"
datafiles = ["newRT_dumbbell_mesh1.dat", "AddDensity_1_newRT_dumbbell_mesh1.dat", "AddDensity_2_newRT_dumbbell_mesh1.dat",
             "AddDensity_3_newRT_dumbbell_mesh1.dat", "AddDensity_4_newRT_dumbbell_mesh1.dat"]
datafile = datafiles[1]

# Directoryname = "..//testmesh//rectangle01//"
# datafiles = ["meshR.dat", "meshRRR.dat", "AddDensity_1_meshRRR.dat",
#              "AddDensity_2_meshRRR.dat", "AddDensity_3_meshRRR.dat", "AddDensity_4_meshRRR.dat"]
# datafile = datafiles[1]

grid.from_meshdat_get_pte(Directoryname + datafile)
grid.readGrid()
grid.globalIndex(deg)
grid.freedomToQuad(deg)
grid.quadToFreedom(deg)
print "grid.gdof = ", grid.gdof

# L2error quadrature
L2errorquad = Quadrature(deg + 6)
L2errorquad.getGuassPointsWeights()
knownfunc = KnownFunc()

# Interpolation quadrature
interpquad = Quadrature(deg + 1)
interpquad.getLobattoPiontsWeights()
interp = Interp(interpquad.points, interpquad)

# Interpolation L2error
funcquad = FuncQuad(knownfunc.exactsolution, L2errorquad, grid, interp.ip)
print "interpolate L2error for deg = ", deg
print funcquad.interpolateL2error()

# fem solve
shcg2d = SHCG2D(knownfunc, grid, interp, interpquad)
shcg2d.solve()

print "femSolution L2error for deg = ", deg
print funcquad.femSolutionL2error(shcg2d.solution)

# from enthought.mayavi import mlab
# from Function.plotFunction import PlotFunction
# mlab.figure(bgcolor=(1.0, 1.0, 1.0), size=(400, 400))
# plotpoints = Quadrature(20)
# plotpoints.getLobattoPiontsWeights()
# plotInterp = Interp(interpquad.points, plotpoints)
# pf = PlotFunction(knownfunc.exactsolution, grid, plotInterp, mlab)
# # pf.plotInterpFunc()
# pf.plotFEMSolution(shcg2d.solution)
# # pf.plotFunc()
# mlab.show()





if deg <= 2:
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    grid.plotNodeDistribution(axes, interp.ip, pointsize=6, plotnodenum=True)
    plotblank(axes)
    plt.show()
