#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: 2dja
@time: 2018/6/29  11:13
"""
from sympy import*
import numpy as np
xhat, yhat, zhat = var("xhat,yhat,zhat")
x, y, z = var("x,y,z")
a,b,c = var("a,b,c")
var(["a_"+str(i) for i in range(5)])
var(["b_"+str(i) for i in range(5)])
var(["c_"+str(i) for i in range(5)])

m1 = a_0*x*y + a_1*x + a_2*y + a_3
m2 = b_0*x*y + b_1*x + b_2*y + b_3
ans = solve([m1,m2,a_0*b_1-b_0*a_1],[x,y])
print ans
# print len(ans)
# t = ans[0][0]
# print diff(t*(a_0*b_1-b_0*a_1),a_0,b_0).subs({a_0:0, b_0:0})
# # print diff(t,b_0).subs({b_0:0})
# print ans[0][1]
# print "---------"
# print ans[1][0]
# print ans[1][1]