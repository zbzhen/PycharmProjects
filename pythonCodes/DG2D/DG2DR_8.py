#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DG2DR_8
@time: 2016-06-01 19:33
"""
#矩形DG简化版
from _1_Intergral_8 import Intergral_2
import numpy as np
from mayavi import mlab
from enthought.mayavi.scripts import mayavi2
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
#每个单元有四条边，每条边恰能确定两个单元，nodb的第i行元素表示第i个单元的所有边的相邻单元编号。
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

#注意这里的Dphi和公式中的刚好隔了一个转置
def Dphi():
    def f0(s):
        return interp2DR_1(s, -1)
    def f1(s):
        return  interp2DR_1(1, s)
    def f2(s):
        return interp2DR_1(s, 1)
    def f3(s):
        return interp2DR_1(-1, s)
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
        self.L = [self.a, self.b, self.a, self.b]
        #单位外法向量
        self.nk = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        #雅克比矩阵
        self.DD = pxy_pst(D)
        #雅克比的逆
        self.DD_v = np.linalg.inv(self.DD)
        #雅克比行列式
        self.J = abs(np.linalg.det(self.DD))
        #过度矩阵
        self.G = np.dot(self.DD_v.T, self.DD_v)

    #----------------------------左边矩阵项-------------------------------
    #两个求导
    def DDe(self):
        def f(s, t):
            ans = np.dot(interp2DR_1(s, t).T, self.G)
            ans = np.dot(ans, interp2DR_1(s, t))
            return ans
        ansx = self.J*Intergral_2().guass_leg_2_comp(f,(-1, 1), (-1, 1))
        return ansx

    #无求导
    def NDe(self, j, i): #第一个变量j为主单元的边序号，i为邻单元边序号
        def f(s):
            phi_j = np.array([phi()[j](s)])
            phi_i = np.array([phi()[i](s)])
            return np.dot(phi_i.T, phi_j)
        return 0.5*self.ss*self.L[j]*Intergral_2().guass_leg_1(f, (-1, 1))
        #这个0.5是因为边界积分（-1,1）所产生

    #一个求导
    def De(self, j, i): #第一个变量j为主单元的边序号
        def f(s):
            Dphi_j = Dphi()[j](s)
            phi_i = np.array([phi()[i](s)])
            ans = np.dot(phi_i.T, np.array([self.nk[j]]))
            ans = np.dot(ans, self.DD_v)
            ans = np.dot(ans, Dphi_j)
            return ans
        return 0.25*Intergral_2().guass_leg_1(f, (-1, 1))*self.L[j]
        #这个0.25=0.5*0.5，一个0.5是边界积分（-1,1）所产生，另一个是公式中本来就有

    #------------------------右端向量项----------------------------------#
    def Fe(self):
        def h(s, t):
            (x, y) = coordtransfm(self.D, s, t)
            return self.f(x, y)*interp2DR(s, t)
        return self.J*Intergral_2().guass_leg_2_comp(h,(-1, 1), (-1, 1))


#############################step4 组装
def KF(f, D, (H, L), ee, ss):
    nod1 = nodib(H, L)      #关联矩阵
    nod2 = [2, 3, 0, 1]
    h, l = (H + 1), (L + 1)
    N = 4*H*L
    K = np.zeros((N, N))
    F = np.zeros(N)
    xn = np.linspace(D[0][0], D[1][0], l)
    yn = np.linspace(D[0][1], D[-1][1], h)
    De = [[xn[0], yn[0]], [xn[1], yn[1]]]
    aa = EleDG2r(f, De, ee, ss)
    w = N*N
    NDe = aa.NDe(0,0)+aa.NDe(1,1)+aa.NDe(2,2)+aa.NDe(3,3)
    De = aa.De(0,0)+aa.De(1,1)+aa.De(2,2)+aa.De(3,3)
    Me = aa.DDe() + NDe*w + De - De.T*ee
    #组装中间项与右端项
    for i in range(H*L):
        de = [[xn[i%L], yn[i/L]], [xn[i%L+1], yn[i/L+1]]]
        fe = EleDG2r(f, de, ee, ss).Fe()
        F[i*4:(i+1)*4] = fe
        K[i*4:(i+1)*4, i*4:(i+1)*4] = Me
        for j in range(4):
            if nod1[i][j] != i:  #内部边的判定
                bb = aa.De(j, nod2[j]) - aa.De(nod2[j], j).T + aa.NDe(j, nod2[j])*w*ss
                K[nod1[i][j]*4:(nod1[i][j]+1)*4, i*4:(i+1)*4] -= np.array(bb)  #注意这里的减号
    return [K, F]

#############################step6 问题求解
def DG2Dsolve(f, D, (H, L), ee, ss):
    (K, F) = KF(f, D, (H, L), ee, ss)   #总刚阵和总荷载
    return np.linalg.solve(np.array(K), np.array(F))

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
    un = DG2Dsolve(f, D, (H, L), ee, ss)
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
    ee, ss = 1, 1
    print "(ee, ss)=", (ee, ss)
    (H, L) = (32, 32)


    #print 4,"&",eh(4, 4)**0.5," & ","*"
    #print 8,"&",eh(8, 8)**0.5," & "#,jie(4, 4)
    #print 16,"&",eh(16, 16)**0.5," & "#,jie(8, 8)
    #print eh(32, 32)**0.5
    #print eh(64, 64)**0.5
    #@mayavi2.standalone
    def main():
        un = DG2Dsolve(f, D, (H, L), ee, ss)
        s, t = np.mgrid[-1:1:21j, -1:1:21j]
        xn = np.linspace(D[0][0], D[1][0], L+1)
        yn = np.linspace(D[0][1], D[-1][1], H+1)
        for i in range(H*L):
            subD = [[xn[i%L], yn[i/L]], [xn[i%L+1], yn[i/L+1]]]
            ue = un[i*4:(i+1)*4]
            (x, y) = coordtransfm(subD, s, t)
            z = interDG2DR(s, t, ue)
            mlab.mesh(x, y, z)
        #mlab.savefig("uh.pdf")
        #x,y=np.mgrid[0:1:21j, 0:1:21j]
        #mlab.mesh(x, y, u(x,y))
        s = mlab.gcf(engine=None);s.scene.background = (1.0, 1.0, 1.0)
        mlab.savefig("ui.pdf")
        mlab.show()
        return
    main()
    #
