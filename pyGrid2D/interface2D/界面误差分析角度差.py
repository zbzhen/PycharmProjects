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
# from pyGrid2D.Grid2D import Grid2D, plotblank
import numpy as np


def plotc(R, axes, c=[0,0], t=[0,2*np.pi]):
    theta = np.linspace(t[0],t[1],200)
    x = R*np.cos(theta)
    y = R*np.sin(theta)
    axes.plot(x+c[0], y+c[1])
    return


if __name__ == '__main__':
    fig = plt.figure(figsize=(9,4.5), dpi=72,facecolor="white")
    # fig = plt.figure(dpi=72,facecolor="white")
    axes = plt.subplot(111)

    plt.xlim(-1, 5)
    plt.ylim(-1.04, 2)
    axes.plot([0,0],[-1,1.8], "black")
    axes.plot([-1,4.5],[0,0], "black")


    axes.annotate("",(4.51,0),(4.5,0),arrowprops={"arrowstyle": "->"})
    axes.annotate("",(0,1.81),(0,1.8),arrowprops={"arrowstyle": "->"})
    plt.text(4.5,-0.3,r'$x$',color="blue",fontsize=30,ha="center")
    plt.text(0.2,1.6,r'$y$',color="blue",fontsize=30,ha="center")

    Directoryname = ""
    datafile = "alphah"

    c = [2,-1]
    R = np.sqrt(c[0]*c[0]+ c[1]*c[1])
    plotc(R, axes, c, t=[0, np.pi])


    plotc(0.5, axes, t=[0, np.pi/6])
    plotc(0.8, axes, t=[np.pi/6, np.arctan(2)])
    plotc(0.8, axes, t=[-np.arctan(0.5),0])

    axes.plot(c[0],c[1],"*")
    # axes.plot(0,0,"*")
    axes.plot([0,0.8],[0,1.6], "black")

    axes.plot([0,2.13],[0,2.13/np.sqrt(3)], "red", lw=1.5 )

    axes.plot([0,c[0]],[0,c[1]], "black")



    plt.text(0.75,0.1,r'$\theta$',color="blue",fontsize=30,ha="center")
    plt.text(0.75,0.6,r'$\alpha$',color="blue",fontsize=30,ha="center")
    plt.text(1.4,0.6,r'$\rho$',color="blue",fontsize=30,ha="center")
    plt.text(2.3,-0.35,r'$S_r^h$',color="blue",fontsize=30,ha="center")
    plt.text(0.9,-0.8,r'$R$',color="blue",fontsize=30,ha="center")
    plt.text(0.96,-0.26,r'$\varphi$',color="blue",fontsize=30,ha="center")

    # axes.annotate('$y$',(-0.04, -1), (-0.04, 2),
    #               fontsize = 30,
    #             arrowprops={"arrowstyle":"<-"})
    #
    # axes.annotate('$x$', (-1, -0.02), (5, -0.02),
    #               fontsize = 30,
    #             arrowprops={"arrowstyle":"<-"})
    axes.set_xticks([])
    axes.set_yticks([])
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['bottom'].set_color('none')
    axes.spines['left'].set_color('none')
    plt.savefig(Directoryname+datafile+".pdf",dip=120,bbox_inches='tight')
    plt.show()
