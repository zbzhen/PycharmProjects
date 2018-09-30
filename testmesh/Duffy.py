#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: Duffy
@time: 2017-03-13 13:39
"""
#---------------------------------------------------
import copy
import re
import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------------------

def from_meshdat_get_pet(datafile):
    with open(datafile) as f:
        lines = f.readlines()
        npoint, nelement = np.loadtxt(lines[3:4],int)[0:2]
        #nedgepoint, nedge = np.loadtxt(lines[5:6],int)[1:3]
        points = np.loadtxt(lines[7:(7+npoint)],float)
        elements = np.loadtxt(lines[8+npoint:(8+npoint+nelement)],int)-1
        edges = np.loadtxt(lines[9+npoint+nelement:],int)-1
    return points, elements, edges

def plotmesh2d(points, touch, axes, pointsize=1,ftz=20):
    newtouch  = np.hstack((touch, touch[:,0:1]))

    for i in newtouch:
        x,y = points[i,:].T
        axes.plot(x,y, color='black', linestyle='solid', markerfacecolor='black', linewidth=1)

    for n,i in enumerate(points):
        x,y = i[:2]
        axes.plot(x, y, color='red', marker='o',markerfacecolor='red', markersize=pointsize)
        axes.text(x, y, str(n), color='blue', fontsize = ftz, verticalalignment='top', horizontalalignment='left')

    for n,i in enumerate(touch):
        x,y = points[i,:].T
        x,y = (x[0]+x[1]+x[2])*1.0/3.0, (y[0]+y[1]+y[2])*1.0/3.0
        axes.text(x, y, str(n), color='red', fontsize = ftz, verticalalignment='center', horizontalalignment='center')



def plotblank(axes):
    axes.set_xticks([])
    axes.set_yticks([])
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['bottom'].set_color('none')
    axes.spines['left'].set_color('none')
    return

def getNeibEle_index(nod):   #���nod���������ν�ľ���t
    #nod = np.array(nod)
    NeibEle = copy.deepcopy(nod)
    NeibEleEdge = copy.deepcopy(nod)
    (m,n)=nod.shape
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

#每个节点都有相邻的单元，用ppnod记录下来
def fromPointGetNeibMessage(elements, npoint):
    eans = []   #用来储存第anum个节点的相邻的单元的编号
    kans = []   #用来储存第anum个节点在相邻客单元对应的单元节点号
    (m, n) = elements.shape
    for anum in range(npoint):
        aa = []
        bb = []
        for i in range(m):
            for j in range(n):
                if elements[i][j] == anum:
                    aa += [i]
                    bb += [j]
        eans += [aa]
        kans += [bb]
    return eans, kans

def fromPointGetNeibPoints(elements, npoint):
    neibpoints = []
    (m, n) = elements.shape
    for anum in range(npoint):
        aa = []
        for i in range(m):
            for j in range(n):
                if elements[i][j] == anum:
                    aa += [i]
        pp = elements[aa,:].reshape(1,3*len(aa))[0]
        pp = set(pp) - set([anum])
        neibpoints += [list(pp)]
    return neibpoints



def getDuffymesh(elements):
    return



if __name__ == '__main__':
    datafile = "dumbbell_mesh1.dat"
    datafile = "Add_1_mesh8T.dat"
    points, elements, edges = from_meshdat_get_pet(datafile)
    fig = plt.figure(figsize=(14,6), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    plotmesh2d(points, elements, axes, pointsize=4)
    k = 1; h = 0.03
    x,y = points.T
    xmin = min(x); xmax = max(x); ymin = min(y); ymax = max(y)
    axes.set_xlim(k*xmin-h, k*xmax+h)
    axes.set_ylim(k*ymin-h, k*ymax+h)
    plotblank(axes)
    plt.savefig(datafile[:-4]+".pdf",dip=120,bbox_inches='tight')
    plt.show()

    npoint = len(points)
    eans, kans = fromPointGetNeibMessage(elements, npoint)
    neibpoints = fromPointGetNeibPoints(elements, npoint)
    #print neibpoints
