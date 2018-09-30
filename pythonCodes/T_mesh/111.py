#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 111
@time: 2016-04-29 22:59
"""
from enthought.mayavi.scripts import mayavi2
import scipy.io as sio
import numpy as np
from mayavi import mlab
#画红网格
#在标准三角形上画图，输出相应画图参数
"""
0
1  2
3  4  5
6  7  8  9
10 11 12 13 14

"""
def tbaseleplot(n):
    x = []
    y = []
    h = 1.0/n
    for i in range(n+1):
        x += [j*h for j in range(i+1)]
        aa = 1 - i*h
        for k in range(i+1):
            y += [aa]
    t = [[0,1,2]]
    for i in range(1,n):
        for j in range(i*(i+1)/2, (i+1)*(i+2)/2):
            t += [[j, j+i+1, j+i+2]]
            if j != (i+1)*(i+2)/2 -1:
                t += [[j, j+i+2, j+1]]
    return [x, y, t]

def coordtransfm(D, s, t):
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    return x, y

def tplt(f, D, n=3):
    [s, t, triangles] =  tbaseleplot(n)
    s = np.array(s)
    t = np.array(t)
    (x, y) = coordtransfm(D, s, t)
    lenx = len(x)
    x = x.tolist() + [x[0]]
    y = y.tolist() + [x[0]]
    x = np.array(x)
    y = np.array(y)
    triangles = np.array(triangles)
    triangles = triangles.tolist()
    triangles += [[lenx,lenx,lenx]]
    z = f(x, y)
    c = np.ones_like(x)
    c[-1] = 0
    mlab.triangular_mesh(x, y, z, triangles, scalars=c, representation="wireframe", transparent=True, line_width=1.0)
    #mlab.triangular_mesh(x, y, z, triangles, transparent=True, line_width=0.1)
    return

def f(x, y):
    return 0*x*y

def makechat(tfile, pfile, point, nn):   #point第一指标为单元编号，第二个指标为它在单元上的局部线段编号
    datap = sio.loadmat(pfile)   #节点坐标
    pp = np.array(datap['p'])
    datat = sio.loadmat(tfile)
    tt =  datat['t'][0:-1,:]    #三角形关联矩阵
    tt = np.array(tt) - 1
    triangles = tt.T

    x = pp[0]
    y = pp[1]
    lenx = len(x)
    x = x.tolist() + [x[0]]
    y = y.tolist() + [x[0]]
    x = np.array(x)
    y = np.array(y)
    triangles = triangles.tolist()
    triangles += [[lenx,lenx,lenx]]
    triangles = np.array(triangles)
    z = np.zeros_like(x)
    t = np.ones_like(x)
    t[-1] = 0

    mlab.triangular_mesh(x, y, z, triangles, scalars=t, representation="wireframe", line_width=4.0)

    triangles = tt.T
    def fff(x, y):
        return 0*x*y

    eans = point
    for k, e in enumerate(eans):
        x0, x1, x2 = triangles[e][0], triangles[e][1], triangles[e][2]
        De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
        tplt(f, De, n=nn)

    ##用aa矩阵记录非给定顶点的单元编号
    a = range(len(triangles))
    aa = []
    for i in a:
        k = 0
        for j in eans:
            if i == j:
                k = 1
        if k == 0:
            aa += [i]

    for e in aa:
        x0, x1, x2 = triangles[e][0], triangles[e][1], triangles[e][2]
        De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
        tplt(fff, De, n=nn)

    return

@mayavi2.standalone
def main(tfile, pfile, point, nn=9):
    makechat(tfile, pfile, point, nn)
    return

if __name__ == '__main__':
    point = np.array([]);xx = 0;md = 1;nn = 3

    point -= 1
    tfiles = ["DGt4_10.mat","CGt4_12.mat","CCGt4_32.mat"]
    pfiles = ["DGp2_10.mat","CGp2_11.mat","CCGp2_25.mat"]
    tfile = tfiles[xx]
    pfile =pfiles[xx]
    main(tfile, pfile, point, nn)
    mlab.show()
    #s = mlab.gcf(engine=None);s.scene.background = (1.0, 1.0, 1.0)