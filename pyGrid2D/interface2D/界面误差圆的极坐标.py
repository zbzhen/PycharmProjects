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
    plt.ylim(-1, 2)
    axes.plot([0,0],[-0.2,1.8], "black")
    axes.plot([-0.2,4.5],[0,0], "black")
    axes.plot([0,np.pi],[1.2,0], "black")
    axes.plot([0,0.5*np.pi],[0.6,0.6], linestyle="dashed")
    axes.plot([0.5*np.pi,0.5*np.pi],[0,0.6], linestyle="dashed")


    axes.annotate("",(4.51,0),(4.5,0),arrowprops={"arrowstyle": "->"})
    axes.annotate("",(0,1.81),(0,1.8),arrowprops={"arrowstyle": "->"})
    plt.text(4.5,-0.3,r'$x$',color="blue",fontsize=25,ha="center")
    plt.text(0.2,1.6,r'$y$',color="blue",fontsize=25,ha="center")
    plt.text(-0.3,1.2,r'$S_r^h$',color="blue",fontsize=25,ha="center")
    plt.text(-0.3,0.6,r'$\frac{1}{2}S_r^h$',color="blue",fontsize=25,ha="center")
    plt.text(3.14,-0.35,r'$\theta_m$',color="blue",fontsize=25,ha="center")
    plt.text(0.5*3.14,-0.35,r'$\frac{1}{2}\theta_m$',color="blue",fontsize=25,ha="center")

    Directoryname = ""
    datafile = "rhotheta"

    x = np.linspace(0,0.5*np.pi,100)
    y = np.cos(x)
    plt.plot(2*x,1.2*y)

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
