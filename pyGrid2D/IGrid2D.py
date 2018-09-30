#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: IGrid2D
@time: 2018/3/4  19:36
"""
import sys
sys.path.append(r'..')
import matplotlib.pyplot as plt
from pyGrid2D.Grid2D import Grid2D, plotblank
import numpy as np



class IGrid2D(Grid2D):
    def __init__(self, levf):
        Grid2D.__init__(self)
        self.levf = levf
        pass

    def getMIOelenum(self):
        if len(np.where(self.levf(self.points.T) == 0)[0]) > 0:
            raise ValueError("grid vertex can not on interface")
        self.pointsMark = np.where(self.levf(self.points.T) > 0, 1, -1)
        markO, markI, markOf, markIf  = [], [], [], []
        for i, e in enumerate(self.elements):
            sumeleMark = self.pointsMark[e].sum()
            if sumeleMark == 3:
                markO += [i]
            elif sumeleMark == -3:
                markI += [i]
            elif sumeleMark == 1:
                markOf += [i]
            else:
                markIf += [i]
        self.outerElements = np.array(markO)
        self.innerElements = np.array(markI)
        self.ofaceElements = np.array(markOf)
        self.ifaceElements = np.array(markIf)
        return

    def findCrossoverPoint(self, indexL, indexR, Maxstep=60):
        L, R = self.points[indexL], self.points[indexR]
        if self.pointsMark[indexL]*self.pointsMark[indexR] > 0:
            raise ValueError("self.pointsMark(insexL)*self.pointsMark(indexR) can not be a positive number")
        cp = 0.5*(L+R)
        step = 0
        while step < Maxstep:
            if self.levf(L)*self.levf(cp) > 0:
                L = cp
            else:
                R = cp
            cp = 0.5*(L+R)
            step += 1
        return cp

    def getInterfaceElementCrossoverPoints(self, interfaceEleindex):
        ele = self.elements[interfaceEleindex]
        elepointsMark = self.pointsMark[ele]
        isolatedVertexLocalIndex = np.argwhere(elepointsMark == elepointsMark.prod())[0][0]
        L = ele[isolatedVertexLocalIndex]
        cp1 = self.findCrossoverPoint(L, ele[(isolatedVertexLocalIndex + 1) % 3])
        cp2 = self.findCrossoverPoint(L, ele[(isolatedVertexLocalIndex + 2) % 3])
        return cp1, cp2

if __name__ == '__main__':
###########circle######################################################
    def eq(x):
        return x[0]*x[0] + x[1]*x[1] - np.pi*np.pi*0.04
##############tuoyuan##################################################
    # def eq(x):
    #     return x[0]*x[0] + 4*x[1]*x[1] - np.pi*np.pi*0.04
################small moon#############################################
    # def eq(x):
    #     return (3*((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])-x[0]-0.5)*\
    #            (3*((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])-x[0]-0.5)-\
    #            ((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])+0.1

    Directoryname = "..//testmesh//triangle11//"
    datafiles = ["mesh2x2.dat","mesh4x4.dat", "mesh8x8.dat", "mesh16x16.dat",
                 "mesh32x32.dat", "mesh64x64.dat"]
    datafile = datafiles[2]
    grid = IGrid2D(eq)
    grid.from_meshdat_get_pte(Directoryname+datafile)
    p, t, e = grid.points, grid.elements, grid.bounds
    grid.readGrid()
    grid.getMIOelenum()


    # fig = plt.figure(figsize=(10,10), dpi=72, facecolor="white")
    # axes = plt.subplot(111)
    # grid.plotmesh2d(axes, pointsize=6, plotpointsnum=False, plotelementsnum=False, plotedgesnum=False)
    #
    #
    # for ic in grid.ofaceElements:
    #     x,y = grid.points[grid.elements[ic], :].T
    #     x = np.hstack((x, x[0]))
    #     y = np.hstack((y, y[0]))
    #     axes.fill(x, y, "g", alpha=0.7)
    #     # cp1, cp2 = grid.getInterfaceElementCrossoverPoints(ic)
    #     # axes.plot(cp1[0], cp1[1], color='black', marker='o', markerfacecolor='black', markersize=4)
    #     # axes.plot(cp2[0], cp2[1], color='black', marker='o', markerfacecolor='black', markersize=4)
    # for ic in grid.ifaceElements:
    #     x,y = grid.points[grid.elements[ic], :].T
    #     x = np.hstack((x, x[0]))
    #     y = np.hstack((y, y[0]))
    #     axes.fill(x, y, "g", alpha=0.7)
    #     # cp1, cp2 = grid.getInterfaceElementCrossoverPoints(ic)
    #     # axes.plot(cp1[0], cp1[1], color='black', marker='o', markerfacecolor='black', markersize=4)
    #     # axes.plot(cp2[0], cp2[1], color='black', marker='o', markerfacecolor='black', markersize=4)
    #
    # x = np.arange(-1,1,0.01)
    # y = np.arange(-1.,1,0.01)
    # X,Y=np.meshgrid(x,y)
    # s = eq([X,Y])
    # axes.contour(X,Y,s,[0], zorder=100)
    # #这里要修改下
    # x = np.linspace(-0.8,0.8,100)
    # # y1 = np.sqrt(np.pi*np.pi*0.04 - x*x)
    # # y2 = -1*np.sqrt(np.pi*np.pi*0.04 - x*x)
    #
    # y1 = np.sqrt(1-x*x)
    # y2 = -np.sqrt(0-(12.25*x*x+18.7578*x*x*x*x-0.5147))/np.sqrt(6.25)
    # plt.fill_between(x, y1, y2, where=y1 > y2, facecolor="g", alpha=1, interpolate=True)
    #
    # for n,i in enumerate(grid.elements[grid.innerElements,:]):
    #     x,y = grid.points[i,:].T
    #     x = np.hstack((x, x[0]))
    #     y = np.hstack((y, y[0]))
    #     axes.fill(x, y, "white", alpha=1)
    #
    #
    # for n,e in enumerate(grid.elements[grid.ofaceElements,:]):
    #     pnum = np.argwhere(grid.pointsMark[e] > 0).T[0]
    #     x,y = grid.points[e[pnum],:].T
    #     axes.plot(x, y, "r", linewidth=3)
    #
    # plotblank(axes)
    # plt.show()

    # from enthought.mayavi import mlab
    from mayavi import mlab
    from Function.plotFunction import PlotFunction
    from Function.interp import Interp
    from Function.functionQuad import Quadrature, FuncQuad

    # mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1.0, 1.0, 1.0), size=(700, 500))
    mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
    # mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1.0, 1.0, 1.0), size=(500, 700))
    # mlab.figure(bgcolor=(1.0, 1.0, 1.0), size=(400, 400))
    # def f1(x):
    #     r = x[0]*x[0]+x[1]*x[1]
    #     return np.cos(r)
    #
    # def f2(x):
    #     r = x[0]*x[0]+x[1]*x[1]
    #     return np.cos(0*r) - 2
    # def f1(x):
    #     r = x[0]*x[0]+x[1]*x[1]
    #     return np.exp(r)
    #
    # def f2(x):
    #     r = x[0]*x[0]+x[1]*x[1]
    #     return np.cos(1-r)*0.1
########circle#######################################################
    def f1(x):
        return np.sin(np.pi*x[0])*np.sin(np.pi*x[1])


    def f2(x):
        return np.exp(x[0]*x[0]+x[1]*x[1])
######tuoyuan#################################################
    # def f1(x):
    #     # r = x[0]*x[0]+x[1]*x[1]
    #     return np.sin(x[0]+x[1])+np.cos(x[0]+x[1])
    #
    #
    # def f2(x):
    #     # r = x[0]*x[0]+x[1]*x[1]
    #     return np.sin(2*x[0]*x[0]+x[1]*x[1]+2)+x[0]

#########small moon######################################################
    # def f1(x):
    #     return np.exp(x[0]+x[1]-4)-1
    #
    #
    # def f2(x):
    #     r = x[0]*x[0]+x[1]*x[1]
    #     return np.cos(1-r)

    disctf = [f1, f2]
    plotpoints = Quadrature(20)
    plotpoints.getLobattoPiontsWeights()
    plotInterp = Interp(plotpoints.points, plotpoints)

    pf = PlotFunction(f1, grid, plotInterp, mlab)
    pf.plotDiscontinuousFunc(disctf, transparent=True, vmax=7, vmin=-1, high=1)
    # pf.plotDiscontinuousFunc(disctf, transparent=True, vmax=2, vmin=-2, high=-0.15)
    # pf.plotDiscontinuousFunc(disctf, transparent=True, vmax=1.25, vmin=-1.5, high=-1)
    # pf.plotDiscontinuousFunc(disctf, transparent=True, vmax=1.25, vmin=-1.25, high=-1)
    # pf.plotUp(disctf, transparent=True, vmax=1.25, vmin=-1.25, high=-1)
    # pf.plotUa(disctf, transparent=True, vmax=1.25, vmin=-1.25, high=-1)
    # pf.plotFunc()
    # mlab.colorbar(nb_labels=6)
    mlab.colorbar()
    # mlab.savefig("111.pdf")
    mlab.show()