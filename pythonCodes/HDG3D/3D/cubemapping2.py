#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 20:19
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : cubemapping2.py
# @version : Python 2.7.6
#---------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#---------------------------------------------------

def plotcube(edgelen, vector,center=[0,0]):
    tx = 1
    ty = 0.4
    tz = 1
    p = 0.5*edgelen
    rate = 1.5
    xlim = np.array([-1*rate*p, rate*p+vector[0]])+center[0]
    ylim = np.array([-1*rate*p, rate*p+vector[1]])+center[1]
    plt.xlim(xlim)
    plt.ylim(ylim)
    x = np.array([-1*p,p,p,-1*p,-1*p])+center[0]
    y = np.array([-1*p,-1*p,p,p,-1*p])+center[1]
    p1 = np.array([x[0], y[0]])
    p2 = np.array([x[1], y[1]])
    p6 = np.array([x[2], y[2]])
    p5 = np.array([x[3], y[3]])
    p4 = np.array([x[0]+vector[0], y[0]+vector[1]])
    p3 = np.array([x[1]+vector[0], y[1]+vector[1]])
    p7 = np.array([x[2]+vector[0], y[2]+vector[1]])
    p8 = np.array([x[3]+vector[0], y[3]+vector[1]])

    plt.plot(x, y, color="black")
    plt.plot(x[1:4]+vector[0], y[1:4]+vector[1], color="black")
    plt.plot(x[-2:]+vector[0], y[-2:]+vector[1], "--",color="black")
    plt.plot(x[:2]+vector[0], y[:2]+vector[1], "--",color="black")
    plt.plot([x[0],x[0]+vector[0]], [y[0], y[0]+vector[1]],"--",color="black")
    plt.plot([x[1:4],x[1:4]+vector[0]], [y[1:4], y[1:4]+vector[1]], color="black")

    xz1 = 0.25*(p1+p2+p6+p5)
    xz2 = 0.25*(p4+p3+p7+p8)
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "bo")

    xz1 = 0.25*(p1+p4+p8+p5)
    xz2 = 0.25*(p2+p3+p7+p6)
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "bo")

    xz1 = 0.25*(p1+p2+p3+p4)
    xz2 = 0.25*(p5+p6+p7+p8)
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "bo")
    tt = 0.5*np.array([p1+p4, p2+p3, p6+p7, p5+p8, p1+p4]).T
    plt.fill(tt[0], tt[1], 'red', alpha = 0.3)
    tt = 0.5*np.array([p1+p2, p4+p3, p8+p7, p5+p6, p1+p2]).T
    plt.fill(tt[0], tt[1], 'b', alpha = 0.3)
    tt = 0.5*np.array([p1+p5, p2+p6, p3+p7, p4+p8, p1+p5]).T
    plt.fill(tt[0], tt[1], 'g', alpha = 0.3)
    # plt.fill(x+ty,y+ty,'red', alpha = 0.3)
    # plt.fill(np.array([x[0],x[0]+vector[1],x[3]+vector[1], x[3], x[0]])+tx,
    #          np.array([y[0],y[0]+vector[1],y[3]+vector[1], y[3], x[0]]),   'b', alpha = 0.3)
    #
    # plt.fill(np.array([x[0], x[1], x[1]+vector[0], x[0]+vector[0], x[0]]),
    #          np.array([y[0], y[1], y[1]+vector[1], y[0]+vector[1], x[0]])+tz,   'g', alpha = 0.3)


    h = 0.2
    plt.text(x[0]+0.2*h,y[0]-h,r"$\widehat P_1$",color="black",fontsize=18,ha="center" )
    plt.text(x[1]+0.2*h,y[1]-h,r"$\widehat P_2$",color="black",fontsize=18,ha="center" )

    plt.text(x[2]+0.7*h,y[2]-h,r"$\widehat P_6$",color="black",fontsize=18,ha="center" )
    plt.text(x[3]+0.7*h,y[3]-h,r"$\widehat P_5$",color="black",fontsize=18,ha="center" )

    plt.text(x[0]+0.2*h+vector[0],y[0]-h+vector[1],r"$\widehat P_4$",color="black",fontsize=18,ha="center" )
    plt.text(x[1]+0.2*h+vector[1],y[1]-h+vector[1],r"$\widehat P_3$",color="black",fontsize=18,ha="center" )

    plt.text(x[2]+0.7*h+vector[0],y[2]-h+vector[1],r"$\widehat P_7$",color="black",fontsize=18,ha="center" )
    plt.text(x[3]+0.7*h+vector[0],y[3]-h+vector[1],r"$\widehat P_8$",color="black",fontsize=18,ha="center" )
    plt.savefig("cubemapping2.pdf",dip=120)
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

    p1 = np.array([x[0], y[0]])
    p2 = np.array([x[1], y[1]])
    p6 = np.array([x[2], y[2]])
    p5 = np.array([x[3], y[3]])
    p4 = np.array([x[0]+vector[0], y[0]+vector[1]])
    p3 = np.array([x[1]+vector[0], y[1]+vector[1]])
    p7 = np.array([x[2]+vector[0], y[2]+vector[1]])
    p8 = np.array([x[3]+vector[0], y[3]+vector[1]])
    xz1 = 0.25*(p1+p2+p6+p5)
    xz2 = 0.25*(p4+p3+p7+p8)
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "bo")
    plt.text(xz1[0], xz1[1], "$F_\\eta^-$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "b")
    plt.text(xz2[0], xz2[1], "$F_\\eta^+$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "b")
    xz1 = 0.25*(p1+p4+p8+p5)
    xz2 = 0.25*(p2+p3+p7+p6)
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "bo")
    plt.text(xz1[0], xz1[1], "$F_\\xi^-$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "g")
    plt.text(xz2[0], xz2[1], "$F_\\xi^+$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "g")
    xz1 = 0.25*(p1+p2+p3+p4)
    xz2 = 0.25*(p5+p6+p7+p8)
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
    plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "bo")
    plt.text(xz1[0], xz1[1], "$F_\\zeta^-$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "r")
    plt.text(xz2[0], xz2[1], "$F_\\zeta^+$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "r")
    tt = 0.5*np.array([p1+p4, p2+p3, p6+p7, p5+p8, p1+p4]).T
    plt.fill(tt[0], tt[1], 'red', alpha = 0.3)
    tt = 0.5*np.array([p1+p2, p4+p3, p8+p7, p5+p6, p1+p2]).T
    plt.fill(tt[0], tt[1], 'b', alpha = 0.3)
    tt = 0.5*np.array([p1+p5, p2+p6, p3+p7, p4+p8, p1+p5]).T
    plt.fill(tt[0], tt[1], 'g', alpha = 0.3)

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
    plt.savefig("parallelcubemapping2.pdf",dip=120)
    plt.show()
    return
edgelen = 2
vector = [0.8,0.8]
fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
plotcube(edgelen, vector,center=[0,0])
plotparallelcube(edgelen, vector,center=[0,0])


