#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: pypde_1
@time: 2016-04-22 19:30
"""


from enthought.mayavi.scripts import mayavi2
from bzmesh import t_mesh
import scipy.io as sio
import numpy as np
from mayavi import mlab
import copy


#求出坐标变换
def coordtransfm(D, s, t):
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    return (x, y)

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
        return (1 - s - t)*(1 - 0.5*s - 0.5*t)
    return [bf0, bf1, bf2]

def exchangef(f, D):
    def ff(s, t):
        (x, y) = coordtransfm(D, s, t)
        return f(x, y)
    return ff



#@mayavi2.standalone
def main():
    datap = sio.loadmat("2_20p.mat")   #点
    pp = np.array(datap['p'])
    #print pp
    datat = sio.loadmat("4_24t.mat")
    tt =  datat['t'][0:-1,:]
    tt = np.array(tt) - 1
    triangles = tt.T

    anum = 17
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
        t_mesh.tpltbasef(exchangef(base_2_()[kans[k]], De), n=17)


    x = pp[0]
    y = pp[1]
    z = np.zeros_like(x)
    z1 = np.zeros_like(x)
    z1[17] = 0.5
    mlab.triangular_mesh(x, y, z, triangles, representation="wireframe",transparent=True,line_width=1.0)
    #mlab.triangular_mesh(x, y, z1, triangles)
    mlab.show()
    return

if __name__ == '__main__':
    main()
