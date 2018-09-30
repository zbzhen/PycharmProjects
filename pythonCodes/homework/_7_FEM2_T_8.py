#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _7_FEM2_T_8
@time: 2016-02-05  23:47
"""
#三角形二维有限元

from _1_Intergral_8 import Intergral_2
import numpy as np
from sympy import*
from enthought.mayavi import mlab
#三角形二维有限元
#这个程序的单元分割是将矩形分割成两个三角形
var(["x"+str(i) for i in range(5)])
"""
一般性问题
△u(x, y) + f(x, y) = 0  in D(D=[a,b]×[c,d])
u = g(s)                 on L1
pu/pn + A(s)u = h(s)     on L2
做三角形有限元


问题中涉及的变量：
函数变量（f(x, y)，D)
边界变量（(g, L1),(A, h, L2)）

"""
#########第一步，离散，得到关联矩阵
"""
def nod(H, L):     #将D等分成H*L个矩形元，每个矩形元有两个三角元,H表示横着分割，L表示竖着分割。
    n = H*L        #n为总单元数
    ans = np.zeros((2*n, 3))
    for k in range(2*n):
        i = k/2
        if k%2 == 0:
            ans[k][0] = i/L + i
            ans[k][1] = i/L + i + L + 2
            ans[k][2] = i/L + i + L + 1
        else:
            ans[k][0] = i/L + i
            ans[k][1] = i/L + i + 1
            ans[k][2] = i/L + i + L + 2
    return ans
"""
#虽然是三角形单元，但是因为这个例子的特殊性，为了提高效率，可以使用矩形的关联矩阵
def nod(H, L):     #将D等分成H*L个矩形元，H表示横着分割，L表示竖着分割。
    n = H*L        #n为总单元数
    ans = np.zeros((n, 4))
    for i in range(n):
            ans[i][0] = i/L + i
            ans[i][1] = i/L + i + 1
            ans[i][2] = i/L + i + L + 2
            ans[i][3] = i/L + i + L + 1
    return ans


#########第二步，插值
#求出三角形面积
def tradet(D):
    return (D[0][0] - D[-1][0])*(D[1][1] - D[-1][1]) - (D[1][0] - D[-1][0])*(D[0][1] - D[-1][1])
"""
D = [[0, 0], [1, 1], [4, 5]]
print tradet(D)
"""
#求出坐标变换
def coordtransfm(D, s, t):
    x = (D[0][0] - D[2][0])*s + (D[1][0] - D[2][0])*t + D[2][0]
    y = (D[0][1] - D[2][1])*s + (D[1][1] - D[2][1])*t + D[2][1]
    return (x, y)

########第三步，单元荷载与单元刚度矩阵
class Ele2t:
    def __init__(self, f, D):   #D为每个三角形单元上的节点
        self.f = f
        self.D = D

    def ke(self):
        b = np.array([[self.D[1][1] - self.D[2][1], self.D[2][1] - self.D[0][1], self.D[0][1] - self.D[1][1]]])
        c = np.array([[self.D[2][0] - self.D[1][0], self.D[0][0] - self.D[2][0], self.D[1][0] - self.D[0][0]]])
        return 0.5*(b.T*b + c.T*c)/abs(tradet(self.D))

    def fe(self):
        #a, b, c = self.f(D[0][0]), self.f(D[1][1]), self.f(D[2][2])
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
        return ff*abs(tradet(self.D))


#########第四步，集成总刚度矩阵和总荷载
#为了提高计算效率，这里只是在原矩形元的基础上，将每个矩形分成两个三角形。
def KF(f, D, (H, L)):       #D可取矩形区域四个点，也可取其第1,3个点。
    Nod = nod(H, L)      #关联矩阵
    h, l = (H + 1), (L + 1)
    N = h*l              #总节点数
    K = np.zeros((N, N))
    F = np.zeros(N)
    xn = np.linspace(D[0][0], D[1][0], l)
    yn = np.linspace(D[0][1], D[-1][1], h)
    evenke = Ele2t(f, [[xn[0], yn[0]], [xn[1], yn[1]], [xn[0], yn[1]]]).ke()
    oddke = Ele2t(f, [[xn[0], yn[0]], [xn[1], yn[0]], [xn[1], yn[1]]]).ke()
    for e in Nod:
        re = [[xn[m%l], yn[m/l]] for m in e]
        evenfe = Ele2t(f, (re[0], re[2], re[3])).fe()
        oddfe = Ele2t(f, (re[0], re[1], re[2])).fe()
        for  ni, vi in enumerate([0, 2, 3]):
            F[e[vi]] += evenfe[ni]
            for nj, vj in enumerate([0, 2, 3]):
                K[e[vi]][e[vj]] += evenke[ni][nj]
        for  ni, vi in enumerate([0, 1, 2]):
            F[e[vi]] += oddfe[ni]
            for nj, vj in enumerate([0, 1, 2]):
                K[e[vi]][e[vj]] += oddke[ni][nj]
    return (K, F)

##########第五步，加边界条件，解方程组
def bdynum(H, L):
    N = (H + 1)*(L + 1)
    b01 = range(1, L + 1)
    b12 = range(2*L + 1, N, L + 1)
    b23 = range(N - 2, N - L - 2, -1)
    b30 = range((H-1)*(L + 1), -1, -L-1)
    return b01 + b12 + b23 + b30

def bound((K, F), (g, L1)):
    for k, e in enumerate(L1):
        K[e] = 0
        K[e][e] = 1
        F[e] = g[k]
    return np.linalg.solve(np.array(K), np.array(F))


##########第6步，问题求解
def fem2solve(f, D, (g, L1), (H, L)):
    (K, F) = KF(f, D, (H, L))   #总刚阵和总荷载
    return bound((K, F), (g, L1))#加边界条件,并解出方程

###########第7步，画图，利用线性方程组的解（即插值函数值），得到近似插值函数，然后画图
def interp(xy):
    def nk(k):
        def wk(x, y):
            return (x - xy[(k+2)%4][0])*(y - xy[(k+2)%4][1])
        def lk(x, y):
            return 1.0*wk(x, y)/wk(xy[k][0], xy[k][1])
        return lk
    return  [nk(i) for i in range(4)]

def fem2fuc((x, y), un, (H, L), D):
    Nod = nod(H, L)
    h, l = (H + 1), (L + 1)
    def f((x, y), xe, ue):
        [[a, b], [c, d]] = [xe[0], xe[2]]
        if (y - b)*(c - a) - (x - a)*(d - b) > 0:
            #return ue[0]*(y - d)/(b - d) + ue[2]*(x - a)/(c - a) + ue[3]*((y - b)*(c - a) - (x - a)*(d - b))/((d - b)*(c - a))
            return ((ue[2] - ue[3])*(x - a)*(b - d) + (c - a)*(ue[0]*(y - d) - ue[3]*(y - b)))/((b - d)*(c - a))
        #return ue[0]*(x - c)/(a - c) + ue[1]*((y - b)*(c - a) - (x - a)*(d - b))/((a - c)*(d - b)) + ue[2]*(y - b)/(d - b)
        return ((ue[2] - ue[1])*(y - b)*(a - c) + (d -b)*(ue[0]*(x - c) - ue[1]*(x - a)))/((a - c)*(d - b))
    def fk(k, (x, y)):
        xe = [[xn[m%l], yn[m/l]] for m in Nod[k]]
        ue = [un[j]for j in Nod[k]]
        return f((x, y), xe, ue)
    xn = np.linspace(D[0][0], D[1][0], l)
    yn = np.linspace(D[0][1], D[-1][1], h)
    (m, n) = x.shape
    ans = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            for k, e in enumerate(Nod):
                if xn[e[0]%l] <= x[i][j] <= xn[e[1]%l] and yn[e[0]/l] <= y[i][j] <= yn[e[-1]/l]:
                    ans[i][j] = fk(k, (x[i][j], y[i][j]))
    return ans

def erro(H, L):
    h, l = (H + 1), (L + 1)
    L1 = bdynum(H, L)
    g = np.zeros(len(L1))
    un = fem2solve(f, D, (g, L1), (H, L))

    (x, y) = np.mgrid[D[0][0]:D[1][0]:h+0j, D[0][1]:D[-1][1]:l+0j]
    u = 10*x*y*(x-1)*(y-1)
    uture = u.reshape((1, h*l))

    uerro = np.max(np.abs(np.array(un) - np.array(uture)))
    return uerro

if __name__ == '__main__' :
    def f(x, y):
        return 20*y*(1-y) + 20*x*(1-x)
    D = [[0, 0], [1, 1]]   #矩形区域

    print erro(2, 2)
    print
    print erro(4, 4)
    print
    print erro(8, 8)
    print
    print erro(16, 16)
    print
    print erro(32, 32)
    print
    """
    print np.log(erro(2, 2)/erro(4, 4))/np.log(2)
    print np.log(erro(4, 4)/erro(8, 8))/np.log(2)
    print np.log(erro(8, 8)/erro(16, 16))/np.log(2)
    print np.log(erro(16, 16)/erro(32, 32))/np.log(2)
        """
    """
    (H, L) = (4, 4)          #行列单元分割
    #边界条件
    L1 = bdynum(H, L)
    g = np.zeros(len(L1))
    #D = [[0, 0], [1, 0], [2, 3]]
    #a = Ele2t(f, D)
    #print a.fe(), a.ke()
    un = fem2solve(f, D, (g, L1), (H, L))
    h, l = (H + 1), (L + 1)
    N = h*l              #总节点数
    (x, y) = np.mgrid[D[0][0]:D[1][0]:21j, D[0][1]:D[-1][1]:21j]
    z = fem2fuc((x, y), un, (H, L), D)
    pl = mlab.mesh(x, y, z)
    mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    mlab.title(str(H) + "*" + str(L) + " Aliquots of triangular FEM2D")
    mlab.outline(pl)
    mlab.show()
    """
