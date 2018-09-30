#!/usr/bin/env python
# encoding: utf-8
import matplotlib.pyplot as plt
from pyGrid2D.Grid2D_2 import Grid2D, plotblank
import numpy as np
import copy
# 分两步走，第一步找到悬点，给出标记,同时把悬点的坐标和位置进行修改

#这个返回的mark向量其实就是索引的重排
def findSingluarPoints(p,t,e):
    mark = range(len(p))
    newp = copy.deepcopy(p)
    for ele in t:
        elepoints = p[ele,:]
        if 2*elepoints[2][0]==elepoints[1][0]+elepoints[3][0] and 2*elepoints[2][1]==elepoints[1][1]+elepoints[3][1]:
            mark[ele[2]] = -1
            if mark[ele[2]] == -1:
                newp[ele[2]] = newp[ele[3]]
                mark[ele[2]] = -2
    tmp1 = -1; tmp2 = -1
    tmp = len(np.where(np.array(mark)<0)[0])
    for i in range(len(p)):
        if mark[i] >= 0:
            tmp1 += 1
            mark[i] = tmp1
        else:
            tmp2 += 1
            mark[i] = tmp2 + (len(p) - tmp)
    return mark, newp


# 第二步，重写构造p，t, e
def restructpte(newp,t,e,mark):
    rp = copy.deepcopy(newp)
    rt = copy.deepcopy(t)
    re = copy.deepcopy(e)
    for i in range(len(rp)):
        rp[mark[i]] = newp[i]
    m,n = np.shape(t)
    for i in range(m):
        for j in range(n):
            rt[i][j] = mark[t[i][j]]
    m,n = np.shape(e)
    for i in range(m):
        for j in range(n):
            re[i][j] = mark[e[i][j]]
    return rp, rt, re



if __name__ == '__main__':
    Directoryname = ""

    datafile = "meshH.dat"
    datafile = "AddDensity_1_meshH.dat"
    outputdatafile = "Duffy"+Directoryname+datafile
    grid = Grid2D()
    grid.from_meshdat_get_pte(Directoryname+datafile)
    p, t, e = grid.points, grid.elements, grid.bounds

    mark, newp = findSingluarPoints(p,t,e)

    rp, rt, re = restructpte(newp,t,e,mark)
    grid.setpte(rp, rt, re)
    grid.outputCppGridDatafile(outputdatafile)

    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    grid.plotmesh2d(axes, pointsize=3, ftz=15,plotpointsnum="y", plotelementsnum="y")
    plotblank(axes)
    plt.savefig(outputdatafile+".pdf",dip=120,bbox_inches='tight')
    plt.show()