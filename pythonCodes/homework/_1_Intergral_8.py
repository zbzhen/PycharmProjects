#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _1_Intergral_8.py
@time: 2016-01-27  11:07
"""
import numpy as np
from sympy import*
var("x,y")

#A standard  code to get the gauss points and the weights
def guasspw(n):
    u = [i/np.sqrt((2*i)**2 -1) for i in range(1, n+1)]
    [bp, vc] = np.linalg.eig(np.diag(u, 1) + np.diag(u, -1))
    bp = np.sort(bp)          #bp the integration points
    wf = 2*vc[0]**2
    wf[n - n/2:] = wf[n/2::-1]  #The weight
    return [bp, wf]

class Intergral_1:
    #一维高斯勒让德求积公式
    def guass_leg_1(self, f, (a, b), n=6):  #n为勒让德多项式阶数
        def g(t):   #积分替换
            return f(0.5*(b+a) + 0.5*(b-a)*t)*0.5*(b-a)
        ans = 0.0
        for i in range(n+1):
            ans += guasspw(n)[1][i]*g(guasspw(n)[0][i])
        return ans

    #一维复化高斯勒让德求积公式
    def guass_leg_1_comp(self, f, (a, b), m=5, n=6):  #m为复化等分区间个数
        ans = 0.0
        t = np.linspace(a, b, m+1)
        for i in range(m):
            ans += self.guass_leg_1(f,(t[i],t[i+1]), n)
        return ans


class Intergral_2(Intergral_1):
    #定义一个积分函数,F(y) = f(x, y)对x（即f的第一个变量）在区间[A(y), B(y)]上的积分。
    def fuc_integrate(self, f, (A, B), m=1, n=6):
        def F(y):
            def g(x):
                return f(x, y)

            if isinstance(A, (int, float)):
                def a(x):
                    return 0*x + A
            else:
                a = A
            if isinstance(B, (int, float)):
                def b(x):
                    return 0*x + B
            else:
                b = B
            return Intergral_1.guass_leg_1_comp(self, g, (a(y), b(y)), m, n)
        return F

    #二维复化高斯勒让德求积公式
    def guass_leg_2_comp(self, f, (a, b), (c, d), mx=1, my=1, n=6):
        def g(y):
            return self.fuc_integrate(f, (a, b), mx, n)(y)
        return Intergral_1.guass_leg_1_comp(self, g, (c, d), my, n)



if __name__ == '__main__' :
    def g(x, y):
        return sin(x*y)
    def A(x):
        return x
    def B(x):
        return 2*x

    b = Intergral_2()
    print "Integral fuction of sin(xy) integral on [y,2y]:"
    print b.fuc_integrate(g, (A, B), n=2)(y)
    print "The value of sin(xy) integral on [y,2y]*[0,1]:"
    print b.guass_leg_2_comp(g, (A, B), (0, 1))
    """
    def f(x):
        return 4/(1+x**2)
    for i in range(2, 20):
        print b.guass_leg_1_comp(f, (0, 1),m=1,n=i),i
    """