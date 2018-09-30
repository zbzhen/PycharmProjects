#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _6_FEM2_8.py
@time: 2016-01-31  21:45
"""
from _1_Intergral_8 import Intergral_2
import  numpy as np
from sympy import*
import re
from enthought.mayavi import mlab
#矩形二维有限元(没有采用坐标变换)
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
#第一步，离散，得到关联矩阵
def nod(H, L):     #将D等分成H*L个矩形元，H表示横着分割，L表示竖着分割。
    n = H*L        #n为总单元数
    ans = np.zeros((n, 4))
    for i in range(n):
            ans[i][0] = i/L + i
            ans[i][1] = i/L + i + 1
            ans[i][2] = i/L + i + L + 2
            ans[i][3] = i/L + i + L + 1
    return ans
#print nod(4, 3)

#第二步，插值
def interp(xy):
    def nk(k):
        def wk(x, y):
            return (x - xy[(k+2)%4][0])*(y - xy[(k+2)%4][1])
        def lk(x, y):
            return 1.0*wk(x, y)/wk(xy[k][0], xy[k][1])
        return lk
    return  [nk(i) for i in range(4)]

#xy = [[2, 0], [3, 0], [3, 1], [2, 1]]
#print interp(xy)[1](x0, x1)

#二元函数求偏导
def f_p(f):
    def fpx(o, y):      #f偏x
        g = diff(f(x0, y), x0)
        g = re.sub(str(x0), "o", str(g))
        return eval(g)
    def fpy(x, o):      #f偏y
        g = diff(f(x, x1), x1)
        g = re.sub(str(x1), "o", str(g))
        return eval(g)
    return [fpx, fpy]

"""
def f(x, y):
    return x**3*y**2
print f_p(f)[0](x0, x1)
print f_p(f)[1](x0, x1)
"""
#插值函数求偏导
def interp_1(xy):
    def nk_1(k):
        return f_p(interp(xy)[k])
    return [nk_1(k) for k in range(4)]

#print interp_1(xy)[1][0](x0, x1)
#print interp_1(xy)[1][1](x0, x1)



#第三步，得到单元刚度矩阵与单元荷载
class Ele2:
    def __init__(self, f, xy):   #xy为每个单元上的节点
        self.f = f
        self.L = interp(xy)      #插值基函数
        self.L_1 = interp_1(xy)
        self.xy = xy

    def ke(self):
        k = np.zeros((4, 4))
        def h(s, t):
            def g(x, y):
                return self.L_1[s][0](x, y)*self.L_1[t][0](x, y) + self.L_1[s][1](x, y)*self.L_1[t][1](x, y)
            return g
        for i in range(4):
            for j in range(4):
                k[i][j] = Intergral_2().guass_leg_2_comp(h(i, j), (self.xy[0][0], self.xy[1][0]), (self.xy[0][1], self.xy[-1][1]))
        return k

    def fe(self):
        ff = np.zeros(4)
        def h(k):
            def g(x, y):
                return self.f(x, y)*self.L[k](x, y)
            return g
        for i in range(4):
            ff[i] = Intergral_2().guass_leg_2_comp(h(i), (self.xy[0][0], self.xy[1][0]), (self.xy[0][1], self.xy[-1][1]))
        return ff

"""
def f(x, y):
    return 2*x + 3*y
xy = [[2, 0], [3, 0], [3, 1], [2, 1]]
aa = Ele2(f, xy)
print aa.fe()
print aa.ke()
"""

#第四步，组装总刚度矩阵和总荷载向量
def KF(f, D, (H, L)):       #D可取矩形区域四个点，也可取其第1,3个点。
    Nod = nod(H, L)      #关联矩阵
    h, l = (H + 1), (L + 1)
    N = h*l              #总节点数
    K = np.zeros((N, N))
    F = np.zeros(N)
    xn = np.linspace(D[0][0], D[1][0], l)
    yn = np.linspace(D[0][1], D[-1][1], h)
    for e in Nod:
        kf = Ele2(f, [[xn[m%l], yn[m/l]] for m in e])
        [ke, fe] = [kf.ke(), kf.fe()]
        #print fe
        for i in range(4):
            F[e[i]] += fe[i]
            for j in range(4):
                K[e[i]][e[j]] += ke[i][j]
    return (K, F)
"""
def KF(f, D, (H, L)):       #D可取矩形区域四个点，也可取其第1,3个点。
    Nod = nod(H, L)      #关联矩阵
    h, l = (H + 1), (L + 1)
    N = h*l              #总节点数
    xn, yn = np.mgrid[D[0][0]:D[1][0]:l+0j, D[0][1]:D[-1][1]:h+0j]
    xn = [r[j] for j in range(h) for r in xn]
    yn = [r[j] for j in range(h) for r in yn]
    xy = [[r[j]for r in [xn, yn]]for j in range(N)]
    K = np.zeros((N, N))
    F = np.zeros(N)
    for e in Nod:
        kf = Ele2(f, [xy[int(m)] for m in e])
        [ke, fe] = [kf.ke(), kf.fe()]
        for i in range(4):
            F[e[i]] += fe[i]
            for j in range(4):
                K[e[i]][e[j]] += ke[i][j]
    return (K, F)
"""

"""
(H, L) = (2, 2)
def f(x, y):
    return 2*x + 3*y
#D = [[2, 0], [3, 0], [3, 1], [2, 1]]
D = [[2, 0], [3, 1]]
print KF((H, L), f, D)
print nod(H, L)
"""
#第五步，加边界条件，解出方程组

def bdynum(H, L):
    N = (H + 1)*(L + 1)
    b01 = range(1, L + 1)
    b12 = range(2*L + 1, N, L + 1)
    b23 = range(N - 2, N - L - 2, -1)
    b30 = range((H-1)*(L + 1), -1, -L-1)
    return b01 + b12 + b23 + b30
"""
#(H, L) = (4, 2)
#print bdynum(H, L)
"""

def bound((K, F), (g, L1)):
    for k, e in enumerate(L1):
        K[e] = 0
        K[e][e] = 1
        F[e] = g[k]
    return np.linalg.solve(np.array(K), np.array(F))


#第6步，问题求解
def fem2solve(f, D, (g, L1), (H, L)):
    (K, F) = KF(f, D, (H, L))   #总刚阵和总荷载
    return bound((K, F), (g, L1))#加边界条件,并解出方程组


#第7步，画图，利用线性方程组的解（即插值函数值），得到近似插值函数，然后画图
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



if __name__ == '__main__' :
    def f(x, y):
        #return 20*y*(1-y) + 20*x*(1-x)
        return -4
    D = [[0, 0], [1, 1]]   #矩形区域
    (H, L) = (4, 4)          #行列单元分割
    #边界条件
    L1 = bdynum(H, L)
    g = np.zeros(len(L1))

    Nod = nod(H, L)      #关联矩阵
    #print Nod
    un = fem2solve(f, D, (g, L1), (H, L))
    print un

    h, l = (H + 1), (L + 1)
    N = h*l              #总节点数
    (x, y) = np.mgrid[D[0][0]:D[1][0]:21j, D[0][1]:D[-1][1]:21j]
    z = fem2fuc((x, y), un, (H, L), D)
    pl = mlab.mesh(x, y, z)
    mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    mlab.outline(pl)
    mlab.show()
    mlab.savefig(str(H) + "_" + str(L) + 'FEM2D_Q.png')
