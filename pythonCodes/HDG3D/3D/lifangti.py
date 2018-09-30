#!/usr/bin/env python
#-*- coding: utf-8 -*-
#---------------------------------------------------
#演示MatPlotLib中设置坐标轴主刻度标签和次刻度标签.

#对于次刻度显示,如果要使用默认设置只要matplotlib.pyplot.minorticks_on()

#---------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#---------------------------------------------------

def plotcube(edgelen, vector,center=[0,0]):
    p = 0.5*edgelen
    rate = 1.5
    xlim = np.array([-1*rate*p, rate*p+vector[0]])+center[0]
    ylim = np.array([-1*rate*p, rate*p+vector[1]])+center[1]
    plt.xlim(xlim)
    plt.ylim(ylim)
    x = np.array([-1*p,p,p,-1*p,-1*p])+center[0]
    y = np.array([-1*p,-1*p,p,p,-1*p])+center[1]
    plt.plot(x, y, color="black")
    plt.plot(x[1:4]+vector[0], y[1:4]+vector[1], color="black")
    plt.plot(x[-2:]+vector[0], y[-2:]+vector[1], "--",color="black")
    plt.plot(x[:2]+vector[0], y[:2]+vector[1], "--",color="black")
    plt.plot([x[0],x[0]+vector[0]], [y[0], y[0]+vector[1]],"--",color="black")
    plt.plot([x[1:4],x[1:4]+vector[0]], [y[1:4], y[1:4]+vector[1]], color="black")
    h = 0.2
    plt.text(x[0]+0.2*h,y[0]-h,r"$\widehat P_1$",color="black",fontsize=18,ha="center" )
    plt.text(x[1]+0.2*h,y[1]-h,r"$\widehat P_2$",color="black",fontsize=18,ha="center" )

    plt.text(x[2]+0.7*h,y[2]-h,r"$\widehat P_6$",color="black",fontsize=18,ha="center" )
    plt.text(x[3]+0.7*h,y[3]-h,r"$\widehat P_5$",color="black",fontsize=18,ha="center" )

    plt.text(x[0]+0.2*h+vector[0],y[0]-h+vector[1],r"$\widehat P_4$",color="black",fontsize=18,ha="center" )
    plt.text(x[1]+0.2*h+vector[1],y[1]-h+vector[1],r"$\widehat P_3$",color="black",fontsize=18,ha="center" )

    plt.text(x[2]+0.7*h+vector[0],y[2]-h+vector[1],r"$\widehat P_7$",color="black",fontsize=18,ha="center" )
    plt.text(x[3]+0.7*h+vector[0],y[3]-h+vector[1],r"$\widehat P_8$",color="black",fontsize=18,ha="center" )
    plt.savefig("cube.pdf",dip=120)
    plt.show()
    return

def plotparallelcube(edgelen, vector,center=[0,0]):
    p = 0.5*edgelen
    rate = 1.5
    s = 0.2*edgelen
    xlim = np.array([-1*rate*p, rate*p+vector[0]+s])+center[0]
    ylim = np.array([-1*rate*p, rate*p+vector[1]])+center[1]
    plt.xlim(xlim)
    plt.ylim(ylim)

    x = np.array([-1*p,p,p+s,-1*p+s,-1*p])+center[0]
    y = np.array([-1*p,-1*p,p,p,-1*p])+center[1]
    plt.plot(x, y, color="black")
    plt.plot(x[1:4]+vector[0], y[1:4]+vector[1], color="black")
    plt.plot(x[-2:]+vector[0], y[-2:]+vector[1], "--",color="black")
    plt.plot(x[:2]+vector[0], y[:2]+vector[1], "--",color="black")
    plt.plot([x[0],x[0]+vector[0]], [y[0], y[0]+vector[1]],"--",color="black")
    plt.plot([x[1:4],x[1:4]+vector[0]], [y[1:4], y[1:4]+vector[1]], color="black")
    h = 0.2
    plt.text(x[0]+0.2*h,y[0]-h,r"$P_1$",color="black",fontsize=18,ha="center" )
    plt.text(x[1]+0.2*h,y[1]-h,r"$P_2$",color="black",fontsize=18,ha="center" )

    plt.text(x[2]+0.7*h,y[2]-h,r"$P_6$",color="black",fontsize=18,ha="center" )
    plt.text(x[3]+0.7*h,y[3]-h,r"$P_5$",color="black",fontsize=18,ha="center" )

    plt.text(x[0]+0.2*h+vector[0],y[0]-h+vector[1],r"$P_4$",color="black",fontsize=18,ha="center" )
    plt.text(x[1]+0.2*h+vector[1],y[1]-h+vector[1],r"$P_3$",color="black",fontsize=18,ha="center" )

    plt.text(x[2]+0.7*h+vector[0],y[2]-h+vector[1],r"$P_7$",color="black",fontsize=18,ha="center" )
    plt.text(x[3]+0.7*h+vector[0],y[3]-h+vector[1],r"$P_8$",color="black",fontsize=18,ha="center" )
    plt.savefig("parallelcube.pdf",dip=120)
    plt.show()
    return

edgelen = 2
vector = [0.8,0.8]
fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
plotcube(edgelen, vector,center=[0,0])

plotparallelcube(edgelen, vector,center=[0,0])


