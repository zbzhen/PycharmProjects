#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: plotFunction
@time: 2018/2/15  20:46
"""
import sys
sys.path.append(r'..')
import numpy as np
from Function.mapping import Map2D
class PlotFunction(object):
    def __init__(self, func, grid, interp, pl):
        self.func = func
        self.grid = grid
        self.interp = interp
        self.plotpoints = interp.quad.points
        self.pl = pl
        pass

    def newplotInterpFunc(self, transparent=True, vmax=1, vmin=-1):
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
            # self.pl.points3d(interpx[0], interpx[1], self.func(interpx)-ic*0.04*np.sin(np.pi*interpx[0]), color=(cx,cy,cz), scale_factor=.02)
            self.pl.points3d(interpx[0], interpx[1], self.func(interpx), color=(cx,cy,cz), scale_factor=.02)
            self.pl.mesh(x, y, z,transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            # self.pl.mesh(x, y, z-ic*0.04*np.sin(np.pi*x),transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            # self.pl.mesh(x, y, z-ic*0.04*np.sin(np.pi*x),representation="wireframe", colormap='blue-red', vmax=vmax, vmin=vmin)
            # self.pl.mesh(interpx[0], interpx[1], self.func(interpx)-ic*0.04*np.sin(np.pi*interpx[0]),representation="wireframe",transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
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
                self.pl.plot3d(xx, yy, zzh, tube_radius=0.0008)
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
                self.pl.plot3d(xx, yy, zzh, tube_radius=0.0008, transparent=True)

        # plot $\widehat u$
        x = np.linspace(0,1,50)
        y = 1-x
        z = self.func([x,y])+0.00*np.sin(np.pi*x)
        self.pl.plot3d(x, y, z, tube_radius=0.005, transparent=True)

        return


    def plotInterpFunc(self, transparent=True, vmax=1, vmin=-1):
        for ic, ele in enumerate(self.grid.elements):
            x, y = self.grid.points[ele].T
            x = np.hstack([x, x[0]])
            y = np.hstack([y, y[0]])
            z = np.zeros_like(x)
            self.pl.plot3d(x, y, z, line_width=1.0, color=(0.7, 0.3, 0.9), transparent=transparent, tube_radius=0.005)
        xhat = np.array(np.meshgrid(self.plotpoints, self.plotpoints))
        interpxhat = np.meshgrid(self.interp.ip, self.interp.ip)
        for ic, ele in enumerate(self.grid.elements):
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            interpx = mapping.mapping(interpxhat)
            z = np.dot((self.interp.matrixH).T, self.func(interpx))
            z = np.dot(z, self.interp.matrixH)
            self.pl.mesh(x, y, z, transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        return

    def plotFEMSolution(self, uh, transparent=True, vmax=1, vmin=-1, plotmesh=True):
        if plotmesh == True:
            for ic, ele in enumerate(self.grid.elements):
                x, y = self.grid.points[ele].T
                x = np.hstack([x, x[0]])
                y = np.hstack([y, y[0]])
                z = np.zeros_like(x)
                self.pl.plot3d(x, y, z, line_width=1.0, color=(0.7, 0.3, 0.9), transparent=transparent, tube_radius=0.005)
        xhat = np.array(np.meshgrid(self.plotpoints, self.plotpoints))
        uhdim = uh.ndim
        quadtofree = self.grid.quadtofree
        de = self.interp.pp
        tmp = np.zeros((de, de))
        for ic, ele in enumerate(self.grid.elements):
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            if uhdim == 1:
                for j in range(de*de):
                    jx, jy = j / de, j % de
                    J = quadtofree[j]
                    tmp[jx][jy] = uh[self.grid.gindex[ic][J]]
            elif uhdim == 2:
                tmp = np.reshape(uh[ic], (de, de))
            else:
                tmp = uh[ic]
            z = np.dot((self.interp.matrixH).T, tmp)
            z = np.dot(z, self.interp.matrixH)
            self.pl.mesh(x, y, z, transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        return

    def plotFunc(self, transparent=True, vmax=1, vmin=-1):
        for ic, ele in enumerate(self.grid.elements):
            x, y = self.grid.points[ele].T
            x = np.hstack([x, x[0]])
            y = np.hstack([y, y[0]])
            z = np.zeros_like(x)
            self.pl.plot3d(x, y, z, line_width=1.0, color=(0.7, 0.3, 0.9), transparent=transparent, tube_radius=0.005)
        xhat = np.array(np.meshgrid(self.plotpoints, self.plotpoints))
        for ic, ele in enumerate(self.grid.elements):
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, self.func([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        return

    def plotDiscontinuousFunc(self, disctFunc, transparent=True, vmax=1, vmin=-1, high=0):
        for ele in self.grid.elements:
            x, y = self.grid.points[ele].T
            x = np.hstack([x, x[0]])
            y = np.hstack([y, y[0]])
            z = np.zeros_like(x) + high
            self.pl.plot3d(x, y, z, line_width=0.1, color=(0.7, 0.3, 0.9), transparent=False, tube_radius=0.005)

        for n,e in enumerate(self.grid.elements[self.grid.ofaceElements,:]):
            pnum = np.argwhere(self.grid.pointsMark[e] > 0).T[0]
            x, y = self.grid.points[e[pnum], :].T
            z = np.zeros_like(x) + high
            self.pl.plot3d(x, y, z, line_width=0.1, color=(0, 0, 0), transparent=False, tube_radius=0.008)


        xhat = np.array(np.meshgrid(self.plotpoints, self.plotpoints))
        for ic in self.grid.innerElements:
            ele = self.grid.elements[ic]
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        for ic in self.grid.outerElements:
            ele = self.grid.elements[ic]
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        for ic in self.grid.ifaceElements:
            ele = self.grid.elements[ic]
            elepointsMark = self.grid.pointsMark[ele]
            iv = np.argwhere(elepointsMark == elepointsMark.prod())[0][0]
            cp1, cp2 = self.grid.getInterfaceElementCrossoverPoints(ic)
            mapping = Map2D([self.grid.points[ele[iv]], cp1, cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            mapping = Map2D([cp1, self.grid.points[ele[(iv+1) % 3]], self.grid.points[ele[(iv+2) % 3]], cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)

        for ic in self.grid.ofaceElements:
            ele = self.grid.elements[ic]
            elepointsMark = self.grid.pointsMark[ele]
            iv = np.argwhere(elepointsMark == elepointsMark.prod())[0][0]
            cp1, cp2 = self.grid.getInterfaceElementCrossoverPoints(ic)
            mapping = Map2D([self.grid.points[ele[iv]], cp1, cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            mapping = Map2D([cp1, self.grid.points[ele[(iv+1) % 3]], self.grid.points[ele[(iv+2) % 3]], cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)

        return


    def plotUa(self, disctFunc, transparent=True, vmax=1, vmin=-1, high=0):
        for ele in self.grid.elements:
            x, y = self.grid.points[ele].T
            x = np.hstack([x, x[0]])
            y = np.hstack([y, y[0]])
            z = np.zeros_like(x) + high
            self.pl.plot3d(x, y, z, line_width=0.1, color=(0.7, 0.3, 0.9), transparent=False, tube_radius=0.005)

        for n,e in enumerate(self.grid.elements[self.grid.ofaceElements, :]):
            pnum = np.argwhere(self.grid.pointsMark[e] > 0).T[0]
            x, y = self.grid.points[e[pnum], :].T
            z = np.zeros_like(x) + high
            self.pl.plot3d(x, y, z, line_width=0.1, color=(0, 0, 0), transparent=False, tube_radius=0.008)


        xhat = np.array(np.meshgrid(self.plotpoints, self.plotpoints))
        for ic in self.grid.innerElements:
            ele = self.grid.elements[ic]
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        for ic in self.grid.outerElements:
            ele = self.grid.elements[ic]
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        for ic in self.grid.ifaceElements:
            ele = self.grid.elements[ic]
            elepointsMark = self.grid.pointsMark[ele]
            iv = np.argwhere(elepointsMark == elepointsMark.prod())[0][0]
            cp1, cp2 = self.grid.getInterfaceElementCrossoverPoints(ic)
            mapping = Map2D([self.grid.points[ele[iv]], cp1, cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            mapping = Map2D([cp1, self.grid.points[ele[(iv+1) % 3]], self.grid.points[ele[(iv+2) % 3]], cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)

        for ic in self.grid.ofaceElements:
            ele = self.grid.elements[ic]
            elepointsMark = self.grid.pointsMark[ele]
            iv = np.argwhere(elepointsMark == elepointsMark.prod())[0][0]
            cp1, cp2 = self.grid.getInterfaceElementCrossoverPoints(ic)
            mapping = Map2D([self.grid.points[ele[iv]], cp1, cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            mapping = Map2D([cp1, self.grid.points[ele[(iv+1) % 3]], self.grid.points[ele[(iv+2) % 3]], cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)

        return

    def plotUp(self, disctFunc, transparent=True, vmax=1, vmin=-1, high=0):
        for ele in self.grid.elements:
            x, y = self.grid.points[ele].T
            x = np.hstack([x, x[0]])
            y = np.hstack([y, y[0]])
            z = np.zeros_like(x) + high
            self.pl.plot3d(x, y, z, line_width=10, color=(0.7, 0.3, 0.9), transparent=False, tube_radius=0.005)

        for n,e in enumerate(self.grid.elements[self.grid.ofaceElements,:]):
            pnum = np.argwhere(self.grid.pointsMark[e] > 0).T[0]
            x, y = self.grid.points[e[pnum], :].T
            z = np.zeros_like(x) + high
            self.pl.plot3d(x, y, z, line_width=0.1, color=(0, 0, 0), transparent=False, tube_radius=0.008)


        xhat = np.array(np.meshgrid(self.plotpoints, self.plotpoints))
        for ic in self.grid.innerElements:
            ele = self.grid.elements[ic]
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        for ic in self.grid.outerElements:
            ele = self.grid.elements[ic]
            mapping = Map2D(self.grid.points[ele])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[1]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
        for ic in self.grid.ifaceElements:
            ele = self.grid.elements[ic]
            elepointsMark = self.grid.pointsMark[ele]
            iv = np.argwhere(elepointsMark == elepointsMark.prod())[0][0]
            cp1, cp2 = self.grid.getInterfaceElementCrossoverPoints(ic)
            mapping = Map2D([self.grid.points[ele[iv]], cp1, cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            mapping = Map2D([cp1, self.grid.points[ele[(iv+1) % 3]], self.grid.points[ele[(iv+2) % 3]], cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)

        for ic in self.grid.ofaceElements:
            ele = self.grid.elements[ic]
            elepointsMark = self.grid.pointsMark[ele]
            iv = np.argwhere(elepointsMark == elepointsMark.prod())[0][0]
            cp1, cp2 = self.grid.getInterfaceElementCrossoverPoints(ic)
            mapping = Map2D([self.grid.points[ele[iv]], cp1, cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)
            mapping = Map2D([cp1, self.grid.points[ele[(iv+1) % 3]], self.grid.points[ele[(iv+2) % 3]], cp2])
            x, y = mapping.mapping(xhat)
            self.pl.mesh(x, y, disctFunc[0]([x,y]), transparent=transparent, colormap='blue-red', vmax=vmax, vmin=vmin)

        return