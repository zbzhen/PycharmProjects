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

if __name__ == '__main__':
    # print kidneyline([1,1])
    #Directoryname = "..//testmesh//"
    Directoryname = ""
    # datafile = "8times8_rect.dat"
    datafile = "mesh8x8_tri.dat"
    #datafile = ".//testmesh//4times4_rect.dat"
    outputdatafile = "new"+datafile





    fig = plt.figure(figsize=(10,6), dpi=72,facecolor="white")
    axes = plt.subplot(111)


    ff, ffpolar = circle(1.2)  #设置里面的曲线函数与极坐标方程
    t = np.linspace(0,2*np.pi,100)
    x,y = ffpolar(t)
    axes.plot(x, y, linewidth=3, color='r')

    # axes.text(x[35], y[35], "$\Gamma$", color='b', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    axes.text(0, 0, "$S$", color='r', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    axes.text(-1.5, 0.9, "$\Omega$", color='b', fontsize = 35, verticalalignment='center', horizontalalignment='center')
    axes.text(0, 2, "$\Gamma_0$", color='g', fontsize = 35, verticalalignment='center', horizontalalignment='center')




    r = 2.5
    c = 1
    x = r*np.array([-1, 1, 1, -1, -1])*c
    y = r*np.array([-0.8, -0.8, 0.8, 0.8, -0.8])*c
    axes.plot(x, y, linewidth=3, color='g')
    axes.fill(x,y, "white",alpha = 1,hatch="\\")
    # axes.fill(x,y,hatch="\\")

    r = 2
    x = r*np.array([-1, 1, 1, -1, -1])*c
    y = r*np.array([-0.8, -0.8, 0.8, 0.8, -0.8])*c
    axes.plot(x, y, linewidth=3, color='b')
    # axes.fill(x,y, "white",alpha = 1)
    plotblank(axes)
    plt.savefig("plm.pdf",dip=120,bbox_inches='tight')
    plt.show()
    print help(axes.fill)