#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _6_FEM2_R_8
@time: 2016-02-23 10:52
"""
#矩形二维有限元，采用了坐标变换。
from _1_Intergral_8 import Intergral_2
import numpy as np
from sympy import*
from enthought.mayavi import mlab
var(["x"+str(i) for i in range(5)])
"""
一般性问题
△u(x, y) + f(x, y) = 0  in D(D=[a,b]×[c,d])
u = g(s)                 on L1
pu/pn + A(s)u = h(s)     on L2
做矩形有限元


问题中涉及的变量：
函数变量（f(x, y)，D)
边界变量（(g, L1),(A, h, L2)）

"""
#########第一步，离散，得到关联矩阵
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
#坐标变换,D为矩形区域,可以为四个顶点，也可以为第一三个顶点
def coordtransfm(D, s, t):
    xc = D[0][0] + D[1][0]
    yc = D[-1][1] + D[0][1]
    a = D[1][0] - D[0][0]
    b=  D[-1][1] - D[0][1]
    x = (xc + a*s)*0.5
    y = (yc + b*t)*0.5
    return (x, y)
"""
D = [[0, 0], [3, 4]]
(s, t) = (1, 1)
print coordtransfm(D, s, t)
"""

#单位矩形元上的插值
def releinterp(s, t):
    L1 = (1 - s)*(1 - t)
    L2 = (1 + s)*(1 - t)
    L3 = (1 + s)*(1 + t)
    L4 = (1 - s)*(1 + t)
    return np.array([L1, L2, L3, L4])*0.25
#print releinterp(x0, x1)

########第三步，单元荷载与单元刚度矩阵
class Ele2r:
    def __init__(self, f, D):   #xy为每个单元上的节点
        self.f = f
        self.D = D
        self.a = D[1][0] - D[0][0]
        self.b = D[-1][1] - D[0][1]

    def ke(self):
        p = np.array([[2, -2, -1, 1], [-2, 2, 1, -1], [-1, 1, 2, -2], [1, -1, -2, 2]])
        q = np.array([[2, 1, -1, -2], [1, 2, -2, -1], [-1, -2, 2, 1], [-2, -1, 1, 2]])
        return (p*(1.0*self.b/self.a) + q*(1.0*self.a/self.b))/6

    def fe(self):
        ff = np.zeros(4)
        def h(k):
            def g(s, t):
                (x, y) = coordtransfm(self.D, s, t)
                return self.f(x, y)*releinterp(s, t)[k]
            return g
        for i in range(4):
            ff[i] = 0.25*self.a*self.b*Intergral_2().guass_leg_2_comp(h(i), (-1, 1), (-1, 1))
        return ff

"""
D = [[0, 0], [0.5, 0.5]]
def f(x, y):
    return 2*y*(1-y) + 2*x*(1-x)
a = Ele2r(f, D)
print a.fe()
"""

#########第四步，集成总刚度矩阵和总荷载
def KF(f, D, (H, L)):       #D可取矩形区域四个点，也可取其第1,3个点。
    Nod = nod(H, L)      #关联矩阵
    h, l = (H + 1), (L + 1)
    N = h*l              #总节点数
    K = np.zeros((N, N))
    F = np.zeros(N)
    xn = np.linspace(D[0][0], D[1][0], l)
    yn = np.linspace(D[0][1], D[-1][1], h)
    de = [[xn[0], yn[0]], [xn[1], yn[1]]]
    ke = Ele2r(f, de).ke()
    for e in Nod:
        kf = Ele2r(f, [[xn[m%l], yn[m/l]] for m in e])
        #[ke, fe] = [kf.ke(), kf.fe()]
        fe = kf.fe()
        for i in range(4):
            F[e[i]] += fe[i]
            for j in range(4):
                K[e[i]][e[j]] += ke[i][j]
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
    return bound((K, F), (g, L1))#加边界条件,并解出方程组

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
        ans = 0
        for i in range(4):
            ans += ue[i]*interp(xe)[i](x, y)
        return ans
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



    (H, L) = (4, 4)          #行列单元分割
    #边界条件
    L1 = bdynum(H, L)
    g = np.zeros(len(L1))

    h, l = (H + 1), (L + 1)
    N = h*l              #总节点数

    un = fem2solve(f, D, (g, L1), (H, L))

    (x, y) = np.mgrid[D[0][0]:D[1][0]:21j, D[0][1]:D[-1][1]:21j]
    z = fem2fuc((x, y), un, (H, L), D)
    #erro = (z - 10*x*y*(x-1)*(y-1))*1000
    pl = mlab.mesh(x, y, z)
    mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    mlab.title(str(H) + "*" + str(L) + " Aliquots of rectangle FEM2D")
    mlab.outline(pl)
    mlab.show()
    """