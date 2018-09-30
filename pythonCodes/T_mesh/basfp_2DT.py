#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: basfp_2DT.py
@time: 2016-04-23 13:13
"""

#二维一次、二次三角形插值基函数示意图

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

#标准三角形一次基函数
def base_1_():
    def bf0(s, t):
        return s
    def bf1(s, t):
        return t
    def bf2(s, t):
        return 1 - s - t
    return [bf0, bf1, bf2]

#标准三角形二次基函数
def base_2_():
    def bf0(s, t):
        return s*(s - 0.5)*2
    def bf1(s, t):
        return t*(t - 0.5)*2
    def bf2(s, t):
        return (1 - s - t)*(0.5 - s - t)*2
    return [bf0, bf1, bf2]

#一次三角形插值
def ptchazhi_1t(D):
    def chazhi0(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_1_()[0](s, t)*0.2
    def chazhi1(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_1_()[1](s, t)*0.2
    def chazhi2(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_1_()[2](s, t)*0.2
    return chazhi0, chazhi1, chazhi2

#二次三角形插值
def ptchazhi_2t(D):
    def chazhi0(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_2_()[0](s, t)*0.2
    def chazhi1(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_2_()[1](s, t)*0.2
    def chazhi2(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_2_()[2](s, t)*0.2
    return chazhi0, chazhi1, chazhi2

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
    mlab.mesh(x, y, z, transparent=True)
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
            if degree == 1:
                tplt(ptchazhi_1t(De)[kans[k]], De, n=nn)
            elif degree == 2:
                tplt(ptchazhi_2t(De)[kans[k]], De, n=nn)
            else:
                print "degree is the either of 0 or 1"

    x = pp[0]
    y = pp[1]
    z = np.zeros_like(x)
    mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=1.0)
    mlab.show()
    return

#@mayavi2.standalone
def main(tfile, pfile, degree, point, nn=17):
    makechat(tfile, pfile, degree, point, nn)
    return

if __name__ == '__main__':
    tfile = "4_24t.mat"
    pfile = "2_20p.mat"
    degree = 1
    point = [1, 16]
    main(tfile, pfile, degree, point)
    #s = mlab.gcf(engine=None)
    #s.scene.background = (1.0, 1.0, 1.0)