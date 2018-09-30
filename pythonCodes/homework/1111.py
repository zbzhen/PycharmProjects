#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _5_FEM1_8.py
@time: 2016-01-28  13:05
"""
from _1_Intergral_8 import Intergral_2
import  numpy as np
from sympy import*


def interpxy(xn):

    def nk(k):
        def wk(x):
            ans = 1.0
            for i in range(len(xn)):
                if  i != k:
                    ans *= (x - xn[i])*1.0/(xn[k] - xn[i])
            return ans
        return wk

    def hihj(index, bsx):
        hi = nk(index[0])
        hj = nk(index[1])
        ans = hi(bsx[0])  * hj(bsx[1])
        return ans
    return hihj

phi =  interpxy([-1, 0, 1])
var(["x,y"])

def phi_ij(index):
    def tmp(x,y):
        return phi(index, [x,y])
    return tmp
# print phi([1,0], [x,y])


def ff(index1, index2):
    def tmp(x,y):
        return phi(index1, [x,y])*phi(index2, [x,y])
    return tmp


#这个例子是对两个基函数做内积
inte = Intergral_2()
ans = inte.guass_leg_2_comp(ff([0,0], [1,0]), [-1,1], [-1,1])
print ans

#下面是函数求导
fij =  phi_ij([0,0])
print fij(x,y)


def phi_x(a,b):
    tmp =  diff(fij(x,y), x)
    return tmp.subs({x:a, y:b})

print phi_x(2,1)


def sort1_2(k, degree):
    n = degree+1;
    i = k%n
    j = k/n
    return i,j

fij =  phi_ij([1,1])
print fij(x,y)

print phi(sort1_2(4, 3), (x,y))