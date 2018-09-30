#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DG2DR
@time: 2016-05-16 09:17
"""
#矩形DG
from _1_Intergral_8 import Intergral_2
import numpy as np
#from enthought.mayavi import mlab
from mayavi import mlab
from sympy import*
var("x, y")
"""
一般性问题
△u(x, y) + f(x, y) = 0  in D(D=[a,b]×[c,d])
u = g(s)                 on L1
pu/pn + A(s)u = h(s)     on L2
做三角形间断有限元

问题中涉及的变量：
函数变量（f(x, y)，D)
边界变量（(g, L1),(A, h, L2)）

本例给出g=0,且没有L2上的边界条件
"""

#############################step1 离散
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

#坐标变换的雅克比矩阵
def pxy_pst(subD):
    a = subD[1][0] - subD[0][0]
    b = subD[-1][1] - subD[0][1]
    c = subD[1][0] + subD[0][0]
    d = subD[-1][1] + subD[0][1]
    xps = 0.5*a
    yps = 0
    xpt = 0
    ypt = 0.5*b
    ans = np.array([[xps, yps], [xpt, ypt]])
    return ans



def interp2DR(s, t):
    return np.array([(1 - s)*(1 - t), (1 + s)*(1 - t), (1 + s)*(1 + t), (1 - s)*(1 + t)])*0.25

def interp2DR_1(s, t):
    ps = np.array([-(1 - t), (1 - t), (1 + t), -(1 + t)])
    pt = np.array([-(1 - s), -(1 + s), (1 + s), (1 - s)])
    return np.array([ps, pt])*0.25

def phi():
    def f0(s):
        return interp2DR(s, -1)
    def f1(s):
        return  interp2DR(1, s)
    def f2(s):
        return interp2DR(s, 1)
    def f3(s):
        return interp2DR(-1, s)
    return f0, f1, f2, f3



#############################step3 单元刚阵，与单元荷载
class EleDG2r:
    def __init__(self, f, D, ee, ss):   #xy为每个单元上的节点
        self.f = f
        self.D = D
        self.a = D[1][0] - D[0][0]
        self.b = D[-1][1] - D[0][1]
        self.ss = ss
        self.ee = ee

        #单元边界的长度
        self.L0 = self.a
        self.L1 = self.b
        self.L2 = self.a
        self.L3 = self.b

        #外法向量
        self.nk0 = [0, -1]
        self.nk1 = [1, 0]
        self.nk2 = [0, 1]
        self.nk3 = [-1, 0]

        #雅克比矩阵
        self.DD = pxy_pst(D)
        #雅克比的逆
        self.DD_v = np.linalg.inv(self.DD)
        #雅克比行列式
        self.J = abs(np.linalg.det(self.DD))
        #过度矩阵
        self.G = np.dot(self.DD_v.T, self.DD_v)

    #----------------------------中间项-------------------------------
    #两个求导
    def Ae(self):
        p = np.array([[2, -2, -1, 1], [-2, 2, 1, -1], [-1, 1, 2, -2], [1, -1, -2, 2]])
        q = np.array([[2, 1, -1, -2], [1, 2, -2, -1], [-1, -2, 2, 1], [-2, -1, 1, 2]])
        return (p*(1.0*self.b/self.a) + q*(1.0*self.a/self.b))/6

    def AAe(self):
        def f(s, t):
            ans = np.dot(interp2DR_1(s, t).T, self.G)
            ans = np.dot(ans, interp2DR_1(s, t))
            return ans
        ansx = self.J*Intergral_2().guass_leg_2_comp(f,(-1, 1), (-1, 1))
        return ansx

    #一个求导
    def BBe(self):
        def f0(s):
            ans = np.array([interp2DR(s, -1)]).T*np.array([self.nk0])
            ans = np.dot(ans, self.DD_v)
            ans = np.dot(ans, interp2DR_1(s, -1))
            return ans*self.L0
        def f1(s):
            ans = np.array([interp2DR(1, s)]).T*np.array([self.nk1])
            ans = np.dot(ans, self.DD_v)
            ans = np.dot(ans, interp2DR_1(1, s))
            return ans*self.L1
        def f2(s):
            ans = np.array([interp2DR(s, 1)]).T*np.array([self.nk2])
            ans = np.dot(ans, self.DD_v)
            ans = np.dot(ans, interp2DR_1(s, 1))
            return ans*self.L2
        def f3(s):
            ans = np.array([interp2DR(-1, s)]).T*np.array([self.nk3])
            ans = np.dot(ans, self.DD_v)
            ans = np.dot(ans, interp2DR_1(-1, s))
            return ans*self.L3
        def f(s):
            return f0(s) + f1(s) + f2(s) + f3(s)
        return 0.5*Intergral_2().guass_leg_1(f, (-1, 1))

    def CCe(self):
        def f0(s):
            ans = np.array([interp2DR(s, -1)]).T*interp2DR(s, -1)
            return ans*self.L0
        def f1(s):
            ans = np.array([interp2DR(1, s)]).T*interp2DR(1, s)
            return ans*self.L1
        def f2(s):
            ans = np.array([interp2DR(s, 1)]).T*interp2DR(s, 1)
            return ans*self.L2
        def f3(s):
            ans = np.array([interp2DR(-1, s)]).T*interp2DR(-1, s)
            return ans*self.L3
        def f(s):
            return f0(s) + f1(s) + f2(s) + f3(s)
        return 0.5*self.ss*Intergral_2().guass_leg_1(f, (-1, 1))


    def BCe(self):
        s, t = self.a, self.b
        ans = np.array([[2*(s+t),s,0,t], [s,2*(s+t),t,0], [0,t,2*(s+t),s], [t,0,s,2*(s+t)]])
        return self.ss*ans*1.0/6

    #-------------------交叉项-------------------------------
    #无求导
    def De(self, i, j):
        L = [self.L0, self.L1, self.L2, self.L3]
        def f(s):
            phi_i = np.array([phi()[i](s)])
            phi_j = np.array([phi()[j](s)])
            return np.dot(phi_j.T, phi_i)
            #return phi_i*phi_j.T #两个向量相乘变成矩阵，谁转置谁为行做贡献
        return 0.5*self.ss*L[i]*Intergral_2().guass_leg_1(f, (-1, 1))

    def Downe(self):
        ans = np.zeros((4,4))
        ans[0][2] = -self.ss*self.a*1.0/6
        ans[0][3] = -self.ss*self.a*1.0/3
        ans[1][2] = -self.ss*self.a*1.0/3
        ans[1][3] = -self.ss*self.a*1.0/6
        return ans

    def Upe(self):
        ans = np.zeros((4,4))
        ans[2][0] = -self.ss*self.a*1.0/6
        ans[2][1] = -self.ss*self.a*1.0/3
        ans[3][0] = -self.ss*self.a*1.0/3
        ans[3][1] = -self.ss*self.a*1.0/6
        return ans

    def Righte(self):
        ans = np.zeros((4,4))
        ans[1][0] = -self.ss*self.b*1.0/3
        ans[1][3] = -self.ss*self.b*1.0/6
        ans[2][0] = -self.ss*self.b*1.0/6
        ans[2][3] = -self.ss*self.b*1.0/3
        return ans

    def Lefte(self):
        ans = np.zeros((4,4))
        ans[0][1] = -self.ss*self.b*1.0/3
        ans[0][2] = -self.ss*self.b*1.0/6
        ans[3][1] = -self.ss*self.b*1.0/6
        ans[3][2] = -self.ss*self.b*1.0/3
        return ans
    #---------------------------------------------------------------#

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

    def FFe(self):
        def h(s, t):
            (x, y) = coordtransfm(self.D, s, t)
            return self.f(x, y)*interp2DR(s, t)
        return self.J*Intergral_2().guass_leg_2_comp(h,(-1, 1), (-1, 1))


#############################step4 组装
def KF(f, D, (H, L), ee, ss):
    Nodib = nodib(H, L)      #关联矩阵
    h, l = (H + 1), (L + 1)
    N = 4*H*L
    K = np.zeros((N, N))
    F = np.zeros(N)
    xn = np.linspace(D[0][0], D[1][0], l)
    yn = np.linspace(D[0][1], D[-1][1], h)
    De = [[xn[0], yn[0]], [xn[1], yn[1]]]
    aa = EleDG2r(f, De, ee, ss)
    w = H*L
    Me = aa.Ae() + aa.BCe()*w + aa.BBe() - aa.BBe()*ee
    aaaa = np.array([aa.Upe(), aa.Lefte(), aa.Downe(), aa.Righte()])*w
    bbbb = np.array([aa.De(0, 2), aa.De(1, 3), aa.De(2, 0), aa.De(3, 1)])*w*(-1)
    #先不考虑外部边界，只考虑内部边界    *4*(H*L)   (H + L)**2  *(H**2 + L**2)
    for i in range(H*L):
        de = [[xn[i%L], yn[i/L]], [xn[i%L+1], yn[i/L+1]]]
        fe = EleDG2r(f, de, ee, ss).Fe()
        F[i*4:(i+1)*4] = fe
        K[i*4:(i+1)*4, i*4:(i+1)*4] = Me
    for k, e in enumerate(Nodib):
        for i in range(4):
            if k != e[i]:
                K[e[i]*4:(e[i]+1)*4, k*4:(k+1)*4] += bbbb[i]
                #K[k*4:(k+1)*4, e[i]*4:(e[i]+1)*4] += aaaa[i]
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
    """
    for k, e in enumerate(L1):
        K[e] = 0
        K[e][e] = 1
        F[e] = g[k]
    """
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


#算出每个单元上的L2泛数平方
def DG2Derro(ue, subD, u):
    J = (subD[1][0] - subD[0][0])*(subD[-1][1] - subD[0][1])*0.25
    def erro(s, t):
        (x, y) = coordtransfm(subD, s, t)
        return (u(x, y) - interDG2DR(s, t, ue))**2
    return  Intergral_2().guass_leg_2_comp(erro, (-1, 1), (-1, 1))*J

#算出总区间的L2范数平方
def eh(H, L):
    L1 = bdynum(H, L)
    g = np.zeros(len(L1))
    un = DG2Dsolve(f, D, (g, L1), (H, L), ee, ss)
    xn = np.linspace(D[0][0], D[1][0], L+1)
    yn = np.linspace(D[0][1], D[-1][1], H+1)
    ans = 0
    for i in range(H*L):
        subD = [[xn[i%L], yn[i/L]], [xn[i%L+1], yn[i/L+1]]]
        ue = un[i*4:(i+1)*4]
        aa = DG2Derro(ue, subD, u)
        ans += aa
    return ans

def jie(H, L):
    return np.log(eh(H, L)/eh(2*H, 2*L))/(2*np.log(2))

if __name__ == '__main__':
    def f(x, y):
        return 20*y*(1-y) + 20*x*(1-x)
    def u(x, y):
        return 10*x*y*(1-x)*(1-y)
    D = [[0, 0], [1, 1]]   #矩形区域
    ee, ss = 1, 3
    print "(ee, ss)=", (ee, ss)

    """
    aa = EleDG2r(f, D, ee, ss)
    #print aa.BBe()
    #print aa.CCe()
    print aa.De(0, 0),100
    print aa.De(0, 2),102
    print aa.De(1, 1),111
    print aa.De(2, 0),120
    print aa.De(1, 3),113
    print aa.Upe(),"up"
    print aa.Downe(),'down'
    print aa.Lefte(),"left"
    print aa.Righte(),"right"
    """


    """
    w = H*L
    print eh(H, L)
    #un = DG2Dsolve(f, D, (g, L1), (H, L), ee, ss)
    #print 4,"&",eh(4, 4)," & ","*"            #4 & 0.000548218429448  &  *
    #print 8,"&",eh(8, 8)," & ",jie(4, 4)      #8 & 3.01283178454e-05  &  2.09277939887
    #print 16,"&",eh(16, 16)," & ",jie(8, 8)   #16 & 1.47844608587e-06  &  2.17448329303
    #print jie(16, 16)                         #2.23366572451
    #print jie(32, 32)
    """



    (H, L) = (4, 4)
    L1 = bdynum(H, L)
    g = np.zeros(len(L1))
    print "(H, L)=",(H, L)
    #(K, F) = KF(f, D, (H, L), ee, ss)
    #un = np.linalg.solve(np.array(K), np.array(F))
    un = DG2Dsolve(f, D, (g, L1), (H, L), ee, ss)
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


