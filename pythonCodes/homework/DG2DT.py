#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DG2DT
@time: 2016-04-13 12:29
"""
#三角形与矩形混合DG
import scipy.io as sio
from _1_Intergral_8 import Intergral_2
import numpy as np
from sympy import*
#from enthought.mayavi import mlab
import copy

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
#每个单元有四条边，每条边有唯一一个单元，nodb的第i行元素表示第i个单元的相邻单元编号。
def nodbd(nod):
    ans = copy.deepcopy(nod)
    ansx = copy.deepcopy(nod)
    (m, n) = nod.shape
    #先对每一个单元进行循环
    for h in range(m):               #主（host）单元循环
        for i in range(n):
            k = 0
            for g in range(m):       #客体（gues）匹配单元循环
                if g != h:           #主客单元不能相同
                    for j in range(n):
                        a = (j+1)%n
                        if nod[h][i] == nod[g][a] and nod[h][(i+1)%n] == nod[g][j]:
                            ans[h][i] = g
                            ansx[h][i] = j
                            k = 1
                            break
                if k == 1:
                    break
            if k == 0:
                ans[h][i] = h
                ansx[h][i] = i
    return ans, ansx

#############################step2 插值
#只需给出标准区域上的插值，和坐标变换。
#三角形标准区域上的线性插值比较简单


#求出三角形所张成的平行四边形面积
def tradet(D):
    ans = (D[0][0] - D[-1][0])*(D[1][1] - D[-1][1]) - (D[1][0] - D[-1][0])*(D[0][1] - D[-1][1])
    return abs(ans)

#求出坐标变换
def coordtransfm(D, s, t):
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    return (x, y)

#坐标变换的雅克比矩阵
def pxy_pst(D):
    xps = D[0][0] - D[2][0]
    xpt = D[1][0] - D[2][0]
    yps = D[0][1] - D[2][1]
    ypt = D[1][1] - D[2][1]
    return np.array([xps, yps], [xpt, ypt])

#坐标变换的雅克比矩阵的逆矩阵
def pst_pxy(D):
    spx = D[1][1] - D[2][1]
    tpx = D[2][0] - D[1][0]
    spy = D[2][1] - D[0][1]
    tpy = D[0][0] - D[2][0]
    ans = np.array([[spx, tpx], [spy, tpy]])
    return ans*1.0/tradet(D)

#############################step3 单元刚阵，与单元荷载`
class EleDG2t:
    def __init__(self, f, D, ee, ss):   #xy为每个单元上的节点
        self.f = f
        self.D = D
        self.ss = ss
        self.ee = ee
        #self.J = pst_pxy(D)
        #self.Le1 = ((self.J[0][0] - self.J[1][0])**2 + (self.J[0][1] - self.J[1][1])**2)**0.5
        #self.Le2 = ((self.J[1][0])**2 + (self.J[1][1])**2)**0.5
        #self.Le3 = ((self.J[0][0])**2 + (self.J[0][1]))**0.5
        def ds((a, b), (c, d)):
            return ((a - c)**2 + (b - d)**2)**0.5
        self.L0 = ds(self.D[0], self.D[1])
        self.L1 = ds(self.D[1], self.D[2])
        self.L2 = ds(self.D[2], self.D[0])
        self.LM = max([self.L0, self.L1, self.L2])
        #self.LM = 1.0/(len(nodt))**0.5
        self.a0 = (self.D[0][1] - self.D[1][1])*(self.D[0][1] - self.D[2][1]) + (self.D[0][0] - self.D[1][0])*(self.D[0][0] - self.D[2][0])
        self.a1 = (self.D[1][1] - self.D[0][1])*(self.D[1][1] - self.D[2][1]) + (self.D[1][0] - self.D[0][0])*(self.D[1][0] - self.D[2][0])
        self.a2 = (self.D[2][1] - self.D[0][1])*(self.D[2][1] - self.D[1][1]) + (self.D[2][0] - self.D[0][0])*(self.D[2][0] - self.D[1][0])


    #--------------------------------方程组矩阵的左边项的子矩阵----------------------#
    #------------------中间项------------------#
    def ke(self):
        b = np.array([[self.D[1][1] - self.D[2][1], self.D[2][1] - self.D[0][1], self.D[0][1] - self.D[1][1]]])
        c = np.array([[self.D[2][0] - self.D[1][0], self.D[0][0] - self.D[2][0], self.D[1][0] - self.D[0][0]]])
        return 0.5*(b.T*b + c.T*c)/tradet(self.D)

    #有求导
    def ae(self):
        a0 = self.a0; a1 = self.a1; a2 = self.a2        
        ans = np.array([[a0+a1, a1, a0], [a1, a1+a2, a2], [a0, a2, a2+a0]])
        return ans*0.5

    #无求导
    def be(self):
        L0, L1, L2 = self.L0, self.L1, self.L2
        ans = np.array([[2*(L0 + L2), L0, L2], [L0, 2*(L0 + L1), L1], [L2, L1, 2*(L1 + L2)]])
        return ans*1.0*self.ss/(6*self.LM)

    #------------------交叉项------------------#
    #有求导    
    def Lji(self, hn, gn):
        LL = [self.a0, self.a1, self.a2]
        L = LL[(hn+1)%3]
        ans = np.zeros((3, 3))
        ans[gn][hn] = L
        ans[gn][(hn+1)%3] = L
        ans[(gn+1)%3][hn] = L
        ans[(gn+1)%3][(hn+1)%3] = L
        return ans*0.5
    
    def Lij(self, hn, gn):
        LL = [self.a0, self.a1, self.a2]
        L = LL[(hn+1)%3]
        ans = np.zeros((3, 3))
        ans[gn][hn] = L
        ans[gn][(hn+1)%3] = L
        ans[(gn+1)%3][hn] = L
        ans[(gn+1)%3][(hn+1)%3] = L
        return ans*0

    #无求导
    def Le(self, hn, gn):   #h为主单元，hn为主单元的边界的序号，g为相邻的客单元,gn为客单元边界序号
        LL = [self.L0, self.L1, self.L2]
        L = LL[hn]
        ans = np.zeros((3, 3))
        ans[gn][hn] = -1.0*L*self.ss/(6*self.LM)
        ans[gn][(hn+1)%3] = -1.0*L*self.ss/(3*self.LM)
        ans[(gn+1)%3][hn] = -1.0*L*self.ss/(3*self.LM)
        ans[(gn+1)%3][(hn+1)%3] = -1.0*L*self.ss/(6*self.LM)
        return ans
    #--------------------------------方程组矩阵的右边项的子矩阵----------------------#
    def fe(self):
        ff = np.zeros(3)
        def h0(s, t):
            (x, y) = coordtransfm(self.D, s, t)
            return s*self.f(x, y)
        def h1(s, t):
            (x, y) = coordtransfm(self.D, s, t)
            return t*self.f(x, y)
        def h2(s, t):
            (x, y) = coordtransfm(self.D, s, t)
            return (1 - s - t)*self.f(x, y)
        def B(s):
            return 1 - s
        ff[0] = Intergral_2().guass_leg_2_comp(h0, (0, B), (0, 1))
        ff[1] = Intergral_2().guass_leg_2_comp(h1, (0, B), (0, 1))
        ff[2] = Intergral_2().guass_leg_2_comp(h2, (0, B), (0, 1))
        return ff*tradet(self.D)

#############################step4 组装
def KF(f, nodt, nodp, ee, ss):   #nodt为关联矩阵， nodp为节点坐标
    (nod1, nod2) = nodbd(nodt)
    n = len(nodt)
    N = 3*n
    K = np.zeros((N, N))
    F = np.zeros(N)
    for i in range(n):
        De = [nodp[nodt[i][0]], nodp[nodt[i][1]], nodp[nodt[i][2]]]
        aa = EleDG2t(f, De, ee, ss)
        fe = aa.fe()
        me = aa.ke() - aa.ae()- aa.ae().T*ee + aa.be()
        F[i*3:(i+1)*3] = fe
        K[i*3:(i+1)*3, i*3:(i+1)*3] = me
        for j in range(3):
            if i > nod1[i][j]:
                K[nod1[i][j]*3:(nod1[i][j]+1)*3, i*3:(i+1)*3] = aa.Le(j, nod2[i][j]) +aa.Lji(j, nod2[i][j])*0.5
            if i < nod1[i][j]:
                K[nod1[i][j]*3:(nod1[i][j]+1)*3, i*3:(i+1)*3] = aa.Le(j, nod2[i][j]) -aa.Lji(j, nod2[i][j]).T*ee*0.5
    return np.linalg.solve(K, F)

#############################step6 问题求解

#############################step7 误差与画图
if __name__ == '__main__':
    def f(x, y):
        return 20*y*(1-y) + 20*x*(1-x)
    def u(x, y):
        return 10*x*y*(1-x)*(1-y)
    #D = [[0, 0], [1, 1]]   #矩形区域
    ee, ss = 1, 100
    print "(ee, ss)=", (ee, ss)

    datap = sio.loadmat("p.mat")   #点
    nodp = np.array(datap['p'])
    nodp = nodp.T

    datat = sio.loadmat("t.mat")
    nodt =  datat['t'][0:-1,:]
    nodt = np.array(nodt) - 1
    nodt = nodt.T 
    
    datagk = sio.loadmat("gk.mat")
    nodgk =  datagk['GK']
    #print nodgk

    

    un = KF(f, nodt, nodp, ee, ss)
    print max(un)
    print min(un)
    
    
    
    
    
    
    
