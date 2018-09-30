#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: t_mesh_ele
@time: 2016-04-21 20:18
"""
#tplt函数可以实现三角形画图
#输入平面上的三个点和一个二维函数，就可以画出图像！
import numpy as np
from enthought.mayavi import mlab

def tplt(D, f, bh=1, n=9):
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
    mlab.mesh(x, y, z, representation="wireframe",line_width=1.0)
    return

if __name__ == '__main__':
    def f(x, y):
        return 10*x*y*(x-1)*(y-1)
    D1 =[[0, 0], [1, 0], [0, 1]]
    D2 = [[1, 1], [1, 0], [0, 1]]
    for d in [D1, D2]:
        tplt(d, f, n=2)
    mlab.show()