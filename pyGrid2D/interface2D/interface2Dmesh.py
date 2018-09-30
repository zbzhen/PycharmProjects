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

def circle(r = np.sqrt(5)*0.3):
    def circleeq(x):
        rr = x[0]*x[0] + x[1]*x[1]
        return rr - r*r
    def circlepolar(t):
        x = r*np.cos(t)
        y = r*np.sin(t)
        return x,y
    return circleeq, circlepolar

def hart(a = np.sqrt(5)*0.1):
    h = 0.0
    def hartline(xx):
        x= xx[0]+a+h; y = xx[1]
        return (x**2+y**2-2*a*x)**2 - 4*a**2*(x**2+y**2)
    def hartlinepolar(t):
        x=a*(2*np.cos(t)-np.cos(2*t))
        y=a*(2*np.sin(t)-np.sin(2*t))
        return -x-h,y
    return hartline, hartlinepolar

# def kidneyline(x):
#     return (1.5*((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])-0.5*(x[0]+0.5))*\
#     	   (1.5*((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])-0.5*(x[0]+0.5))-\
#     	   1.2*((x[0]+0.5)*(x[0]+0.5)+x[1]*x[1])+0.14

# def star(a = np.sqrt(5)*0.3):
#     def starline(xx):
#         x= xx[0]; y = xx[1]
#         return -a**(2.0/3) + x**(2.0/3) + y**(2.0/3)
#     def starlinepolar(t):
#         x=a*np.cos(t)**3
#         y=a*np.sin(t)**3
#         return x,y
#     return starline, starlinepolar

if __name__ == '__main__':
    # print kidneyline([1,1])
    #Directoryname = "..//testmesh//"
    Directoryname = ""
    # datafile = "8times8_rect.dat"
    datafile = "mesh8x8_tri.dat"
    #datafile = ".//testmesh//4times4_rect.dat"
    outputdatafile = "new"+datafile
    grid = Grid2D()
    grid.from_meshdat_get_pte(Directoryname+datafile)
    p, t, e = grid.points, grid.elements, grid.bounds

    ff, ffpolar = circle()  #设置里面的曲线函数与极坐标方程

    markO, markI, markM =  getMIOelenum(grid.points.T, grid.elements,ff)
    gammatilde =  set(markO)&set(markM)
    pointsOnum = np.where(ff(grid.points.T)>0)[0]

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
    t = np.linspace(0,2*np.pi,100)
    x,y = ffpolar(t)
    axes.plot(x, y, linewidth=3, color='b')

    axes.text(x[35], y[35], "$\Gamma$", color='b', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    axes.fill(x,y, "white",alpha = 1)
    axes.fill(x,y, "g",alpha = 0.4)
    for n,i in enumerate(grid.elements[markI,:]):
        x,y = grid.points[i,:].T
        x = np.hstack((x, x[0]))
        y = np.hstack((y, y[0]))
        axes.fill(x, y, "white", alpha=1)


    for n,e in enumerate(grid.elements[markM,:]):
        pnum = set(e.tolist())&set(pointsOnum.tolist())
        x,y = grid.points[list(pnum),:].T
        axes.plot(x, y, "r", linewidth=3)
    axes.text(x[0], y[0], "$\\widetilde\Gamma$", color='r', fontsize = 35, verticalalignment='center', horizontalalignment='center')

    plotblank(axes)
    plt.savefig(Directoryname+datafile+".pdf",dip=120,bbox_inches='tight')
    plt.show()
