#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DG2DT_1
@time: 2016-05-31 19:58
"""
#矩形一次DG
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

#坐标变换的逆变换
def coordtransfm_v(D, x, y):
    s = (D[1][0] - x)*(D[2][1] - y) - (D[2][0] - x)*(D[1][1] - y)
    t = (D[2][0] - x)*(D[0][1] - y) - (D[0][0] - x)*(D[2][1] - y)
    s *= 1.0/tradet(D)
    t *= 1.0/tradet(D)
    return  s, t


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
    ans = np.array([s, t, 1 - (s + t)])
    return ans

def phi():
    def f0(s):
        return inter_t_1(1-s, s)
    def f1(s):
        return  inter_t_1(0, 1-s)
    def f2(s):
        return inter_t_1(s, 0)
    return f0, f1, f2

def Dphi():
    return


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

        #外法向量,没有单位化
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
    #两个求导
    def DDe(self):
        def f(s, t):
            ans = np.dot(grad_inter_t_1(s, t), self.G)
            ans = np.dot(ans, grad_inter_t_1(s, t).T)
            return ans
        ansx = self.J*Intergral_2().guass_leg_2_comp(f,(0, (lambda s:1-s)), (0, 1))
        return ansx

    #一个求导
    def De(self, j, i):
        nk = [self.nk0, self.nk1, self.nk2]
        def f(s):
            phi_i = np.array([phi()[i](s)])
            ans = np.dot(phi_i.T, np.array([nk[j]]))
            ans = np.dot(ans, self.DD_v)
            ans = np.dot(ans, grad_inter_t_1(s, s).T)
            return ans
        return 0.5*Intergral_2().guass_leg_1(f, (0, 1))

    #无求导
    def NDe(self, j, i):
        L = [self.L0, self.L1, self.L2]
        def f(s):
            phi_j = np.array([phi()[j](s)])
            phi_i = np.array([phi()[i](s)])
            return np.dot(phi_i.T, phi_j)
        return Intergral_2().guass_leg_1(f, (0, 1))#*L[j]
    #--------------------------------右端向量---------------------#
    def Fe(self):
        def ff(s, t):
            (x, y) = coordtransfm(self.D, s, t)
            return self.f(x, y)*inter_t_1(s, t)
        ansx = self.J*Intergral_2().guass_leg_2_comp(ff,(0, (lambda s:1-s)), (0, 1))
        return ansx

def f(x, y):
    return x*y
D = [[0, 0], [3, 1], [1, 3]]
aa = EleDG2t(f, D)
print aa.DD
print aa.DD_v
print aa.NDe(0, 1)
#############################step4 组装
def KF(f, nodt, nodp, ee, ss):   #nodt为关联矩阵， nodp为节点坐标
    (nod1, nod2) = nodbd(nodt)
    n = len(nodt)              #n为单元个数
    N = 3*n
    K = np.zeros((N, N))
    F = np.zeros(N)
    w = N*N
    for i in range(n):
        De = [nodp[nodt[i][0]], nodp[nodt[i][1]], nodp[nodt[i][2]]]
        aa = EleDG2t(f, De)
        fe = aa.Fe()
        NDe = aa.NDe(0, 0) + aa.NDe(1, 1) + aa.NDe(2, 2)
        De = aa.De(0, 0) + aa.De(1, 1) + aa.De(2, 2)
        me = aa.DDe() + NDe*w*ss + De - De.T*ee
        F[i*3:(i+1)*3] = fe
        K[i*3:(i+1)*3, i*3:(i+1)*3] = me
        for j in range(3):
            if nod1[i][j] != i: #内部边的判定
                bb = aa.De(j, nod2[i][j]) - aa.De(nod2[i][j], j).T + aa.NDe(j, nod2[i][j])*w*ss
                K[nod1[i][j]*3:(nod1[i][j]+1)*3, i*3:(i+1)*3] -= np.array(bb) #注意这里的减号
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
    ee, ss = -1, 1
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


    """
    un = KF(f, nodt, nodp, ee, ss)
    print max(un)
    print min(un)
    plotall(nodp.T, nodt, un, nn=2)
    mlab.show()"""
