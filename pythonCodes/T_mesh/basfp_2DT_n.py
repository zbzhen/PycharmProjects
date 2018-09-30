#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: basfp_2DT_n
@time: 2016-04-26 16:42
"""
#二维n次三角形插值基函数示意图

from enthought.mayavi.scripts import mayavi2
import numpy as np
from mayavi import mlab
import scipy.io as sio


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
        return [b0, b1, b2]
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

def tplt(f, D, bh=1, n=9):
    x, y = np.mgrid[0:1:n+0j, 0:1:n+0j]
    #这种坐标变换是将等腰直角三角形斜边的中点变成正方形的一个角
    if bh == 1:
        s = x - 0.5*x*y
        t = y - 0.5*x*y
    #这种变换是将正方形的其中两点变换成为同一个点：直角三角形的直角顶点
    else:
        s = x*y
        t = y*(1 - x)
    #下面是建立标准三角形与普通三角形之间的坐标变换
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    z = f(x, y)
    mlab.mesh(x, y, z, representation="wireframe", transparent=True, line_width=1.0)
    return


def makechat(tfile, pfile, degree, point, nn):
    datap = sio.loadmat(pfile)   #点
    pp = np.array(datap['p'])
    datat = sio.loadmat(tfile)
    tt =  datat['t'][0:-1,:]
    tt = np.array(tt) - 1
    triangles = tt.T
    for anum in point:
        eans = []   #用来储存第anum个节点的相邻的单元的编号
        kans = []   #用来储存第anum个节点在相邻客单元对应的单元节点号
        (m, n) = triangles.shape
        for i in range(m):
            for j in range(n):
                if triangles[i][j] == anum:
                    eans += [i]
                    kans += [j]

        for k, e in enumerate(eans):
            x0, x1, x2 = triangles[e][0], triangles[e][1], triangles[e][2]
            De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
            tplt(ptchazhi_nt(De, degree)[kans[k]], De, n=nn)

    x = pp[0]
    y = pp[1]
    z = np.zeros_like(x)
    mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=1.0)
    mlab.show()
    return

#@mayavi2.standalone
def main(tfile, pfile, degree, point, nn=9):
    makechat(tfile, pfile, degree, point, nn)
    return

if __name__ == '__main__':
    tfile = "4_24t.mat"
    pfile = "2_20p.mat"
    degree = 2
    point = [1, 12]
    nn = 5
    main(tfile, pfile, degree, point, nn)
    #s = mlab.gcf(engine=None)
    #s.scene.background = (1.0, 1.0, 1.0)