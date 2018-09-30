#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: test_hdg2dT
@time: 2018/2/25  20:43
"""
import sys
sys.path.append(r'..')
from hdg2dT import SHDG2D
import numpy as np
from pyGrid2D.Grid2D import Grid2D, plotblank
from Function.interp import Interp
from Function.functionQuad import Quadrature, FuncQuad


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



deg = 6
grid = Grid2D()

# Directoryname = "..//testmesh//Tdumbbell//"
# datafiles = ["newdumbbell_mesh1.dat", "Add_1_newdumbbell_mesh1.dat", "Add_2_newdumbbell_mesh1.dat",
#              "Add_3_newdumbbell_mesh1.dat", "Add_4_newdumbbell_mesh1.dat"]
# datafile = datafiles[2]

Directoryname = "..//testmesh//triangle01//"
datafiles = ["zeromesh2x2.dat","zeromesh4x4.dat", "zeromesh8x8.dat", "zeromesh16x16.dat",
             "zeromesh32x32.dat", "zeromesh64x64.dat"]
datafile = datafiles[0]
# datafile = "zeromesh1.dat"
#
# Directoryname = "..//testmesh//triangle11//"
# datafiles = ["mesh2x2.dat","mesh4x4.dat", "mesh8x8.dat", "mesh16x16.dat",
#              "mesh32x32.dat", "mesh64x64.dat"]
# datafile = datafiles[0]

print Directoryname + datafile
grid.from_meshdat_get_pte(Directoryname + datafile)
grid.readGrid()
grid.freedomToQuad(deg)
grid.quadToFreedom(deg)
print "grid.tgdof = ", grid.Nedge*2*(deg+1)


# L2error quadrature
L2errorquad = Quadrature(deg + 5)
L2errorquad.getGuassPointsWeights()
knownfunc = KnownFunc()

# Interpolation quadrature
interpquad = Quadrature(deg + 1)
interpquad.getLobattoPiontsWeights()
interp = Interp(interpquad.points, L2errorquad)

# Interpolation L2error
funcquad = FuncQuad(knownfunc.exactsolution, L2errorquad, grid, interp.ip)
print "interpolate L2error for deg = ", deg
print funcquad.interpolateL2error()

# fem solve
# shdg2d = SHDG2D(knownfunc, grid, interp, L2errorquad)
# shdg2d.solve()
#
# print "femSolution L2error for deg = ", deg
# du = (deg+1)*(deg+1)
# dq = 2*du
# uh = shdg2d.solution[:, dq:]
# uh = uh*0
# uh[6][6] = 1
# uh[6][4] = 1
# uh[6][0] = 1
# uh[6][-1] = 1
# uh[6][-2] = 1
# print funcquad.femSolutionL2error(uh)


# from enthought.mayavi import mlab
# from mayavi import mlab
# from Function.plotFunction import PlotFunction
# mlab.figure(bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
# plotpoints = Quadrature(100)
# plotpoints.getLobattoPiontsWeights()
# plotInterp = Interp(interpquad.points, plotpoints)
# pf = PlotFunction(knownfunc.exactsolution, grid, plotInterp, mlab)
# # pf.plotInterpFunc()
# pf.plotFEMSolution(uh, plotmesh=True)
# # pf.plotFunc()
# mlab.show()

ftz = 26
if deg <= 8:
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    # grid.elements[1] = np.array([grid.elements[1][1], grid.elements[1][2], grid.elements[1][0]])

    # grid.plotNodeDistribution(axes, interp.ip, plotnodenum=False, pointsize=5, ftz=30, linewidth=5)
    grid.plotmesh2d(axes, pointsize=6, plotpointsnum=False, plotelementsnum=True, plotedgesnum=False)
    # axes.text(0.51, 0.5, str(2), color='blue', fontsize=ftz, verticalalignment='bottom', horizontalalignment='left')
    # axes.text(0.51, 0.636, str(1), color='blue', fontsize=ftz, verticalalignment='top', horizontalalignment='left')
    # axes.text(0.82, 0.586, str(3), color='blue', fontsize=ftz, verticalalignment='top', horizontalalignment='left')
    # axes.text(0.751, 0.75, str(4), color='blue', fontsize=ftz, verticalalignment='bottom', horizontalalignment='left')
    # axes.text(0.674, 0.814, str(5), color='blue', fontsize=ftz, verticalalignment='top', horizontalalignment='right')
    plotblank(axes)

    x = np.array([0.05, 0.45])
    y = np.array([0, 0])
    xx = np.array([0.02, 0.23])
    linewidth = 5
    # plt.plot(x, y, "g", linewidth=linewidth)
    # plt.plot(x+0.5, y, "g", linewidth=linewidth)
    plt.plot(xx, y+1, "g", linewidth=linewidth)
    plt.plot(xx+0.25, y+1, "g", linewidth=linewidth)

    ### plt.plot(xx, y+0.5, "r", linewidth=linewidth)
    ### plt.plot(xx+0.25, y+0.5, "r", linewidth=linewidth)
    # plt.plot(x, y+0.5, "g", linewidth=linewidth)

    plt.plot(xx+0.5, y+1, "g", linewidth=linewidth)
    plt.plot(xx+0.75, y+1, "g", linewidth=linewidth)
    plt.plot(xx+0.5, y+0.5, "r", linewidth=linewidth)
    plt.plot(xx+0.75, y+0.5, "r", linewidth=linewidth)
    t = np.array([0.03, 0.23])
    plt.plot(t, 1-t, "r", linewidth=linewidth)   ##
    plt.plot(t, 0.5-t, "g", linewidth=linewidth)
    plt.plot(t+0.25, 1-t-0.25, "r", linewidth=linewidth)
    plt.plot(t+0.25, 0.5-t-0.25, "g", linewidth=linewidth) ##
    plt.plot(t+0.5, 1-t, "r", linewidth=linewidth)
    plt.plot(t+0.5, 0.5-t, "r", linewidth=linewidth)
    plt.plot(t+0.75, 1-t-0.25, "r", linewidth=linewidth)
    plt.plot(t+0.75, 0.5-t-0.25, "r", linewidth=linewidth)
    # plt.plot(y, x, "g", linewidth=linewidth)
    # plt.plot(y+0.5, x, "g", linewidth=linewidth)
    # plt.plot(y+1, x, "g", linewidth=linewidth)
    # plt.plot(y, x+0.5, "g", linewidth=linewidth)
    # plt.plot(y+0.5, x+0.5, "g", linewidth=linewidth)
    # plt.plot(y+1, x+0.5, "g", linewidth=linewidth)
    plt.savefig("motarrededge.pdf")


    # plt.savefig("deg6Tnode.pdf")
    plt.show()


