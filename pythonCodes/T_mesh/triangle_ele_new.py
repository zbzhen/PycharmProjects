#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: triangle_ele_new
@time: 2016-05-04 12:14
"""

from enthought.mayavi.scripts import mayavi2
import scipy.io as sio
import numpy as np
from mayavi import mlab

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

#求出三角形面积
def tradet(D):
    ans = (D[0][0] - D[-1][0])*(D[1][1] - D[-1][1]) - (D[1][0] - D[-1][0])*(D[0][1] - D[-1][1])
    return abs(ans)


def coordtransfm_v(D, x, y):
    s = (D[1][0] - x)*(D[2][1] - y) - (D[2][0] - x)*(D[1][1] - y)
    t = (D[2][0] - x)*(D[0][1] - y) - (D[0][0] - x)*(D[2][1] - y)
    s *= 1.0/tradet(D)
    t *= 1.0/tradet(D)
    return  s, t

def coordtransfm(D, s, t):
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    return x, y


#标准三角形n次插值的三个顶点的基函数
def base_n_(n):
    def base(s, t):
        b0 = 1
        b1 = 1
        b2 = 1
        for i in range(n):
            h = 1.0/n
            b0 *= (s - h*i)*1.0/(1 - h*i)
            b1 *= (t - h*i)*1.0/(1 - h*i)
            b2 *= (1 - h*i - s - t)*1.0/(1 - h*i)
            ans = np.array([b0, b1, b2])
        return ans*0.2
    return base


#普通三角形n次插值三个顶点的基函数
def ptchazhi_nt(D, n):   #D为三角形区域，n为插值次数
    def chazhi(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_n_(n)(s, t)
    def ansf(k):
        def ansff(x, y):
            return chazhi(x, y)[k]
        return ansff
    return ansf(0), ansf(1), ansf(2)

def tplt(f, D, n=4):
    [s, t, triangles] =  tbaseleplot(n)
    s = np.array(s)
    t = np.array(t)
    (x, y) = coordtransfm(D, s, t)
    z = f(x, y)
    #mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=0.5)
    mlab.triangular_mesh(x, y, z, triangles, line_width=0.1)
    return

def makechat(tfile, pfile, degree, point, nn):
    datap = sio.loadmat(pfile)   #点
    pp = np.array(datap['p'])
    datat = sio.loadmat(tfile)
    tt =  datat['t'][0:-1,:]
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
    if meth == 'DG':
        eans = [point[0]]
        kans = [point[1]]
        x0, x1, x2 = triangles[point[0]][0], triangles[point[0]][1], triangles[point[0]][2]
        De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
        tplt(ptchazhi_nt(De, degree)[point[1]], De, n=nn*md)
    else:
        for anum in point:
            eans = []   #用来储存第anum个节点的相邻的单元的编号
            kans = []   #用来储存第anum个节点在相邻客单元对应的单元节点号
            aaa = []
            (m, n) = triangles.shape
            for i in range(m):
                for j in range(n):
                    if triangles[i][j] == anum:
                        eans += [i]
                        kans += [j]

            for k, e in enumerate(eans):
                x0, x1, x2 = triangles[e][0], triangles[e][1], triangles[e][2]
                De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
                tplt(ptchazhi_nt(De, degree)[kans[k]], De, n=nn*md)
                #tplt(fff, De, n=nn*md)


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

#@mayavi2.standalone
def main(tfile, pfile, degree, point, nn=9):
    makechat(tfile, pfile, degree, point, nn)
    return
if __name__ == '__main__':
    degree = 2
    #DG方案一：边界顶点：
    #meth = 'DG';point = np.array([1, 2]);xx = 0;md = 3;nn=7

    #DG方案二：内部顶点：
    #point = np.array([25, 1]);xx = 2;meth = 'DG';md = 6;nn=4


    #CG方案一：边界顶点：
    #meth = 'CG';point = np.array([1]);xx = 0;md = 3;nn=7
    #meth = 'CG';point = np.array([1]);xx = 0;md = 2;nn=13
    #CG方案二：内部顶点：
    point = np.array([17]);xx = 2;meth = 'CG';md = 3;nn=7
    #point = np.array([17]);xx = 0;meth = 'CG';md = 1;nn=3




    tfiles = ["DGt4_10.mat","CGt4_12.mat","CCGt4_32.mat"]
    pfiles = ["DGp2_10.mat","CGp2_11.mat","CCGp2_25.mat"]
    tfile = tfiles[xx]
    pfile = pfiles[xx]

    point -= 1
    main(tfile, pfile, degree, point, nn)
    s = mlab.gcf(engine=None);s.scene.background = (1.0, 1.0, 1.0)
    mlab.show()
    #mlab.savefig("qqq.pdf")

    #s = mlab.gcf(engine=None);s.scene.background = (1.0, 1.0, 1.0)
    #s.scene.background = (1.0, 1.0, 1.0)