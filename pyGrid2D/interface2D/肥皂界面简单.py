#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: interface2Dmesh
@time: 2017-03-27 16:46
"""
import matplotlib.pyplot as plt
from pyGrid2D.Grid2D_2 import Grid2D, plotblank
import numpy as np

def getMIOelenum(points, elements, func):
    pointsOnum = np.where(func(points)>0)
    pointsInum = np.where(func(points)<0)
    pointsMnum = np.where(func(points)==0)
    O, I, M = pointsOnum[0], pointsInum[0], pointsMnum[0]
    markO = []
    markI = []
    markM = []
    for i,e in enumerate(elements):
        if set(e.tolist())&set(O.tolist()) == set(e.tolist()):
            markO += [i]
        elif set(e.tolist())&set(I.tolist()) == set(e.tolist()):
            markI += [i]
        else:
            markM += [i]
    #return set(range(len(points)))-set(markO) - set(markI)
    return markO, markI, markM


def feizao(x):
    return 5*x[1]*x[1] -9*x[0]*x[0]+20*x[0]*x[0]*x[0]*x[0]-0.5
    # return 6.25*x[1]*x[1] -12.25*x[0]*x[0]+18.7578*x[0]*x[0]*x[0]*x[0]-0.5147


if __name__ == '__main__':
    # print kidneyline([1,1])
    #Directoryname = "..//testmesh//"
    Directoryname = ""
    # datafile = "8times8_rect.dat"
    datafile = "mesh8x8_tri.dat"
    #datafile = ".//testmesh//4times4_rect.dat"
    outputdatafile = "feizao"+datafile
    grid = Grid2D()
    grid.from_meshdat_get_pte(Directoryname+datafile)
    p, t, e = grid.points, grid.elements, grid.bounds



    markO, markI, markM =  getMIOelenum(grid.points.T, grid.elements,feizao)
    gammatilde =  set(markO)&set(markM)
    pointsOnum = np.where(feizao(grid.points.T)>0)[0]

    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    grid.plotmesh2d(axes, pointsize=3, ftz=15,plotpointsnum="n", plotelementsnum="n")




    for n,i in enumerate(grid.elements[markM,:]):
        x,y = grid.points[i,:].T
        x = np.hstack((x, x[0]))
        y = np.hstack((y, y[0]))
        axes.fill(x, y, "g", alpha=0.7)

        # x,y = grid.points[i,:].T
        # x,y = sum(x)*1.0/len(x),  sum(y)*1.0/len(y)
        # axes.text(x, y, str(n), color='red', fontsize = 15, verticalalignment='center', horizontalalignment='center')

    x = np.arange(-1,1,0.01)
    y = np.arange(-1.,1,0.01)
    X,Y=np.meshgrid(x,y)
    s = feizao([X,Y])
    axes.contour(X,Y,s,[0],zorder=100)

    # cmap = plt.get_cmap('PiYG')
    # axes.contourf(X,Y,s<0,zorder=200)

    x = np.linspace(-0.8,0.8,100)
    y1 = np.sqrt(0-(-9*x*x+20*x*x*x*x-0.5)/5)
    y2 = -1*np.sqrt(0-(-9*x*x+20*x*x*x*x-0.5)/5)

    # plt.fill_between(x, y1, y2, where= y1 > y2, facecolor = "g",alpha = 1, interpolate= True)

    for n,i in enumerate(grid.elements[markI,:]):
        x,y = grid.points[i,:].T
        x = np.hstack((x, x[0]))
        y = np.hstack((y, y[0]))
        axes.fill(x, y, "white", alpha=1)


    for n,e in enumerate(grid.elements[markM,:]):
        pnum = set(e.tolist())&set(pointsOnum.tolist())
        x,y = grid.points[list(pnum),:].T
        axes.plot(x, y, "r", linewidth=3)

    # axes.text(-0.63, 0.61, "$\Omega_c^2$", color='w', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    axes.text(-0.6, 0.1, "$\mathcal{T}_{h,c}$", color='w', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    # axes.text(-0.83, 0.4, "$\\widetilde\Gamma$", color='r', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    axes.text(-0.4, -0.54, "$\Gamma$", color='w', fontsize = 35, verticalalignment='center', horizontalalignment='center')

    plotblank(axes)
    plt.savefig(Directoryname+"feizao0.pdf",dip=120,bbox_inches='tight')
    plt.show()
    # help(axes.contourf)