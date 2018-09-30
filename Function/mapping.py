#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mapping
@time: 2018/1/26  15:21
"""
import numpy as np

def mapping1D(a, b):
    return lambda x: 0.5*(b-a)*x + 0.5*(b+a)


class Map2D(object):
    def __init__(self, p):
        self.p = np.array(p)
        if len(p) == 2:
            self.p = self.p.T

        if len(self.p) == 3:     # just for quadrilateral
            self.p = np.vstack((self.p[:2, :], [(self.p[1]+self.p[2])*0.5], self.p[2:, :]))


        self.alpha_1 = [0, 0]
        self.alpha_2 = [0, 0]
        self.alpha_3 = [0, 0]
        self.alpha_4 = [0, 0]
        for i in [0, 1]:
            self.alpha_1[i] = (self.p[0][i] + self.p[2][i] - self.p[1][i] - self.p[3][i])*0.25
            self.alpha_2[i] = (self.p[1][i] + self.p[2][i] - self.p[0][i] - self.p[3][i])*0.25
            self.alpha_3[i] = (self.p[2][i] + self.p[3][i] - self.p[0][i] - self.p[1][i])*0.25
            self.alpha_4[i] = (self.p[0][i] + self.p[1][i] + self.p[2][i] + self.p[3][i])*0.25

        self.D1 = self.alpha_2[0]*self.alpha_1[1] - self.alpha_1[0]*self.alpha_2[1]
        self.D2 = self.alpha_1[0]*self.alpha_3[1] - self.alpha_3[0]*self.alpha_1[1]
        self.D3 = self.alpha_2[0]*self.alpha_3[1] - self.alpha_3[0]*self.alpha_2[1]

    def __checkxhat__(self, xHat):
        xHat = np.array(xHat)
        if len(xHat) != 2:
            xHat = xHat.T
        return xHat

    def mapping(self, xHat):
        xHat = self.__checkxhat__(xHat)
        x0 = self.alpha_1[0]*xHat[0]*xHat[1] + self.alpha_2[0]*xHat[0] + self.alpha_3[0]*xHat[1] + self.alpha_4[0]
        x1 = self.alpha_1[1]*xHat[0]*xHat[1] + self.alpha_2[1]*xHat[0] + self.alpha_3[1]*xHat[1] + self.alpha_4[1]
        return np.array([x0, x1])

    def jacobiMatrix(self, xHat):
        xHat = self.__checkxhat__(xHat)
        a = self.alpha_1[0]*xHat[1] + self.alpha_2[0]
        b = self.alpha_1[1]*xHat[1] + self.alpha_2[1]
        c = self.alpha_1[0]*xHat[0] + self.alpha_3[0]
        d = self.alpha_1[1]*xHat[0] + self.alpha_3[1]
        return np.array([[a, b], [c, d]])

    def jacobiAdjoint(self, xHat):
        mat = self.jacobiMatrix(xHat)
        a = mat[1][1]
        b = -1.0*mat[0][1]
        c = -1.0*mat[1][0]
        d = mat[0][0]
        return np.array([[a, b], [c, d]])

    def jAdTDotJAd(self, xHat):
        js = self.jacobiAdjoint(xHat)
        a = js[0][0]*js[0][0] + js[1][0]*js[1][0]
        b = js[0][0]*js[0][1] + js[1][0]*js[1][1]
        c = js[0][1]*js[0][0] + js[1][1]*js[1][0]
        d = js[0][1]*js[0][1] + js[1][1]*js[1][1]
        return np.array([[a, b],[c, d]])


    def jacobi(self, xHat):
        xHat = self.__checkxhat__(xHat)
        return self.D1*xHat[0] + self.D2*xHat[1] + self.D3

    def edgeTangentVector(self):
        newp = np.vstack((self.p[1:], self.p[0]))
        return newp - self.p

    def edgeOutNorm(self):
        tangent = self.edgeTangentVector().T
        ans = np.zeros_like(tangent)
        ans[0] = 1.0*tangent[1]/self.edgeLength()
        ans[1] = -1.0*tangent[0]/self.edgeLength()
        return ans.T

    def edgeLength(self):
        tangent = self.edgeTangentVector()
        ans = map(np.linalg.norm, tangent)
        return np.array(ans)



class Map2DT(object):
    def __init__(self, p):
        self.p = np.array(p)
        if len(p) == 2:
            self.p = self.p.T
        self.alpha_x = [0, 0]
        self.alpha_y = [0, 0]
        self.alpha_0 = [0, 0]
        for i in [0, 1]:
            self.alpha_x[i] = self.p[0][i] - self.p[2][i]
            self.alpha_y[i] = self.p[1][i] - self.p[2][i]
            self.alpha_0[i] = self.p[2][i]

    def __checkxhat__(self, xHat):
        xHat = np.array(xHat)
        if len(xHat) != 2:
            xHat = xHat.T
        return xHat

    def mapping(self, xHat):
        xHat = self.__checkxhat__(xHat)
        x0 = xHat[0]*self.alpha_x[0] + xHat[1]*self.alpha_y[0] + self.alpha_0[0]
        x1 = xHat[0]*self.alpha_x[1] + xHat[1]*self.alpha_y[1] + self.alpha_0[1]
        return np.array([x0, x1])

    def jacobi(self, xHat=[]):
        return self.alpha_x[0]*self.alpha_y[1] - self.alpha_y[0]*self.alpha_x[1]

    def jacobiMatrix(self, xHat=[]):
        return np.array([[self.alpha_x[0], self.alpha_x[1]],
                         [self.alpha_y[0], self.alpha_y[1]]])


    def jacobiAdjoint(self, xHat=[]):
        mat = self.jacobiMatrix()
        a = mat[1][1]
        b = -1.0*mat[0][1]
        c = -1.0*mat[1][0]
        d = mat[0][0]
        return np.array([[a, b], [c, d]])


    def jAdTDotJAd(self, xHat=[]):
        js = self.jacobiAdjoint()
        a = js[0][0]*js[0][0] + js[1][0]*js[1][0]
        b = js[0][0]*js[0][1] + js[1][0]*js[1][1]
        c = js[0][1]*js[0][0] + js[1][1]*js[1][0]
        d = js[0][1]*js[0][1] + js[1][1]*js[1][1]
        return np.array([[a, b], [c, d]])



if __name__ == "__main__":
    from sympy import var
    x,y = var("x,y")

    p = [[1,0],[0,1],[0,0]]

    mp = Map2DT(p)
    print mp.mapping([x,y])
    print mp.jacobi()

    # p11 = [[0,0], [1,0], [0.5,0.5], [0,1]]
    # p0 = [[0,0], [1,0], [0,1], [0,1]]
    # pp = [[-1,-1], [0,-1],[-0.5,-0.5],[-1,0]]
    # pp3d = [[0,1], [0,0], [1,0], [1,1]]
    # mppp3d = Map2D(pp3d)
    # print mppp3d.mapping([[-1,1,1,-1],[-1,-1,1,1]])
    # print mppp3d.jacobi([[-1,1,1,-1],[-1,-1,1,1]])
    # print mppp3d.mapping([x,y])
    # print mppp3d.jacobi([x,y])
    # print mppp3d.alpha_1
    # print mppp3d.alpha_2
    # print mppp3d.alpha_3
    # print mppp3d.alpha_4
    # print mppp3d.D1
    # print mppp3d.D2
    # print mppp3d.D3
    # print "----------------------------"
    # xhat = [[-1,1,1,-1],[-1,-1,1,1]]
    # mp11 = Map2D(p11)
    # print mp11.mapping([x,y])
    # print mp11.jacobi([x,y])
    # print "----------------------------"
    # mp0 = Map2D(p0)
    # print mp0.mapping([x,y])
    # print mp0.jacobi([x,y])
    #
    # print "----------------------------"
    # mpp = Map2D(pp)
    # print mpp.mapping(xhat)-np.array(pp).T
    # print mpp.jacobi(xhat)
    #
    # print mpp.edgeLength()
    # print mpp.edgeTangentVector()
    # print mpp.edgeOutNorm()