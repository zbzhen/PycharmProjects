#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: triangle_ele_new_b
@time: 2016-05-04 13:51
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


#标准三角形2次插值的三个边上顶点的基函数
def base_2_b():
    def base(s, t):
        b0 = s*t*4
        b1 = t*(1 - s - t)*4
        b2 = s*(1 - s - t)*4
        ans = np.array([b0, b1, b2])
        return ans*0.4
    return base


#普通三角形2次插值三个边上顶点的基函数
def ptchazhi_nt(D):   #D为三角形区域，n为插值次数
    def chazhi(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_2_b()(s, t)
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
    mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=0.1)
    #mlab.triangular_mesh(x, y, z, triangles, transparent=True, line_width=0.1)
    return

def makechat(tfile, pfile, point, nn):   #point第一指标为单元编号，第二个指标为它在单元上的局部线段编号
    datap = sio.loadmat(pfile)   #节点坐标
    pp = np.array(datap['p'])
    datat = sio.loadmat(tfile)
    tt =  datat['t'][0:-1,:]    #三角形关联矩阵
    tt = np.array(tt) - 1
    triangles = tt.T

    x = pp[0]
    y = pp[1]
    z = np.zeros_like(x)
    t = z
    mlab.triangular_mesh(x, y, z, triangles, scalars=t, representation="wireframe", line_width=3.0)

    def fff(x, y):
        return 0*x*y

    (m, n) = triangles.shape
    (ee, kk) = point
    p0 = triangles[ee][kk]
    p1 = triangles[ee][(kk+1)%3]

    eans = []
    kans = []
    for i in range(m):
        for j in range(n):
            if (triangles[i][j] == p0 and triangles[i][(j+1)%3] == p1) or (triangles[i][j] == p1 and triangles[i][(j+1)%3] == p0):
                eans += [i]
                kans += [j]
    print eans, kans
    for k, e in enumerate(eans):
        x0, x1, x2 = triangles[e][0], triangles[e][1], triangles[e][2]
        De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
        tplt(ptchazhi_nt(De)[kans[k]], De, n=nn)

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
def main(tfile, pfile, point, nn=9):
    makechat(tfile, pfile, point, nn)
    return
if __name__ == '__main__':
    tfile = "DGt4_10.mat"
    pfile = "DGp2_10.mat"
    point = [9, 0]
    nn = 21
    main(tfile, pfile, point, nn)

    s = mlab.gcf(engine=None)
    s.scene.background = (1.0, 1.0, 1.0)

    mlab.savefig("111111.pdf")
    mlab.show()