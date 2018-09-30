#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: interp
@time: 2018/1/24  23:34
"""

import numpy as np

class Interp(object):
    def __init__(self, ip, quad, computeH_1=True):
        self.deg = len(ip)-1
        self.pp = self.deg + 1
        self.ip = ip

        self.quad = quad

        self.matrixH = self.mathbbH()
        if computeH_1 == True:
            self.matrixH_1 = self.mathbbH_1()
        self.beta = lambda x: 1 + 0*x


    def mathbbH(self):
        mat = np.zeros((self.pp, self.quad.permuteData))
        abssort = lambda x: x[abs(x).argsort()]   # sort: For the sake of the more precision
        for i in range(self.pp):
            ip = np.delete(self.ip, i)
            denominator = abssort(self.ip[i] - ip)            # interpolate points
            for j in range(self.quad.permuteData):
                numerator = abssort(self.quad.points[j] - ip)   # quadrature points
                mat[i][j] = (numerator/denominator).prod()
        return mat

    def mathbbH_1(self):
        mat = np.zeros((self.pp, self.quad.permuteData))
        abssort = lambda x: x[abs(x).argsort()]   # sort: For the sake of the more precision
        if self.pp == 2:
            mat[0] = -0.5
            mat[1] = 0.5
            return mat
        for i in range(self.pp):
            ip = np.delete(self.ip, i)
            denominator = abssort(self.ip[i] - ip)     # interpolate points
            for j in range(self.quad.permuteData):
                numerator = self.quad.points[j] - ip            # quadrature points
                tmp = 0.0
                for k in range(self.deg):
                    subnu = numerator.copy()              # for deepcopy
                    subnu[k] = 1.0
                    subnu = abssort(subnu)
                    tmp += (subnu/denominator).prod()
                mat[i][j] = tmp
        return mat

    def mtilde(self, i, j):
        return (self.matrixH[i]*self.matrixH[j]*self.quad.weights).sum()

    def mhat(self, i, j):
        return (self.quad.points*self.matrixH[i]*self.matrixH[j]*self.quad.weights).sum()

    def ctilde(self, i, j):
        return (self.matrixH_1[i]*self.matrixH[j]*self.quad.weights).sum()

    def chat(self, i, j):
        return (self.quad.points*self.matrixH_1[i]*self.matrixH[j]*self.quad.weights).sum()


    def ctilde_beta(self, i, j):
        return (self.beta(self.quad.points)*self.matrixH_1[i]*self.matrixH[j]*self.quad.weights).sum()

    def chat_beta(self, i, j):
        return (self.beta(self.quad.points)*self.quad.points*self.matrixH_1[i]*self.matrixH[j]*self.quad.weights).sum()


    def __getMatrix__(self, f):
        ans = np.zeros((self.pp, self.pp))
        for i in range(self.pp):
            for j in range(self.pp):
                ans[i][j] = f(i, j)
        return ans

    def getMtMhCtCh(self):
        Mt = self.__getMatrix__(self.mtilde)
        Mh = self.__getMatrix__(self.mhat)
        Ct = self.__getMatrix__(self.ctilde)
        Ch = self.__getMatrix__(self.chat)
        return np.array([Mt, Mh, Ct, Ch])

    # def h(self, i):
    #     y = np.zeros(self.pp)
    #     y[i] = 1
    #     return lagrange(self.ip, y)
    #
    # def __finteg__(self, f):
    #     return np.dot(f(self.quad.points), self.quad.weights)
    # def mtilde(self, i, j):
    #     f = self.h(i)*self.h(j)
    #     return self.__finteg__(f)
    #
    # def mhat(self, i, j):
    #     f = self.h(i)*self.h(j)*self.xi
    #     return self.__finteg__(f)
    #
    # def ctilde(self, i, j):
    #     f = self.h(i)*self.h(j).deriv()
    #     return self.__finteg__(f)
    #
    # def chat(self, i, j):
    #     f = self.h(i)*self.h(j).deriv()*self.xi
    #     return self.__finteg__(f)


class Interp2DT(object):
    def __init__(self):
        self.qp = np.array([[1.0/3.0, 0.6, 0.2, 0.2], [1.0/3.0, 0.2, 0.6, 0.2]])
        self.qw = np.array([-27.0/48.0, 25.0/48.0, 25.0/48.0, 25.0/48.0])*0.5

        # self.qp = np.array([[0.44594849091597, 0.44594849091597, 0.10810301816807, 0.09157621350977, 0.09157621350977, 0.81684757298046],
        #                     [0.44594849091597, 0.10810301816807, 0.44594849091597, 0.09157621350977, 0.81684757298046, 0.09157621350977]])
        # self.qw = 0.5*np.array([0.22338158967801, 0.22338158967801, 0.22338158967801, 0.10995174365532, 0.10995174365532, 0.10995174365532])


    def phi(self, X, deg):
        L1 = X[0]
        L2 = X[1]
        L3 = 1.0-X[0]-X[1]
        if deg == 1:
            return np.array([L1, L2, L3])
        elif deg == 2:
            f0 = L1*(2.0*L1-1.0)
            f1 = L2*(2.0*L2-1.0)
            f2 = L3*(2.0*L3-1.0)
            f3 = 4.0*L1*L2
            f4 = 4.0*L2*L3
            f5 = 4.0*L1*L3
            return np.array([f0, f1, f2, f3, f4, f5])
        else:
            raise(" deg = 1 or 2 ")

    def gradphix(self, X, deg):
        L1=X[0]
        L2=X[1]
        L3=1.0-X[0]-X[1]
        if deg == 1:
            return np.array([1, 0, -1])
        elif deg == 2:
            f0 = 4.0*L1-1.0
            f1 = 0*(L1-L1)
            f2 = -(4.0*L3-1.0)
            f3 = 4.0*L2
            f4 = -4.0*L2
            f5 = 4.0*L3-4.0*L1
            return np.array([f0, f1, f2, f3, f4, f5])
        else:
            raise(" deg = 1 or 2 ")

    def gradphiy(self, X, deg):
        L1=X[0]
        L2=X[1]
        L3=1.0-X[0]-X[1]
        if deg == 1:
            return np.array([0, 1, -1])
        elif deg == 2:
            f0 = 0*(L1-L1)
            f1 = 4.0*L2-1.0
            f2 = -(4.0*L3-1.0)
            f3 = 4.0*L1
            f4 = 4.0*L3-4.0*L2
            f5 = -4.0*L1
            return np.array([f0, f1, f2, f3, f4, f5])
        else:
            raise(" deg = 1 or 2 ")

    def mathbbK(self, deg):
        px = self.gradphix(self.qp, deg)
        py = self.gradphiy(self.qp, deg)
        n = deg * 3  # just for deg = 1,2
        kxx = np.zeros((n, n))
        kxy = np.zeros((n, n))
        kyy = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                kxx[i][j] = (px[i]*px[j]*self.qw).sum()
                kxy[i][j] = (px[i]*py[j]*self.qw).sum()
                kyy[i][j] = (py[i]*py[j]*self.qw).sum()
        return kxx, kxy, kyy

    def mathbbCP2P1(self):
        p = self.phi(self.qp, 1)
        px = self.gradphix(self.qp, 2)
        py = self.gradphiy(self.qp, 2)
        cx = np.zeros((3,6))
        cy = np.zeros((3,6))
        for i in range(3):
            for j in range(6):
                cx[i][j] = (p[i]*px[j]*self.qw).sum()
                cy[i][j] = (p[i]*py[j]*self.qw).sum()
        return cx, cy




if __name__ == "__main__":
    from functionQuad import Quadrature
    n = 5
    quad = Quadrature(n)
    quad.getLobattoPiontsWeights()
    interp = Interp(quad.points, quad)
    print interp.__getMatrix__(interp.mtilde)
    from sympy import var
    # x,y = var("x,y")
    # it = Interp2DT()
    # a,b,c =  it.mathbbK()
    # print it.mathbbK()
    # print it.mathbbCP2P1()





    # print it.phi(np.array([[1,2,3,4],[0,1,2,3]]), 2)
    # print it.gradphix(np.array([[1,2,3,4],[0,1,2,3]]), 2)
    # print it.gradphiy(np.array([[1,2,3,4],[0,1,2,3]]), 2)
    # print it.gradphix([x,y])
    # print it.gradphiy([x,y])


    # for phi in it.phi_func():
    #     print phi([x,y])






