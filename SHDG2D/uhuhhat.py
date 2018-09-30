#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: uhuhhat
@time: 2018/5/15  0:07
"""

import numpy as np
from pyGrid2D.Grid2D import Grid2D
from Function.interp import Interp
from Function.functionQuad import Quadrature
from Function.mapping import Map2D
from mayavi import mlab
from Function.plotFunction import PlotFunction
from mayavi.scripts import mayavi2
splitcoef = 0.95

class PlotHDGSketch(PlotFunction):
    def __init__(self, func, grid, interp, pl):
        PlotFunction.__init__(self, func, grid, interp, pl)
        pass
    def newplotInterpFunc(self, transparent=True, vmax=1, vmin=-1):

        # plot mesh
        for ic, ele in enumerate(self.grid.elements):
            x, y = self.grid.points[ele].T
            x = np.hstack([x, x[0]])
            y = np.hstack([y, y[0]])
            z = np.zeros_like(x)
            self.pl.plot3d(1.0*x, 1.0*y, 1.0*z, color=(0.7, 0.3, 0.9), transparent=transparent, tube_radius=0.005)

        cc = [[1.0, 0.0, 0.0],[0,0,1.0]]
        xhat = np.array(np.meshgrid(self.plotpoints, self.plotpoints))
        interpxhat = np.meshgrid(self.interp.ip, self.interp.ip)
        for ic, ele in enumerate(self.grid.elements):
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            interpx = mapping.mapping(interpxhat)
            z = np.dot((self.interp.matrixH).T, self.func(interpx))
            z = np.dot(z, self.interp.matrixH)
            cx,cy,cz = cc[ic]

            # plot node
            self.pl.points3d(interpx[0], interpx[1], self.func(interpx)+ic*0.1, color=(cx,cy,cz), scale_factor=.02)

            # plot surface
            self.pl.mesh(x, y, z+ic*0.1,transparent=False, colormap='blue-red', vmax=vmax, vmin=vmin)

            # plot node line
            for i in range(len(self.interp.ip)):
                xxhat = self.plotpoints
                yyhat = self.interp.ip[i] + 0*xxhat
                xx,yy = mapping.mapping([xxhat, yyhat])
                zz = self.func([xx,yy])
                # 下面这个是直接的函数曲线
                # self.pl.plot3d(xx, yy, zz, tube_radius=0.005
                xh = self.interp.ip
                yh = self.interp.ip[i] + 0*xh
                xxh, yyh = mapping.mapping([xh, yh])
                zh = self.func([xxh,yyh])
                zzh = np.dot([zh], self.interp.matrixH)[0]
                # 插值函数的曲线
                self.pl.plot3d(xx, yy, zzh+ic*0.1, tube_radius=0.002, transparent=True, color=(1.0, 1.0, 1.0))
            for i in range(len(self.interp.ip)):
                yyhat = self.plotpoints
                xxhat = self.interp.ip[i] + 0*yyhat
                xx,yy = mapping.mapping([xxhat, yyhat])
                zz = self.func([xx,yy])
                # 下面这个是直接的函数曲线
                # self.pl.plot3d(xx, yy, zz, tube_radius=0.005
                yh = self.interp.ip
                xh = self.interp.ip[i] + 0*yh
                xxh, yyh = mapping.mapping([xh, yh])
                zh = self.func([xxh,yyh])
                zzh = np.dot([zh], self.interp.matrixH)[0]
                # 插值函数的曲线
                self.pl.plot3d(xx, yy, zzh+ic*0.1, tube_radius=0.002, transparent=True, color=(1.0, 1.0, 1.0))

        # plot $\widehat u$
        x = np.linspace(1-splitcoef,splitcoef,100)
        y = 1-x
        # z = self.func([x,y])+0.00*np.sin(np.pi*x)
        z = self.func([x,y])
        self.pl.plot3d(x, y, z+0.05, tube_radius=0.005, transparent=True, color=(0, 0, 0))
        return


splitcoef = 0.95   # Coefficient of cellular splitting, eg splitcoef = 1 for elements hold together.
deg = 4            # Degree of interpolation polynomial

@mayavi2.standalone
def main():
    grid = Grid2D()
    pele0 = np.array([[0.0,0.0], [splitcoef, 0], [0,splitcoef]])
    pele1 = np.array([[1,1], [1-splitcoef, 1], [1,1-splitcoef]])
    p = np.vstack((pele0, pele1))
    grid.setpte(points=p, elements=[[1,2,0],[3,4,5]])


    mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))

    # set interplate points
    interpquad = Quadrature(deg + 1)
    interpquad.getLobattoPiontsWeights()
    # set plot points
    plotpoints = Quadrature(100)
    plotpoints.getLobattoPiontsWeights()

    h = 0.5
    h = 0.8
    def f(x):
        r = 1-x[0]+x[1]
        return 0.2*np.sin(np.pi*r)+ h
    plotInterp = Interp(interpquad.points, plotpoints)
    pf = PlotHDGSketch(f, grid, plotInterp, mlab)
    pf.newplotInterpFunc(vmax=0.3+h, vmin=-0.3+h)

    x = 0.5*(1-splitcoef+0.5) + 0.5*interpquad.points*(0.5-1+splitcoef)
    mlab.points3d(x, 1-x, f([x, 1-x])+0.05, scale_factor=.02, color = (0.0, 0.0, 1.0))

    x = 0.5*(splitcoef+0.5) + 0.5*interpquad.points*(splitcoef-0.5)
    mlab.points3d(x, 1-x, f([x, 1-x])+0.05, scale_factor=.02, color = (0.0, 0.0, 1.0))
    # mlab.text(0.2, 0.2, r"$K_1$")
    mlab.show()


main()