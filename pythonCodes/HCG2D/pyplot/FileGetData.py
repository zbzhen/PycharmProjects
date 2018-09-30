#!/usr/bin/env python
# encoding: utf-8

#---------------------------------------------------
import scipy.io as sio
import copy
import re
import os
import shutil
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
#---------------------------------------------------


def getNeibEle_index(nod):   #���nod���������ν�ľ���t
    NeibEle = copy.deepcopy(nod)
    NeibEleEdge = copy.deepcopy(nod)
    (m, n) = nod.shape
    outEdge = []
    #�ȶ�ÿһ����Ԫ����ѭ��
    for h in range(m):               #����host����Ԫѭ��
        for i in range(n):
            k = 0
            for g in range(m):       #���壨gues��ƥ�䵥Ԫѭ��
                if g != h:           #���͵�Ԫ������ͬ
                    for j in range(n):
                        a = (j+1)%n
                        if nod[h][i] == nod[g][a] and nod[h][(i+1)%n] == nod[g][j]:
                            NeibEle[h][i] = g
                            NeibEleEdge[h][i] = j
                            k = 1
                            break
                if k == 1:
                    break
            if k == 0:
                NeibEle[h][i] = h
                NeibEleEdge[h][i] = i
                outEdge += [[h,i]]
    outEdge = np.array(outEdge)
    return NeibEle, NeibEleEdge, outEdge   #outEdge��������߽�ĵ�Ԫ�źͱ߽��

def fromEdgeGetPoint(p,nod, EdgeMessage):
    (m, n) = nod.shape
    EdgeTwoP = []
    for edge in EdgeMessage:
        i,j = edge
        I = nod[i][j]
        J = nod[i][(j+1)%n]
        EdgeTwoP += [[p[I].tolist(), p[J].tolist()]]
    return np.array(EdgeTwoP)

def getNumEdge(NeibEle,NeibEleEdge):
    (m, n) = NeibEle.shape
    NumEdge = copy.deepcopy(NeibEle)
    k = -1
    for h in range(m):
        for i in range(n):
            if NeibEle[h][i] >= h:
                k += 1
                NumEdge[h][i] = k
            else:
                I = NeibEle[h][i]
                J = NeibEleEdge[h][i]
                NumEdge[h][i] = NumEdge[I][J]
    return NumEdge,k+1

def getEdgeMessage(NumEdge, k):
    EdgeMessage1 = [[]]*k
    EdgeMessage2 = [[]]*k
    (m, n) = NumEdge.shape
    for h in range(m):
        for i in range(n):
            I = NumEdge[h][i]
            if len(EdgeMessage1[I]) == 0:
                EdgeMessage1[I] = [h,i]
                EdgeMessage2[I] = [h,i]
            else:
                EdgeMessage2[I] = [h,i]
    return EdgeMessage1, EdgeMessage2


def plotblank(axes):
    axes.set_xticks([])
    axes.set_yticks([])
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['bottom'].set_color('none')
    axes.spines['left'].set_color('none')
    return

def fromuhDatafileGetPointsAndTouch(datafile, n=3):
    with open(datafile) as f:
        lines = f.readlines()
        line2 = lines[n-1]
        N =  re.compile("N=(.*?),").findall(line2,re.I)[0]
        N = int(N)
        E =  re.compile("E=(.*?),").findall(line2,re.I)[0]
        E = int(E)
        points = []; touch = []
        points +=  [np.loadtxt(lines[n:n+N])]
        touch += [np.loadtxt(lines[n+N:n+N+E], int)-1]
        while len(lines) >= (n+N+E+1):
            n += N + E + 1
            line2 = lines[n-1]
            N =  re.compile("N=(.*?),").findall(line2,re.I)[0]
            N = int(N)
            E =  re.compile("E=(.*?),").findall(line2,re.I)[0]
            E = int(E)
            points +=  [np.loadtxt(lines[n:n+N])]
            touch += [np.loadtxt(lines[n+N:n+N+E], int)-1]
    return points, touch





def plotmesh2d(points, touch, axes, pointsize=4, dashedsize=0.1, solidsize=2):
    NeibEle, NeibEleEdge, outEdge = getNeibEle_index(touch)
    outEdgeTwoP = fromEdgeGetPoint(points,touch, outEdge)
    NumEdge, nedge = getNumEdge(NeibEle,NeibEleEdge)
    EdgeMessage1, EdgeMessage2 = getEdgeMessage(NumEdge, nedge)
    meshEdgeTwop = fromEdgeGetPoint(points,touch, EdgeMessage1)
    #print outEdgeTwoP

    #plot outedge
    for i in range(len(outEdgeTwoP)):
        x,y = outEdgeTwoP[i].T[0:2]
        axes.plot(x,y, linewidth=6, color='blue')
        # axes.plot(x,y, linestyle='solid',markerfacecolor='blue', linewidth=6)


    #plot meshedge
    """
    newtouch  = np.hstack((touch, touch[:,0:1]))
    for i in newtouch:
        x,y = points[i,:].T[0:2]
        axes.plot(x,y, color='black', linestyle='dashed', markerfacecolor='black', linewidth=0.3)
    """
    for i in range(nedge):
        x,y = meshEdgeTwop[i].T[0:2]
        # axes.plot(x,y, color='black', linestyle='dashed', markerfacecolor='black', linewidth=dashedsize)
        axes.plot(x,y, color='black', linestyle=':', markerfacecolor='black', linewidth=0.01)

    #plot scatter
    for i in points:
        x,y = i[:2]
        # axes.plot(x, y, color='red', marker='o',markerfacecolor='red', markersize=1.5)
        axes.plot(x, y, color='red', marker='o',markerfacecolor='red', markersize=4)


if __name__ == '__main__':
    datafile = "uhplot.dat"
    datafile = "RRRuh.dat"
    datafile = "meshR8.dat"
    # datafile = "meshnohT8.dat"
    # datafile = "meshhT8.dat"
    pointsx, touchx = fromuhDatafileGetPointsAndTouch(datafile)
    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    xminx = []; xmaxx = []; yminx = []; ymaxx = []
    for i in range(len(pointsx)):
        points, touch = pointsx[i], touchx[i]
        xminx += [points.T[0].min()]
        xmaxx += [points.T[0].max()]
        yminx += [points.T[1].min()]
        ymaxx += [points.T[1].max()]
        plotmesh2d(points, touch, axes, pointsize=8, dashedsize=0.4, solidsize=8)
    plotblank(axes)
    k = 1; h = 0.03
    xmin = min(xminx); xmax = max(xmaxx); ymin = min(yminx); ymax = max(ymaxx)
    axes.set_xlim(k*xmin-h, k*xmax+h)
    axes.set_ylim(k*ymin-h, k*ymax+h)
    plt.savefig(datafile[:-4]+".pdf",dip=120,bbox_inches='tight')
    plt.show()
    #help(plt.savefig)