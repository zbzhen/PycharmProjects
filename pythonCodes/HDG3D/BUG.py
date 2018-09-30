#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: BUG
@time: 2018/6/27  16:07
"""
from sympy import factor,simplify,sqrt
from sympy.abc import x
a = 0.1*0.1*x*x - 1
b = factor(a, deep=True)
print(b)
print factor(x**2 - 0.04)
# a = 0.1*0.1*(x*x - 1)
# b = factor(a)
# print(b)
# a = x*x - 0.01
# b = factor(a)
# print(b)
# Wrong answer 1.0*(0.01*x - 0.1)*(0.01*x + 0.1)

#
# print factor(100*a)
#
# a = y*y*x*x - z*z
# print factor(a)
# print factor(100*a)


