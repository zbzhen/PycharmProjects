#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: elebase
@time: 2016-06-02 20:37
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
        return ans
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
    mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=0.5)
    # mlab.triangular_mesh(x, y, z, triangles, line_width=0.1)
    return

def tplt1(f, D, n=4):
    [s, t, triangles] =  tbaseleplot(n)
    s = np.array(s)
    t = np.array(t)
    (x, y) = coordtransfm(D, s, t)
    z = f(x, y)
    mlab.triangular_mesh(x, y, z, triangles, transparent=True, line_width=0.5)#, representation="wireframe"
    # mlab.triangular_mesh(x, y, z, triangles, line_width=0.1)
    return


D = [[1,0], [0,1], [0,0]]

x = [1,0,0,1]
y = [0,1,0,0]
z = [0,0,0,0]
triangles = [[0,1,2],[0,1,3]]
t = [1,1,1,0]
#mlab.triangular_mesh(x, y, z, triangles, scalars=t, transparent=True, line_width=0.5)
tplt1(ptchazhi_nt(D, 3)[0], D, n=18)
#mlab.outline()
mlab.show()
