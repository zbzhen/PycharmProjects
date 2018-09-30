#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DG1D
@time: 2016-03-26 10:42
"""
from _1_Intergral_8 import Intergral_1
import  numpy as np
from sympy import*
import matplotlib.pyplot as plt


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
#该数值例子的标准单元[-1, 1]上的基函数为1，x, x**2


##########################################step2, 计算刚度矩阵的零件
def ke(ne, ee, ss):
    AN = np.array([[0,0,0], [0,4,0], [0,0,16.0/3]])
    
    BN = np.array(
        [[       ss,        1 - ss,    -2 + ss],
        [ - ee - ss,  -1 + ee + ss,    2 - ee - ss],
        [ 2*ee + ss, 1 - 2*ee - ss,   -2 + 2*ee + ss]])
    
    CN = np.array(
        [[       ss,         ss - 1,    -2 + ss],
        [  ee + ss,    -1 + ee + ss,    -2 + ee + ss],
        [ 2*ee + ss, -1 + 2*ee + ss,    -2 + 2*ee + ss]])
    
    DN = np.array(
        [[      -ss,         ss - 1,    2 - ss],
        [ - ee - ss,    -1 + ee + ss,    2 - ee - ss],
        [ -2*ee - ss, -1 + 2*ee + ss,    2 - 2*ee - ss]])
    
    EN = np.array(
        [[      -ss,        -ss + 1,    2 - ss],
        [  ee + ss,    -1 + ee + ss,    -2 + ee + ss],
        [ -2*ee - ss, 1 - 2*ee - ss,    2 - 2*ee - ss]])
    
    F0 = np.array(
        [[      ss,        2 - ss,    -4 + ss],
        [  -2*ee - ss,  -2 + 2*ee + ss,  4 - 2*ee - ss],
        [ 4*ee + ss,  2 - 4*ee - ss,   -4 + 4*ee + ss]])
    
    FN = np.array(
        [[      ss,        -2 + ss,    -4 + ss],
        [  2*ee + ss,  -2 + 2*ee + ss,  -4 + 2*ee + ss],
        [ 4*ee + ss,  -2 + 4*ee + ss,   -4 + 4*ee + ss]])
    AN = AN*ne
    BN = BN*ne
    CN = CN*ne
    DN = DN*ne
    EN = EN*ne
    F0 = F0*ne
    FN = FN*ne
    
    M  = AN + BN + CN
    M0 = AN + F0 + CN
    MN = AN + FN + BN
    return [M, M0, MN, DN, EN]
##########################################step3, 计算荷载的零件
def b(f, n, ne, ee, ss):
    def gg(i):
        def g(t):
            return f(0.5*t/ne + (n+0.5)/ne)*t**i
        return Intergral_1().guass_leg_1(g, (-1, 1))*0.5/ne
    if n == 0:
        return [gg(0) + ss*ne, gg(1) - ee*2*ne - ss*ne, gg(2) + 4*ee*ne + ss*ne]
    return [gg(0), gg(1), gg(2)]

##########################################step4, 组装总刚阵与总荷载
def KF(f, ne, ee, ss):  #ne为单元个数，从1数起
    gn = 3*ne  #gn为方程未知数个数,从1数起
    K = np.zeros((gn, gn))
    F = np.zeros(gn)
    [M, M0, MN, DN, EN] = ke(ne, ee, ss)
    #组装,采用切片法
    for i in range(ne-1):
        F[i*3:(i+1)*3] =  b(f, i, ne, ee, ss)
        K[i*3:(i+1)*3, i*3:(i+1)*3] = M
        K[(i+1)*3:(i+2)*3, i*3:(i+1)*3] = EN
        K[i*3:(i+1)*3, (i+1)*3:(i+2)*3] = DN
    F[-3:] = b(f, ne, ne, ee, ss)
    K[0:3, 0:3] = M0
    K[-3:, -3:] = MN
    return (K, F)

##########################################step5, 强加边界条件
#这一步前面已经完成
##########################################step6, 问题求解
def DG1Dsolve(f, ne, ee, ss):
    (K, F) = KF(f, ne, ee, ss)
    return np.linalg.solve(np.array(K), np.array(F))


##########################################step7, 画图与误差
#利用每个单元上的基系数构造，逼近函数，(a,b)为单元区间端点，方便画图
def DGfuc(ue, (a, b)):
    c = 0.5*(a + b)
    d = 0.5*(b - a)
    def g(x):
        t = (x - c)/d
        return ue[0] + t*ue[1] + t**2*ue[2]
    return g

#算出每个单元上的L2泛数的平方
def DG1Derro(ue, (a, b), u):
    def erro(x):
        return (DGfuc(ue, (a, b))(x)-u(x))**2
    return Intergral_1().guass_leg_1(erro, (a, b))

#算出总区间的L2范数的平方
def eh(ne, ee, ss):
    h = 1.0/ne
    un = DG1Dsolve(f, ne, ee, ss)
    ans = 0
    for i in range(ne):
        a = DG1Derro(un[3*i:3*(i+1)], (i*h, i*h+h), u)
        ans += a
    return ans

def jie(ne, ee, ss):
    return np.log(eh(ne, ee, ss)/eh(2*ne, ee, ss))/(2*np.log(2))


if __name__ == '__main__' :
    ee = 1
    ss = 1
    ne = 32     #单元个数,从1数起
    
    def f(x):
        return -(4*x**2*(-x + 1) + 6*x - 2)*np.exp(-x**2)        
    def u(x):   #真实函数
        return (1-x)*np.exp(-x**2)
    #print eh(64, ee, ss),2222    
    """
    print "ee = ", ee, " and ss = ", ss
    print 8,"&",eh(128, ee, ss)," & ","*" 
   # print 16,"&",eh(16, ee, ss)," & ",jie(8, ee, ss)
    #print 32,"&",eh(32, ee, ss)," & ",jie(16, ee, ss)       
    #print 64,"&",eh(64, ee, ss)," & ",jie(32, ee, ss) 
    #print 128,"&",eh(128, ee, ss)," & ",jie(64, ee, ss) 
    """
 
    
    un =  DG1Dsolve(f, ne, ee, ss) #系数
    h = 1.0/ne  #每个单元长度

    def xx(n, pn=10):    
        return np.linspace(h*n, h*n + h, pn)
    for i in range(ne):
        plt.plot(xx(i), u(xx(i)))
        #plt.plot(xx(i), u(xx(i)) - DGfuc(un[3*i:3*(i+1)], (xx(i)[0], xx(i)[-1]))(xx(i)), "--",label="Exact")
    #plt.title("erro of 32 elements")

    x = np.linspace(0, 1, 129)
    plt.plot(x, u(x), label="u")
    #plt.title("4 elements")
    plt.legend()
    plt.show()
