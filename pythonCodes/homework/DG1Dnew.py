#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DG1Dnew
@time: 2016-03-26 17:15
"""
from _1_Intergral_8 import Intergral_1
import  numpy as np
from sympy import*
import matplotlib.pyplot as plt
import re

var(["x"+str(i) for i in range(5)])
#一维间断有限元简单实例
#----------------------------------------------------
"""
对于问题
- u" = f(x), x in [0,1]，   u(0)=1 and u(1)=0.
f(x) = (4*x**2*(-x + 1) + 6*x - 2)*np.exp(-x**2)
真实解为
u(x) = (1-x)*e**(-x**2),x in [0,1].

基于DG方法的可选变量
区间个数N
单元维数m,该例子取定为2.
下面三个变量的不同选取对应不同的方法
sgm0, sgm1, epxl

单元的基函数可以自行确定
"""
#----------------------------------------------------
##########################################step1, 插值基函数及其导数的确定
def interp(xn):
    def nk(k):
        def wk(x):
            ans = 1.0
            for i in range(len(xn)):
                if  i != k:
                    ans *= x - xn[i]
            return ans
        def lk(x):
            return wk(x)/wk(xn[k])
        return lk
    return [nk(j) for j in range(len(xn))]

#函数求导
def f_1(f):
    def f1(o):
        g = diff(f(x0), x0)
        g = re.sub(str(x0), "o", str(g))
        return eval(g)
    return f1

#插值函数求导
def interp_1(xn):
    def nk_1(k):
        return f_1(interp(xn)[k])
    return [nk_1(j) for j in range(len(xn))]

##########################################step2, 计算刚度矩阵的零件
def An(xn):
    ne = len(xn) #每个单元的节点个数
    ans = np.zeros((ne, ne))
    def h(s, t):
        def F(x):
            return interp_1(xn)[s](x)*interp_1(xn)[t](x)
        return F
    for i in range(ne):
        for j in range(ne):
            ans[i][j] = Intergral_1().guass_leg_1_comp(h(i, j), (xn[0], xn[-1]))

def Bn(xn):
    ne = len(xn)
    ans = np.zeros((ne, ne))
    for i in range(ne):
        for j in range(ne):
            ans[i][j] = 0.5*interp_1(xn)
    return
