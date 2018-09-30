#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: _5_FEM1_8.py
@time: 2016-01-28  13:05
"""
from _1_Intergral_8 import Intergral_1
import  numpy as np
from sympy import*
import matplotlib.pyplot as plt
import re

#一维有限元
"""
一般性问题:
(pu')' - qu + f = 0    x in [a, b]
-p(a)u'(a) + ar*u(a) = A
p(a)u'(b) + bt*u(b) = B

问题中涉及的变量：
函数变量((p, q, f), (a, b))
边界变量((pua, ar, A), (pub, bt, B))
分点变量(n, ne),n为单元个数，ne为每个单元的节点个数，
一旦确定好每个单元节点数ne，该程序会自动识别插值多项式为ne-1阶


程序的功能：
输入问题中的所有变量，就可以获得相应方程组的解，并且画出图像

"""

var(["x"+str(i) for i in range(5)])


#第1步，离散，得到关联矩阵nod
def nod(n, ne): #n为单元数，ne为每个单元节点数
    d = np.zeros((n, ne))
    for i in range(n):
        for j in range(ne):
            d[i][j] = (ne - 1)*i + j
    return d
#print nod(8, 3)


#第2步，插值。
def interp(xn):
    def nk(k):
        def wk(x):
            ans = 1.0
            for i in range(len(xn)):
                if  i != k:
                    ans *= x - xn[i]
            return ans
        def lk(x):
            return wk(x)/wk(xn[k])
        return lk
    return [nk(j) for j in range(len(xn))]
print interp([1,2,3])[0](5)

#函数求导
def f_1(f):
    def f1(o):
        g = diff(f(x0), x0)
        g = re.sub(str(x0), "o", str(g))
        return eval(g)
    return f1

#插值函数求导
def interp_1(xn):
    def nk_1(k):
        return f_1(interp(xn)[k])
    return [nk_1(j) for j in range(len(xn))]
#print interp_1([1,2,3])[0](6)


#第3步，得到单元刚度矩阵与单元荷载.
class Ele:
    def __init__(self, (p, q, f),  xn):   #xn为每个单元上的节点
        self.p = p
        self.q = q
        self.f = f
        self.L = interp(xn)      #插值基函数
        self.L_1 = interp_1(xn)
        self.ne = len(xn)    #每个单元节点个数
        self.xn = xn

    def ke(self):
        k = np.zeros((self.ne, self.ne))
        def h(s, t):
            def F(x):
                return self.L_1[s](x)*self.L_1[t](x)*self.p(x) + self.L[s](x)*self.L[t](x)*self.q(x)
            return F
        for i in range(self.ne):
            for j in range(self.ne):
                k[i][j] = Intergral_1().guass_leg_1_comp(h(i, j), (self.xn[0], self.xn[-1]))
        return k

    def fe(self):
        ff = np.zeros(self.ne)
        def h(s):
            def F(x):
                return self.f(x)*self.L[s](x)
            return F
        for i in range(self.ne):
            ff[i] = Intergral_1().guass_leg_1_comp(h(i), (self.xn[0], self.xn[-1]))
        return ff


#第4步，组装成总刚度矩阵和总荷载向量
def KF(Nod, (p, q, f), (a, b)):
    ne = Nod.shape[1]
    N = Nod[-1][-1] + 1
    K = np.zeros((N, N))
    F = np.zeros(N)
    x = np.linspace(a, b, N)
    ke = Ele((p, q, f), [x[m] for m in range(ne)]).ke()
    for e in Nod:
        fe = Ele((p, q, f), [x[m] for m in e]).fe()
        for i in range(ne):
            F[e[i]] += fe[i]
            for j in range(ne):
                K[e[i]][e[j]] += ke[i][j]
    return (K, F)

"""
def KF(Nod, (p, q, f), (a, b)):
    ne = Nod.shape[1]
    N = Nod[-1][-1] + 1
    K = np.zeros((N, N))
    F = np.zeros(N)
    x = np.linspace(a, b, N)
    for e in Nod:
        kf = Ele((p, q, f), [x[m] for m in e])
        [ke, fe] = [kf.ke(), kf.fe()]
        for i in range(ne):
            F[e[i]] += fe[i]
            for j in range(ne):
                K[e[i]][e[j]] += ke[i][j]
    return (K, F)
"""

#第5步，加边界条件,并解出方程组
def bound((K, F), (pua, ar, A), (pub, bt, B)):
    if pua != 0:
        K[0][0] += ar
        F[0] += A
    elif ar != 0:
        F[0] = 1.0*A/ar
        K[0] = 0
        K[0][0] = 1
    else:
        K, F = K, F
    if pub != 0:
        K[-1][-1] += bt
        F[-1] += B
    elif bt != 0:
        F[-1] = 1.0*B/bt
        K[-1] = 0
        K[-1][-1] = 1
    return np.linalg.solve(np.array(K), np.array(F))


#第6步，问题求解
def femsolve((p, q, f), (a, b), (pua, ar, A), (pub, bt, B), (n, ne)):
    Nod = nod(n, ne)  #关联矩阵
    (K, F) = KF(Nod,  (p, q, f), (a, b))   #总刚阵和总荷载
    return bound((K, F), (pua, ar, A), (pub, bt, B))  #加边界条件,并解出方程组


#第7步，画图，利用线性方程组的解（即插值函数值），得到近似插值函数，然后画图
def femfuc(x, un, Nod, (a, b)):
    def f(t, xe, ue):
        ans = 0
        for i in range(len(xe)):
            ans += ue[i]*interp(xe)[i](t)
        return ans
    def fk(k, t):
        xe = [xn[i]for i in Nod[k]]
        ue = [un[j]for j in Nod[k]]
        return f(t, xe, ue)
    N = Nod[-1][-1] + 1
    xn = np.linspace(a, b, N)
    ans = np.zeros(len(x))
    for i in range(len(x)):
        for k in range(len(Nod)):
            if xn[Nod[k][0]] <= x[i] <= xn[Nod[k][-1]]:
                ans[i] = fk(k, x[i])
                break
    return ans

def erro(n, ne):
    un = femsolve((p, q, f), (a, b), (pua, ar, A), (pub, bt, B), (n, ne))

    x = np.linspace(a, b, n*ne - n + 1)
    uture = np.sin(np.pi*x)

    uerro = np.max(np.abs(np.array(un) - np.array(uture)))
    return uerro

#测试
if __name__ == '__main__' :
    def p(x):
        return 1 + 0*x
    def q(x):
        return 1 + 0*x
    def f(x):
        return (np.pi**2 + 1)*np.sin(np.pi*x)
    (a, b) = (0, 1)             #区间[a, b]
    (pua, ar, A) = (0, 1, 0)    #边界条件a
    (pub, bt, B) = (0, 1, 0)    #边界条件b
    ne = 1
    """
    print erro(8, ne)
    print
    print erro(16, ne)
    print
    print erro(32, ne)
    print
    print erro(64, ne)
    print
    print erro(128, ne)
    print



    #一次多项式的误差阶数
    #print np.log(erro(1, 2)/erro(2, 2))/np.log(2)
    #print np.log(erro(2, 2)/erro(4, 2))/np.log(2)
    #print np.log(erro(4, 2)/erro(8, 2))/np.log(2)
    print np.log(erro(8, 2)/erro(16, 2))/np.log(2)
    print np.log(erro(16, 2)/erro(32, 2))/np.log(2)
    print np.log(erro(32, 2)/erro(64, 2))/np.log(2)
    print np.log(erro(64, 2)/erro(128, 2))/np.log(2)


    #二次多项式的误差阶数
    #print np.log(erro(1, 3)/erro(2, 3))/np.log(2)
    #print np.log(erro(2, 3)/erro(4, 3))/np.log(2)
    print np.log(erro(4, 3)/erro(8, 3))/np.log(2)
    print np.log(erro(8, 3)/erro(16, 3))/np.log(2)
    print np.log(erro(16, 3)/erro(32, 3))/np.log(2)
    print np.log(erro(32, 3)/erro(64, 3))/np.log(2)
    print np.log(erro(64, 3)/erro(128, 3))/np.log(2)



    #三次多项式的误差阶数
  
    print np.log(erro(8, 4)/erro(16, 4))/np.log(2)
    print np.log(erro(16, 4)/erro(32, 4))/np.log(2)
    print np.log(erro(32, 4)/erro(64, 4))/np.log(2)
    print np.log(erro(64, 4)/erro(128, 4))/np.log(2)
 
    #四次
    #print np.log(erro(1, 5)/erro(2, 5))/np.log(2)
    #print np.log(erro(2, 5)/erro(4, 5))/np.log(2)
    #print np.log(erro(4, 5)/erro(8, 5))/np.log(2)


    """
    (n, ne) = (4, 3)            #n为单元数，ne为每个单元节点数
    #上面是输入的变量，下面是输出的结果

    Nod = nod(n, ne)     #Nod关联矩阵
    N = Nod[-1][-1] + 1  #N总结点数
    xn = np.linspace(a, b, N)  #xn插值节点
    un = femsolve((p, q, f), (a, b), (pua, ar, A), (pub, bt, B), (n, ne))
    #un插值节点上的函数值
    #print Nod
    #print xn
    #print un
    x = np.linspace(a, b, 45) 
    y = femfuc(x, un, Nod, (a, b))
    
    plt.plot(xn, un, "*", label = "Root")
    plt.plot(x, y, label="Interped")
    plt.plot(x, np.sin(np.pi*x), label="Ture")
    plt.title(str(n) + " element and " + str(ne-1) + u" powers polynomial interpolation", fontsize=16, color='r')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.savefig(str(n) + "_" + str(ne) + 'FEM1D.png')
    #plt.savefig('FEM1D.png')
