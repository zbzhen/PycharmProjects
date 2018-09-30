#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _4_Parametric_Differentiation_8.py
@time: 2016-01-28  11:55
"""
from _2_Newton_Method_8 import Froot, F_n
from sympy import*
import numpy as np
var(["x"+str(i) for i in range(5)])


class Nhpd:
    #定义一个能求微分方程数值解的函数
    #中间的计算过程见P280(6.14)李庆杨《数值计算原理》
    def dif(self, F, x, y0, n=8):
        a = n*F_n().f_1(F_n().f1(F, x), y0)
        b = -1.0*np.array(F_n().f_0(F_n().f0(F, x), y0))
        y1 = np.linalg.solve(a, b)
        y1 += np.array(y0)
        y1_5 = y1 + 0.5*(y1 - y0)
        c = n*F_n().f_1(F_n().f1(F, x), y1_5)
        y2 = np.linalg.solve(c, b)
        y2 += np.array(y1)
        def f(z0, z1):
            z1_5 = z1 + 0.5*(z1 - z0)
            d = n*F_n().f_1(F_n().f1(F, x), z1_5)
            z2 = np.linalg.solve(d, b)
            z2 += np.array(z1)
            return (z1, z2)
        for i in range(n - 1):
            (y0, y1) = f(y0, y1)
        return y1

    #循环终点求积牛顿法最后一步，思路见P281李庆杨《数值计算原理》
    def root_1(self, F, x, y0, n=9):
        y1 = self.dif(F, x, y0, n)
        y2 = Froot(F, x, y0).fuc_newton()(y1).tolist()
        y3 = Froot(F, x, y0).fuc_newton()(y2).tolist()
        if np.max(np.abs(np.array(y3) - np.array(y2))) < \
                np.max(np.abs(np.array(y2) - np.array(y1))):
            return Froot(F, x, y3).ans()
        print u"跳进自我循环"
        return self.root_1(F, x, y1, n)



if __name__ == '__main__' :
    f = [x1**2 - x2 + 1, x1 - cos(x2*pi/2)]
    x = [x1, x2]
    y = [1, 0]
    a = Nhpd()
    b = a.dif(f, x, y)
    print b,u"参数微分法迭代8次的结果和书本上p280的答案（0.0955，0.9784）相同"
    print
    print "The nonlinear equations: F(x) =\n", f
    print
    print "The unknown quantity: x =", x
    print
    print "Initial value: x(0) =", y
    print
    print "The answer x* of F(x*) = 0, x* = \n", a.root_1(f, x, y)
    print
    print "Testing, F(x*) = \n", F_n().f_0(F_n().f0(f, x) , a.root_1(f, x, y))


