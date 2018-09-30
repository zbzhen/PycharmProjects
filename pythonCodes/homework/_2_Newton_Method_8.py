#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _2_Newton_Method_8.py
@time: 2016-01-27  17:46
"""
import numpy as np
from sympy import*
import re
var(["x"+str(i) for i in range(5)])

class F_n:
    #Let expression becomes a function and change xi to o[i].
    def f0(self, f, x):
        n = len(x)
        for j in range(n):
            f = re.sub(str(x[j]), [("o[" + str(i) + "]") for i in range(n)][j], str(f))
        return f

    #assigned a value
    def f_0(self, f, o):
        g = eval(str(f))
        for i in range(len(g)):
            g[i] = eval(str(g[i]))
            if not isinstance(g[i], (int, float)):
                g[i] = g[i].evalf(10)
        return g

    #Yield the Jacobian matrix and change xi to o[i].
    def f1(self, f, x):
        m, n = len(f), len(x)
        h = np.reshape(x*m, (m, n))
        for i in range(m):
            for j in range(n):
                h[i][j] = diff(eval(str(f[i])), x[j])
                for k in range(n):
                    h[i][j] = re.sub(str(x[k]), [("o[" + str(t) + "]") for t in range(n)][k], str(h[i][j]))
        return h

    #assigned a value
    def f_1(self, f, o):
        m = len(f)
        n = len(o)
        a = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                a[i][j] = eval(f[i][j])
        return a

#Define a Newton iterated function,
#and carry out the iteration to obtain the desired root
class Froot(F_n):
    def __init__(self, f, x, y, e=0.000001):
        self.g0 = self.f0(f, x)
        self.g1 = self.f1(f, x)
        self.f = f
        self.x = x
        self.y = y
        self.e = e
        self.n = len(self.x)
        self.m = len(self.f)

    def fuc_newton(self):
        def dd(z):
            a = self.f_1(self.g1, z)
            b = -1.0*np.array(self.f_0(self.g0, z))
            c = np.linalg.solve(a, b)
            c += np.array(z)
            return c
        return dd

    def ans(self):
        k = 0
        y1 = self.y
        y2 = self.fuc_newton()(y1).tolist()
        #Using infinite norm
        while np.max(np.abs(np.array(y1) - np.array(y2))) > self.e:
            y1, y2 = y2, self.fuc_newton()(y2).tolist()
            k += 1
            if k == 50:
                print "!!The number of iterations exceeds upper limit!!"
                break
        return y2


if __name__ == '__main__' :
    f = [
            5*x1 + 3 ,
            4*x0*x0 - 2*sin(x1*x2),
            x1*x2 - 1.5
                                  ]

    x = [x0, x1, x2]
    y = [1, 0.1, -1]
    F = Froot(f, x, y)
    print "The nonlinear equations: F(x) =\n", f
    print
    print "The unknown quantity: x =", x
    print
    print "Initial value: x(0) =", y
    print
    print "The answer x* of F(x*) = 0, x* = \n", F.ans()
    print
    print "Testing, F(x*) = \n", F.f_0(F.f0(f, x), F.ans())