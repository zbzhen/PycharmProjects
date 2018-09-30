#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DG2D
@time: 2016-04-03 10:31
"""
#矩形DG
from _1_Intergral_8 import Intergral_2
import  numpy as np
from sympy import*
from enthought.mayavi import mlab

"""
一般性问题
△u(x, y) + f(x, y) = 0  in D(D=[a,b]×[c,d])
u = g(s)                 on L1
pu/pn + A(s)u = h(s)     on L2
做矩形间断有限元

问题中涉及的变量：
函数变量（f(x, y)，D)
边界变量（(g, L1),(A, h, L2)）

本例给出g=0,且没有L2上的边界条件
"""

#############################step1 离散
#规定外法向量方向是自左向右，自下向上
#而曲线的方向是自左向右，自上向下
#每个单元有四条边，每条边有唯一一个单元，nodb的第i行元素表示第i个单元的相邻单元编号。
def nodib(H, L):
    n = H*L
    ans = np.zeros((n, 4))
    for i in range(n):
        ans[i][0] = i - L
        ans[i][1] = i + 1
        ans[i][2] = i + L
        ans[i][3] = i - 1
    for i in range(L):
        ans[i][0] = i
    for i in range(H):
        a = (i+1)*L-1
        ans[a][1] = a
    for i in range(L):
        a = n-1-i
        ans[a][2] = a
    for i in range(H):
        a = i*L
        ans[a][3] = a
    return ans

#############################step2 插值
#只需给出标准区域上的插值，和坐标变换。
def coordtransfm(subD, s, t):
    a = subD[1][0] - subD[0][0]
    b = subD[-1][1] - subD[0][1]
    c = subD[1][0] + subD[0][0]
    d = subD[-1][1] + subD[0][1]
    x = (c + a*s)*0.5
    y = (d + b*t)*0.5
    return [x, y]

def interp2DR(s, t):
    return np.array([(1 - s)*(1 - t), (1 + s)*(1 - t), (1 + s)*(1 + t), (1 - s)*(1 + t)])*0.25

def interp2DR_1(s, t):
    ps = np.array([-(1 - t), (1 - t), (1 + t), -(1 + t)])
    pt = np.array([-(1 - s), -(1 + s), (1 + s), (1 - s)])
    return np.array([ps, pt])*0.25

#############################step3 单元刚阵，与单元荷载
class EleDG2r:
    def __init__(self, f, D, ee, ss):   #xy为每个单元上的节点
        self.f = f
        self.D = D
        self.a = D[1][0] - D[0][0]
        self.b = D[-1][1] - D[0][1]
        self.ss = ss
        self.ee = ee

    def Ae(self):
        p = np.array([[2, -2, -1, 1], [-2, 2, 1, -1], [-1, 1, 2, -2], [1, -1, -2, 2]])
        q = np.array([[2, 1, -1, -2], [1, 2, -2, -1], [-1, -2, 2, 1], [-2, -1, 1, 2]])
        return (p*(1.0*self.b/self.a) + q*(1.0*self.a/self.b))/6

    def BCe(self):
        s, t = self.a, self.b
        ans = np.array([[2*(s+t),s,0,t], [s,2*(s+t),t,0], [0,t,2*(s+t),s], [t,0,s,2*(s+t)]])
        return self.ss*ans*1.0/6

    def Downe(self):
        ans = np.zeros((4,4))
        ans[0][2] = 0.25 - 0.25*self.ee - self.ss*self.a*1.0/6
        ans[0][3] = -0.25 - 0.25*self.ee - self.ss*self.a*1.0/3
        ans[1][2] = 0.25 + 0.25*self.ee - self.ss*self.a*1.0/3
        ans[1][3] = -0.25 + 0.25*self.ee - self.ss*self.a*1.0/6
        return ans

    def Upe(self):
        ans = np.zeros((4,4))
        ans[2][0] = 0.25 - 0.25*self.ee - self.ss*self.a*1.0/6
        ans[2][1] = -0.25 - 0.25*self.ee - self.ss*self.a*1.0/3
        ans[3][0] = 0.25 + 0.25*self.ee - self.ss*self.a*1.0/3
        ans[3][1] = -0.25 + 0.25*self.ee - self.ss*self.a*1.0/6
        return ans

    def Righte(self):
        ans = np.zeros((4,4))
        ans[1][0] = -0.25 - 0.25*self.ee - self.ss*self.b*1.0/3
        ans[1][3] = 0.25 - 0.25*self.ee - self.ss*self.b*1.0/6
        ans[2][0] = -0.25 + 0.25*self.ee - self.ss*self.b*1.0/6
        ans[2][3] = 0.25 + 0.25*self.ee - self.ss*self.b*1.0/3
        return ans

    def Lefte(self):
        ans = np.zeros((4,4))
        ans[0][1] = 0.25 + 0.25*self.ee - self.ss*self.b*1.0/3
        ans[0][2] = -0.25 + 0.25*self.ee - self.ss*self.b*1.0/6
        ans[3][1] = 0.25 - 0.25*self.ee - self.ss*self.b*1.0/6
        ans[3][2] = -0.25 - 0.25*self.ee - self.ss*self.b*1.0/3
        return ans

    def Downbe(self):
        ans = np.zeros((4,4))
        ans[2][2] = (-0.5 + ee*0.5)*self.a/6
        ans[2][3] = (-0.5 + ee*0.5)*self.a/6
        ans[3][2] = (-0.5 + ee*0.5)*self.a/6
        ans[3][3] = (-0.5 + ee*0.5)*self.a/6
        return ans

    def Upbe(self):
        ans = np.zeros((4,4))
        ans[0][0] = (0.5 - ee*0.5)*self.a/6
        ans[0][1] = (0.5 - ee*0.5)*self.a/6
        ans[1][0] = (0.5 - ee*0.5)*self.a/6
        ans[1][1] = (0.5 - ee*0.5)*self.a/6
        return ans

    def Rightbe(self):
        ans = np.zeros((4,4))
        ans[0][0] = (0.5 - ee*0.5)*self.b/6
        ans[0][3] = (0.5 - ee*0.5)*self.b/6
        ans[3][0] = (0.5 - ee*0.5)*self.b/6
        ans[3][3] = (0.5 - ee*0.5)*self.b/6
        return ans

    def Leftbe(self):
        ans = np.zeros((4,4))
        ans[1][1] = (-0.5 + ee*0.5)*self.b/6
        ans[1][2] = (-0.5 + ee*0.5)*self.b/6
        ans[2][1] = (-0.5 + ee*0.5)*self.b/6
        ans[2][2] = (-0.5 + ee*0.5)*self.b/6
        return ans

    def Fe(self):
        ff = np.zeros(4)
        def h(k):
            def g(s, t):
                (x, y) = coordtransfm(self.D, s, t)
                return self.f(x, y)*interp2DR(s, t)[k]
            return g
        for i in range(4):
            ff[i] = 0.25*self.a*self.b*Intergral_2().guass_leg_2_comp(h(i), (-1, 1), (-1, 1))
        return ff


#############################step4 组装
def KF(f, D, (H, L), ee, ss):
    Nodib = nodib(H, L)      #关联矩阵
    h, l = (H + 1), (L + 1)
    N = 4*H*L
    K = np.zeros((N, N))
    F = np.zeros(N)
    xn = np.linspace(D[0][0], D[1][0], l)
    yn = np.linspace(D[0][1], D[-1][1], h)
    aa = EleDG2r(f, D, ee, ss)
    Me = aa.Ae() + aa.BCe()
    print Me
    #先不考虑外部边界，只考虑内部边界
    for i in range(H*L):
        de = [[xn[i%L], yn[i/L]], [xn[i%L+1], yn[i/L+1]]]
        fe = EleDG2r(f, de, ee, ss).Fe()
        F[i*4:(i+1)*4] = fe
        K[i*4:(i+1)*4, i*4:(i+1)*4] = Me
    aaaa = [aa.Upe(), aa.Lefte(), aa.Downe(), aa.Righte()]
    bbbb = [aa.Upbe(), aa.Leftbe(), aa.Downbe(), aa.Rightbe()]
    for k, e in enumerate(Nodib):
        for i in range(4):
            """
            K[e[i]*4:(e[i]+1)*4, k*4:(k+1)*4] += aaaa[i]
            if k == e[i]:
                K[e[i]*4:(e[i]+1)*4, k*4:(k+1)*4] += bbbb[i]
            """
            if k != e[i]:
                K[e[i]*4:(e[i]+1)*4, k*4:(k+1)*4] += aaaa[i]
            #K[e[i]*4:(e[i]+1)*4, k*4:(k+1)*4] += bbbb[i]
    return [K, F]
#############################step5 强加边界条件
def bdynum(H, L):
    a = np.arange(0, 4*L, 4)
    aa = a + 1
    b = np.arange(4*(H-1)*L+2, 4*H*L, 4)
    bb = b + 1
    c = np.arange(4*L-3, 4*H*L, 4*L)
    cc = c + 1
    d = np.arange(0, 4*H*L, 4*L)
    dd = d + 3
    ans = a.tolist() + b.tolist() + c.tolist() + d.tolist() + aa.tolist() + bb.tolist() + cc.tolist() + dd.tolist()
    return list(set(ans))

def bound((K, F), (g, L1)):
    for k, e in enumerate(L1):
        K[e] = 0
        K[e][e] = 1
        F[e] = g[k]
    return np.linalg.solve(np.array(K), np.array(F))

#############################step6 问题求解
def DG2Dsolve(f, D, (g, L1), (H, L), ee, ss):
    (K, F) = KF(f, D, (H, L), ee, ss)   #总刚阵和总荷载
    return bound((K, F), (g, L1))#加边界条件,并解出方程组

#############################step7 误差与画图
#定义单位矩形上的插值函数
def interDG2DR(s, t, u):
    ans = (1 - s)*(1 - t)*u[0] + (1 + s)*(1 - t)*u[1] + (1 + s)*(1 + t)*u[2] + (1 - s)*(1 + t)*u[3]
    return 0.25*ans

if __name__ == '__main__' :
    def f(x, y):
        return 20*y*(1-y) + 20*x*(1-x)
    D = [[0, 0], [1, 1]]   #矩形区域
    ee, ss = 1, 10
    (H, L) = (2, 2)
    L1 = bdynum(H, L)
    g = np.zeros(len(L1))

    un = DG2Dsolve(f, D, (g, L1), (H, L), ee, ss)
    print un
    s, t = np.mgrid[-1:1:21j, -1:1:21j]
    xn = np.linspace(D[0][0], D[1][0], L+1)
    yn = np.linspace(D[0][1], D[-1][1], H+1)
    for i in range(H*L):
        subD = [[xn[i%L], yn[i/L]], [xn[i%L+1], yn[i/L+1]]]
        ue = un[i*4:(i+1)*4]
        (x, y) = coordtransfm(subD, s, t)
        z = interDG2DR(s, t, ue)
        mlab.mesh(x, y, z)
    mlab.show()

