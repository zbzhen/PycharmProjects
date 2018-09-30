#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _3_Newton_Homotopy_8.py
@time: 2016-01-28  10:48
"""
from _2_Newton_Method_8 import Froot, F_n
from sympy import*
import numpy as np
var(["x"+str(i) for i in range(5)])

class Homotopy:
    def __init__(self, f, x, y):
        self.f = f       #函数表达式
        self.x = x       #表达式变量
        self.y = y       #初始值
        self.g0 = F_n().f0(self.f, self.x)   #表达式变成函数
        self.g1 = F_n().f1(self.f, self.x)   #French导数变成函数
        self.gy = F_n().f_0(self.g0, self.y)

    #同伦函数：输入F(x)=>输出H(x,t) = F(x) + (t - 1)F(y)，其中t是参数，y是初始值
    def hxt(self, x, t):
        a = np.array(F_n().f_0(self.g0, x))
        b = np.array(self.gy)*(t - 1)
        return a + b

    #简化同伦迭代函数，并设定精度为10，这样避免内循环时太复杂。
    def hom(self, z, t):
        return Froot(self.hxt(self.x, t).tolist(), self.x, z, e=10).ans()

    #通过内循环得到初值近似值，再运用牛顿迭代法，得到结果
    def hom_ans(self, n):              #n为区间等分个数
        a = self.hom(self.y, 1.0/n)
        for i in range(2, n + 1):
            a = self.hom(a, 1.0*i/n)
        return Froot(self.f, self.x, a).ans()


if __name__ == '__main__' :
    f = [x1**2 - x2 + 1, x1 - cos(x2*pi/2)]
    x = [x1, x2]
    y = [1, 0]
    aa = Homotopy(f, x, y)
    print "The nonlinear equations: F(x) =\n", f
    print
    print "The unknown quantity: x =", x
    print
    print "Initial value: x(0) =", y
    print
    print "The answer x* of F(x*) = 0, x* = \n", aa.hom_ans(8)
    print
    print "Testing, F(x*) = \n", F_n().f_0(aa.g0, aa.hom_ans(8))
