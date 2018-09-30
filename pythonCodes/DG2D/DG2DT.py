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
from enthought.mayavi import mlab
import copy
var("x,y")
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
#每个单元有四条边，每条边恰有两个相邻单元，ans的第i行元素表示第i个单元的边的相邻单元编号，ansx记录边在相邻单元的序号。
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
    ans = np.array([[xps, yps], [xpt, ypt]])
    return ans

#坐标变换的雅克比矩阵的逆矩阵
def pst_pxy(D):
    spx = D[1][1] - D[2][1]
    tpx = D[2][0] - D[1][0]
    spy = D[2][1] - D[0][1]
    tpy = D[0][0] - D[2][0]
    ans = np.array([[spx, tpx], [spy, tpy]])
    return ans*1.0/tradet(D)

#标准三角形上的线性插值矩阵
def inter_t_1(s, t):
    ans = np.array([s, t, 1-s-t])
    return ans

def phi():
    def f0(s):
        return inter_t_1(s, 1-s)
    def f1(s):
        return  inter_t_1(0, s)
    def f2(s):
        return inter_t_1(s, 0)
    return f0, f1, f2


#插值矩阵的梯度
def grad_inter_t_1(s, t):
    ans = np.array([[1, 0], [0, 1], [-1, -1]])
    return ans



#############################step3 单元刚阵，与单元荷载`
class EleDG2t:
    def __init__(self, f, D):   #xy为每个单元上的节点
        self.f = f
        self.D = D

        #求三角形每条边长
        def ds((a, b), (c, d)):
            return ((a - c)**2 + (b - d)**2)**0.5
        self.L0 = ds(self.D[0], self.D[1])
        self.L1 = ds(self.D[1], self.D[2])
        self.L2 = ds(self.D[2], self.D[0])
        self.LM = max([self.L0, self.L1, self.L2])

        self.a0 = (self.D[0][1] - self.D[1][1])*(self.D[0][1] - self.D[2][1]) + (self.D[0][0] - self.D[1][0])*(self.D[0][0] - self.D[2][0])
        self.a1 = (self.D[1][1] - self.D[0][1])*(self.D[1][1] - self.D[2][1]) + (self.D[1][0] - self.D[0][0])*(self.D[1][0] - self.D[2][0])
        self.a2 = (self.D[2][1] - self.D[0][1])*(self.D[2][1] - self.D[1][1]) + (self.D[2][0] - self.D[0][0])*(self.D[2][0] - self.D[1][0])

        #外法向量
        self.nk0 = np.array([D[1][1] - D[0][1], D[0][0] - D[1][0]])
        self.nk1 = np.array([D[2][1] - D[1][1], D[1][0] - D[2][0]])
        self.nk2 = np.array([D[0][1] - D[2][1], D[2][0] - D[0][0]])

        #雅克比矩阵
        self.DD = pxy_pst(D)
        #雅克比的逆
        self.DD_v = np.linalg.inv(self.DD)
        #雅克比行列式
        self.J = abs(np.linalg.det(self.DD))
        #过度矩阵
        self.G = np.dot(self.DD_v.T, self.DD_v)

    #--------------------------------方程组矩阵的左边项的子矩阵----------------------#
    #------------------中间项------------------#
    #注意ke与Ae的相同
    def ke(self):
        def f(s, t):
            ans = np.dot(grad_inter_t_1(s, t), self.G)
            ans = np.dot(ans, grad_inter_t_1(s, t).T)
            return ans
        ansx = self.J*Intergral_2().guass_leg_2_comp(f,(0, (lambda s:1-s)), (0, 1))
        return ansx

    def Ae(self):
        b = np.array([[self.D[1][1] - self.D[2][1], self.D[2][1] - self.D[0][1], self.D[0][1] - self.D[1][1]]])
        c = np.array([[self.D[2][0] - self.D[1][0], self.D[0][0] - self.D[2][0], self.D[1][0] - self.D[0][0]]])
        return 0.5*(b.T*b + c.T*c)/tradet(self.D)

    #有求导
    def Be(self):
        def f0(s):
            ans = np.dot(grad_inter_t_1(s, 1-s), (self.DD_v).T)
            ans = np.dot(ans, self.nk0)
            ans = np.array([ans]).T*inter_t_1(s, 1-s)
            return ans
        def f1(s):
            ans = np.dot(grad_inter_t_1(0, s), (self.DD_v).T)
            ans = np.dot(ans, self.nk1)
            ans = np.array([ans]).T*inter_t_1(0, s)
            return ans
        def f2(s):
            ans = np.dot(grad_inter_t_1(s, 0), (self.DD_v).T)
            ans = np.dot(ans, self.nk2)
            ans = np.array([ans]).T*inter_t_1(s, 0)
            return ans
        def f(s):
            return f1(s)+f2(s)+f0(s)
        return Intergral_2().guass_leg_1(f, (0, 1))

    #无求导
    def Ee(self):
        def f0(s):
            ans = np.array([phi()[0](s)])
            return ans*ans.T*self.L0
        def f1(s):
            ans = np.array([phi()[1](s)])
            return ans*ans.T*self.L1
        def f2(s):
            ans = np.array([phi()[2](s)])
            return ans*ans.T*self.L2
        def f(s):
            return f1(s)+f2(s)+f0(s)
        return Intergral_2().guass_leg_1(f, (0, 1))
    #------------------交叉项------------------#
    #无求导
    def Qe(self, i, j):
        def f(s):
            phi_i = np.array([phi()[i](s)])
            phi_j = np.array([phi()[j](1-s)])
            return phi_i*phi_j.T
        return Intergral_2().guass_leg_1(f, (0, 1))
    #--------------------------------方程组矩阵的右边项的子矩阵----------------------#
    def fe(self):
        def ff(s, t):
            (x, y) = coordtransfm(self.D, s, t)
            return self.f(x, y)*inter_t_1(s, t)
        ansx = self.J*Intergral_2().guass_leg_2_comp(ff,(0, (lambda s:1-s)), (0, 1))
        return ansx

"""
def f(x, y):
    return x*y
#D = [[1, 0], [0, 1], [0, 0]]
D = [[0, 0], [2, 1], [1, 2]]
a = EleDG2t(f, D)
#print a.Ae(),"========Ae"
#print a.ke(),"========ke"
print a.Ee(),"========Ee"
print a.Be(),"========Be"
print a.DD,"===========DD"
print a.DD_v,"========DD_v.T"
print a.nk0,'====nk0'
print a.nk1,'====nk1'
print a.nk2,'====nk2'
print a.D,'====D'
print a.fe(),"=======fe"
print a.fee(),"======fee"
#print a.Qe(1, 1),"========ke"
"""

#############################step4 组装
def KF(f, nodt, nodp, ee, ss):   #nodt为关联矩阵， nodp为节点坐标
    (nod1, nod2) = nodbd(nodt)
    n = len(nodt)              #n为单元个数
    N = 3*n
    K = np.zeros((N, N))
    F = np.zeros(N)
    for i in range(n):
        De = [nodp[nodt[i][0]], nodp[nodt[i][1]], nodp[nodt[i][2]]]
        aa = EleDG2t(f, De)
        fe = aa.fe()
        me = aa.Ae() - aa.Be().T- aa.Be()*ee + aa.Ee().T*ss
        F[i*3:(i+1)*3] = fe
        K[i*3:(i+1)*3, i*3:(i+1)*3] = me
        for j in range(3):
            if nod1[i][j] != [i]:
                K[nod1[i][j]*3:(nod1[i][j]+1)*3, i*3:(i+1)*3] = -aa.Qe(j, nod2[i][j]).T*ss
    return np.linalg.solve(K, F)

#############################step6 问题求解
#在标准三角形上画图，输出相应画图参数
"""
0
1  2
3  4  5
6  7  8  9
10 11 12 13 14

"""
def tbaseleplot(n):
    x = []
    y = []
    h = 1.0/n
    for i in range(n+1):
        x += [j*h for j in range(i+1)]
        aa = 1 - i*h
        for k in range(i+1):
            y += [aa]
    t = [[0,1,2]]
    for i in range(1,n):
        for j in range(i*(i+1)/2, (i+1)*(i+2)/2):
            t += [[j, j+i+1, j+i+2]]
            if j != (i+1)*(i+2)/2 -1:
                t += [[j, j+i+2, j+1]]
    return [x, y, t]

def tplt(f, D, n=4):
    [s, t, triangles] =  tbaseleplot(n)
    s = np.array(s)
    t = np.array(t)
    (x, y) = coordtransfm(D, s, t)
    z = f(x, y)
    #mlab.triangular_mesh(x, y, z, triangles, representation="wireframe", transparent=True, line_width=0.1)
    mlab.triangular_mesh(x, y, z, triangles, transparent=True, line_width=0.1)
    return

def coordtransfm_v(D, x, y):
    s = (D[1][0] - x)*(D[2][1] - y) - (D[2][0] - x)*(D[1][1] - y)
    t = (D[2][0] - x)*(D[0][1] - y) - (D[0][0] - x)*(D[2][1] - y)
    s *= 1.0/tradet(D)
    t *= 1.0/tradet(D)
    return  s, t

def plotall(nodp, nodt, un, nn=4): #nn为画图参数，越大表示越精密
    #画出区域网格
    x = nodp[0]
    y = nodp[1]
    z = np.zeros_like(x)
    mlab.triangular_mesh(x, y, z, nodt, representation="wireframe", line_width=3.0)
    def ff(De, ue):
        def gg(x, y):
            (s, t) = coordtransfm_v(De, x, y)
            return s*ue[0] + t*ue[1] +(1-s-t)*ue[2]
        return gg
    #逐个画出网格上的函数
    for e in range(len(nodt)):
        x0, x1, x2 = nodt[e][0], nodt[e][1], nodt[e][2]
        De = [[nodp[0][x0], nodp[1][x0]], [nodp[0][x1], nodp[1][x1]], [nodp[0][x2], nodp[1][x2]]]
        ue = un[e*3:(e+1)*3]
        tplt(ff(De, ue), De, n=nn)
    return

#############################step7 误差与画图

if __name__ == '__main__':
    def f(x, y):
        return 20*y*(1-y) + 20*x*(1-x)
    def u(x, y):
        return 10*x*y*(1-x)*(1-y)
    #D = [[0, 0], [1, 1]]   #矩形区域
    ee, ss = 1, 1
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
    plotall(nodp.T, nodt, un, nn=2)
    mlab.show()
