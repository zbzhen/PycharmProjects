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
    O, I, M = pointsOnum[0].tolist(), pointsInum[0].tolist(), pointsMnum[0].tolist()
    markO = []
    markI = []
    markM = []
    for i,e in enumerate(elements):
        if set(e.tolist())&set(O) == set(e.tolist()):
            markO += [i]
        elif set(e.tolist())&set(I) == set(e.tolist()):
            markI += [i]
        else:
            markM += [i]
    #return set(range(len(points)))-set(markO) - set(markI)
    return markO, markI, markM


def eq(x):
    return (3*((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])-x[0]-0.5)*\
    	   (3*((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])-x[0]-0.5)-\
    	   ((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])+0.1
    # return x[0]*x[0] + 4*x[1]*x[1] - np.pi*np.pi*0.04
    # return 5*x[1]*x[1] -9*x[0]*x[0]+20*x[0]*x[0]*x[0]*x[0]-0.5
    # return 6.25*x[1]*x[1] -12.25*x[0]*x[0]+18.7578*x[0]*x[0]*x[0]*x[0]-0.5147


if __name__ == '__main__':
    # print kidneyline([1,1])
    #Directoryname = "..//testmesh//"
    Directoryname = ""
    datafile = "8times8_rect.dat"
    # datafile = "mesh16x16_tri.dat"
    # datafile = "mesh32x32.dat"
    #datafile = ".//testmesh//4times4_rect.dat"
    outputdatafile = "yuan"+datafile
    grid = Grid2D()
    grid.from_meshdat_get_pte(Directoryname+datafile)
    p, t, e = grid.points, grid.elements, grid.bounds



    markO, markI, markM =  getMIOelenum(grid.points.T, grid.elements,eq)
    gammatilde =  set(markO)&set(markM)
    pointsOnum = np.where(eq(grid.points.T)>0)[0]

    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    grid.plotmesh2d(axes, pointsize=3, ftz=15,plotpointsnum="n", plotelementsnum="n", plotedgesnum="n")




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
    s = eq([X,Y])
    axes.contour(X,Y,s,[0], zorder=100)

    # cmap = plt.get_cmap('PiYG')
    # axes.contourf(X,Y,s<0,zorder=200)

    #这里要修改下
    x = np.linspace(-0.8,0.8,100)
    # y1 = 0.5*np.sqrt(np.pi*np.pi*0.04 - x*x)
    # y2 = -0.5*np.sqrt(np.pi*np.pi*0.04 - x*x)
    y1 = np.sqrt(1-x*x)
    y2 = -np.sqrt(0-(12.25*x*x+18.7578*x*x*x*x-0.5147))/np.sqrt(6.25)
    plt.fill_between(x, y1, y2, where= y1 > y2, facecolor = "white",alpha = 1, interpolate= True)
    plt.fill_between(x, y1, y2, where= y1 > y2, facecolor = "g",alpha = 1, interpolate= True)
    axes.plot(x, y1, linewidth=3, color='b')
    # axes.fill(x,y, "white",alpha = 1)
    # axes.fill(x,y, "g",alpha = 0.4)
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
    # axes.text(-0.6, 0.1, "$\Omega_c^1$", color='w', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    # axes.text(-0.83, 0.4, "$\\widetilde\Gamma$", color='r', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    # axes.text(-0.4, -0.54, "$\Gamma$", color='w', fontsize = 35, verticalalignment='center', horizontalalignment='center')

    plotblank(axes)
    plt.savefig(Directoryname+"xiaoyueliang1.pdf",dip=120,bbox_inches='tight')
    plt.show()
    # help(axes.contourf)