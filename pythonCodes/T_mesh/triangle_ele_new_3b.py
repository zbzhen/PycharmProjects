#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: triangle_ele_new_3b
@time: 2016-05-10 16:04
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


#标准三角形3次插值的三个边上顶点的基函数
def base_3_b():
    def base(s, t):
        b0 = [s*(s-1.0/3)*t, s*(2.0/3-s)*t]
        b1 = [(t-1.0/3)*t*(1-s-t), (2.0/3-t)*t*(1-s-t)]
        b2 = [s*(2.0/3-s-t)*(1-s-t), -s*(1.0/3-s-t)*(1-s-t)]
        b = b0+b1+b2
        ans = np.array(b)*13.5
        return ans*0.2
    return base


#普通三角形2次插值三个边上顶点的基函数
def ptchazhi_nt(D):   #D为三角形区域，n为插值次数
    def chazhi(x, y):
        (s, t) = coordtransfm_v(D, x, y)
        return base_3_b()(s, t)
    def ansf(i):
        def ansff(x, y):
            return chazhi(x, y)[i]
        return ansff
    return [ansf(i)for i in range(6)]

def tplt(f, D, n=4):
    [s, t, triangles] =  tbaseleplot(n)
    s = np.array(s)
    t = np.array(t)
    (x, y) = coordtransfm(D, s, t)
    z = f(x, y)
    #mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=lw)
    mlab.triangular_mesh(x, y, z, triangles, line_width=0.1)
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

    (m, n) = triangles.shape
    (ee, kk) = point
    p0 = triangles[ee][kk/2]           #通过p0, p1这两个顶点就可以找到节点所在的边
    p1 = triangles[ee][(kk/2+1)%3]

    eans = [] #用来储存单元ee上的第p0,p1个节点相邻的单元的编号
    kans = [] #用来储存单元ee上的第p0,p1个节点在相邻客单元对应的线段单元节点号
    #很显然 eans与kans都只有两个元素

    for i in range(m):
        for j in range(n):
            if (triangles[i][j] == p0 and triangles[i][(j+1)%3] == p1) or (triangles[i][j] == p1 and triangles[i][(j+1)%3] == p0):
                eans += [i]
                kans += [j]

    if meth == "DG":
        eans = [ee]
        kans = [kk]
    for k, e in enumerate(eans):
        x0, x1, x2 = triangles[e][0], triangles[e][1], triangles[e][2]
        De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
        if e == ee:  #注意到k只能取0或者1
            tplt(ptchazhi_nt(De)[kk], De, n=nn*md)

        elif len(eans)>1:
            xx = kans[k]*2 + (kk%2+1)%2
            tplt(ptchazhi_nt(De)[xx], De, n=nn*md)

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
    #md为主单元网格相对加密倍数，nn为副单元的网格数，1w为网格粗细

    #DG方案一：边界边节点：
    #point = np.array([1, 2]);xx = 0;meth = 'DG';nn = 7;md=3;lw=0.5
    #point = np.array([1, 1]);xx = 0;meth = 'DG';nn = 7;md=3;lw=0.5
    #DG方案二：内部边节点：
    #point = np.array([25, 5]);xx = 2;meth = 'DG';nn = 4;md=6;lw=0.5
    #point = np.array([25, 6]);xx = 2;meth = 'DG';nn = 4;md=6;lw=0.5

    #CG方案二：内部边节点：
    #point = np.array([25, 5]);xx = 2;meth = 'CG';nn = 4;md=6;lw=0.5
    point = np.array([25, 2]);xx = 2;meth = 'CG';nn = 4;md=6;lw=0.5

    point -= 1
    tfiles = ["DGt4_10.mat","CGt4_12.mat","CCGt4_32.mat"]
    pfiles = ["DGp2_10.mat","CGp2_11.mat","CCGp2_25.mat"]
    tfile = tfiles[xx]
    pfile =pfiles[xx]
    main(tfile, pfile, point, nn)
    s = mlab.gcf(engine=None);s.scene.background = (1.0, 1.0, 1.0)
    mlab.show()
    #s = mlab.gcf(engine=None);s.scene.background = (1.0, 1.0, 1.0)
    #s.scene.background = (1.0, 1.0, 1.0)