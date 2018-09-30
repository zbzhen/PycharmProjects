#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: triangle_all.py
@time: 2016-05-02 09:39
"""
#先在标准三角形上画函数图
#然后通过坐标变换在普通三角形区域上画图

from enthought.mayavi.scripts import mayavi2
import scipy.io as sio
import numpy as np
from mayavi import mlab
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
            ans = np.array([b0, b1, b2])
        return ans*0.5
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



def tplt(f, D, n=4):
    [s, t, d] =  tbaseleplot(n)
    s = np.array(s)
    t = np.array(t)
    d = np.array(d)
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    z = f(x, y)
    #mlab.triangular_mesh(x, y, z, d, representation="wireframe", transparent=True, line_width=0.1)
    return x, y, z, d

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

        x, y, z, dd = np.array([]), np.array([]), np.array([]), np.array([])
        for k, e in enumerate(eans):
            x0, x1, x2 = triangles[e][0], triangles[e][1], triangles[e][2]
            De = [[pp[0][x0], pp[1][x0]], [pp[0][x1], pp[1][x1]], [pp[0][x2], pp[1][x2]]]
            a, b, c, d = tplt(ptchazhi_nt(De, degree)[kans[k]], De, n=nn)
            dd = np.append(dd, d + len(x))
            x = np.append(x, a)
            y = np.append(y, b)
            z = np.append(z, c)

    #这一步是补充区域平面
    t = z
    dd = np.append(dd, triangles + len(x))
    dd = dd.reshape((len(dd)/3, 3))
    x = np.append(x, pp[0])
    y = np.append(y, pp[1])
    z = np.append(z, np.zeros_like(pp[0]))
    t = np.append(t, pp[0])
    fig_myv = mlab.figure(size=(500,500), bgcolor=(1,1,1), fgcolor=(0.5, 0.5, 0.5))
    mlab.triangular_mesh(x, y, z, dd, transparent=True, line_width=1.0, figure=fig_myv)
    #mlab.triangular_mesh(x, y, z, dd, scalars=t, transparent=True, line_width=1.0, color=(0,0,0))
    mlab.colorbar(title='ID', orientation='vertical', nb_labels=3)
    return

#@mayavi2.standalone
def main(tfile, pfile, degree, point, nn=9):
    makechat(tfile, pfile, degree, point, nn)
    return
if __name__ == '__main__':
    tfile = "4_10t.mat"
    pfile = "2_10p.mat"
    degree = 2
    point = [1, 10]
    nn = 21
    main(tfile, pfile, degree, point, nn)
    mlab.show()

