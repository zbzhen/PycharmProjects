#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: functionQuad
@time: 2018/1/11  10:23
Functional integration, normal, interpolation
"""
import sys
sys.path.append(r'..')
import numpy as np
from pyGrid2D.Grid2D import Grid2D
from numpy.polynomial import legendre
from mapping import mapping1D, Map2D

# Get integral  points and weights
class Quadrature(object):
    def __init__(self, n):
        ideg = int(n)
        if ideg != n or n < 1:
            raise ValueError("n must be a non-negative integer")
        self.permuteData = n
        self.points = []
        self.weights = []

    # A standard  code to get the lobatto points and weights
    def getLobattoPiontsWeights(self):
        if self.permuteData == 2:
            self.points = np.array([-1, 1])
            self.weights = np.array([1, 1])
            return self.points, self.weights
        u = [np.sqrt(1.0*j/(2*j+1)*(j+2)/(2*j+3)) for j in range(1, self.permuteData-2)]
        bp = np.linalg.eigvals(np.diag(u, 1) + np.diag(u, -1))
        self.points = np.hstack(([-1], np.sort(bp), [1]))
        n = self.permuteData - 1
        lx = legendre.legval(self.points, [0]*n+[1])
        self.weights = 2.0/(n*lx*(n+1)*lx)
        return self.points, self.weights

    # A standard  code to get the gauss points and the weights
    def getGuassPointsWeights(self):
        self.points, self.weights = legendre.leggauss(self.permuteData)
        return self.points, self.weights

    def getTriangularPointsWeights(self, n):
        if n == 4:
            self.points = np.array([[1.0/3.0, 0.6, 0.2, 0.2], [1.0/3.0, 0.2, 0.6, 0.2]])
            self.weights = np.array([-27.0/48.0, 25.0/48.0, 25.0/48.0, 25.0/48.0])*0.5
        if n == 6:
            self.points = np.array([[0.44594849091597, 0.44594849091597, 0.10810301816807, 0.09157621350977, 0.09157621350977, 0.81684757298046],
                                [0.44594849091597, 0.10810301816807, 0.44594849091597, 0.09157621350977, 0.81684757298046, 0.09157621350977]])
            self.weights = 0.5*np.array([0.22338158967801, 0.22338158967801, 0.22338158967801, 0.10995174365532, 0.10995174365532, 0.10995174365532])


        return self.points, self.weights


class FuncQuad(object):
    def __init__(self, func, quad, grid=[], interp=[]):
        # function
        self.func = func
        self.identityfunc = lambda x: x

        # grid and mapping
        self.grid = grid
        self.mapping = lambda x: x
        self.jacobi = lambda x: x

        # quadrature
        self.N = quad.permuteData
        self.qp = quad.points
        self.qw = quad.weights
        self.qp2d = np.array(np.meshgrid(self.qp, self.qp))

        # sub element
        self.nx = 1
        self.ny = 1

        # matrix
        self.matrixW = np.outer(self.qw, self.qw)
        self.matrixF = []

        # interpolation and interpolate matrix
        if interp != []:
            self.p = len(interp)
            self.ip = interp
            self.matrixH = self.__mathbbHxieta__(lambda x: x)
            self.matrixHt = self.matrixH.T
            self.ip2d = np.array(np.meshgrid(self.ip, self.ip))

    def __mathbbF__(self):
        x = self.mapping(self.ip2d)
        return self.func(x)

    def __mathbbHxieta__(self, mapping=lambda x: x):
        mat = np.zeros((self.p, self.N))
        mapqp = mapping(self.qp)   # quadrature points
        abssort = lambda x: x[abs(x).argsort()]   # sort: For the sake of the more precision
        for i in range(self.p):
            ip = np.delete(self.ip, i)
            denominator = abssort(ip - self.ip[i])           # interpolate points
            for j in range(self.N):
                numerator = abssort(ip - mapqp[j])              # quadrature points
                mat[i][j] = (numerator/denominator).prod()
        return mat


    def __mathbbJ__(self, mapping):
        x = mapping(self.qp2d)
        return self.jacobi(x)


    def __mathbbFHat__(self, mapping):
        x = mapping(self.qp2d)
        return self.func(x)


    def __eleL2errorSquare__(self):
        if self.nx * self.ny == 1:
            m = np.dot(self.matrixHt, self.matrixF)
            t = self.__mathbbFHat__(self.mapping) - np.dot(m, self.matrixH)
            return t*t*self.__mathbbJ__(self.identityfunc)
        def tmp(mapxi, mapeta, map1, map2):
            m = np.dot(self.__mathbbHxieta__(mapeta).T, self.matrixF)
            t = self.__mathbbFHat__(map2) - np.dot(m, self.__mathbbHxieta__(mapxi))
            return t*t*self.__mathbbJ__(map1)
        ans = np.zeros((self.N, self.N))
        hx = 2.0/(1.0*self.nx)
        hy = 2.0/(1.0*self.ny)
        for i in range(self.nx):
            mapxi = mapping1D(-1.0 + hx*i, -1.0 + hx*(i+1))
            for j in range(self.ny):
                mapeta = mapping1D(-1.0 + hy*j, -1.0 + hy*(j+1))
                map1 = lambda x: np.array([mapxi(x[0]), mapeta(x[1])])
                map2 = lambda x: self.mapping(map1(x))
                ans += tmp(mapxi, mapeta, map1, map2)
        return np.array(ans)

    def __eleFphiQuad__(self, m, n):
        if self.nx * self.ny == 1:
            t = self.__mathbbFHat__(self.mapping)*np.outer(self.matrixH[m], self.matrixH[n])
            return t*self.__mathbbJ__(self.identityfunc)
        def tmp(mapxi, mapeta, map1, map2):
            t = np.outer(self.__mathbbHxieta__(mapeta)[m], self.__mathbbHxieta__(mapxi)[n])
            return self.__mathbbFHat__(map2)*t*self.__mathbbJ__(map1)
        ans = np.zeros((self.N, self.N))
        hx = 2.0/(1.0*self.nx)
        hy = 2.0/(1.0*self.ny)
        for i in range(self.nx):
            mapxi = mapping1D(-1.0 + hx*i, -1.0 + hx*(i+1))
            for j in range(self.ny):
                mapeta = mapping1D(-1.0 + hy*j, -1.0 + hy*(j+1))
                map1 = lambda x: np.array([mapxi(x[0]), mapeta(x[1])])
                map2 = lambda x: self.mapping(map1(x))
                ans += tmp(mapxi, mapeta, map1, map2)
        return np.array(ans)

    def __eleQuad__(self):
        if self.nx * self.ny == 1:
            return self.__mathbbFHat__(self.mapping)*self.__mathbbJ__(self.identityfunc)
        ans = np.zeros((self.N, self.N))
        hx = 2.0/(1.0*self.nx)
        hy = 2.0/(1.0*self.ny)
        for i in range(self.nx):
            mapxi = mapping1D(-1.0 + hx*i, -1.0 + hx*(i+1))
            for j in range(self.ny):
                mapeta = mapping1D(-1.0 + hy*j, -1.0 + hy*(j+1))
                map1 = lambda x: np.array([mapxi(x[0]), mapeta(x[1])])
                map2 = lambda x: self.mapping(map1(x))
                ans += self.__mathbbFHat__(map2)*self.__mathbbJ__(map1)
        return ans

    def interpolateL2error(self):
        ans = np.zeros((self.N, self.N))
        for i, ele in enumerate(self.grid.elements):
            mp = Map2D(self.grid.points[ele])
            self.mapping = mp.mapping
            self.jacobi = mp.jacobi
            self.matrixF = self.__mathbbF__()
            ans += self.__eleL2errorSquare__()
        ans = ans*self.matrixW
        return np.sqrt(ans.sum())/np.sqrt(self.nx*self.ny)

    def femSolutionL2error(self, uh):
        ans = np.zeros((self.N, self.N))
        self.matrixF = np.zeros((self.p, self.p))
        uhdim = uh.ndim
        quadtofree = self.grid.quadtofree
        freetoquad = self.grid.freetoquad
        for i, ele in enumerate(self.grid.elements):
            if uhdim == 1:
                for j in range(self.p*self.p):
                    jx, jy = j / self.p, j % self.p
                    J = quadtofree[j]
                    # J = freetoquad[j]
                    self.matrixF[jx][jy] = uh[self.grid.gindex[i][J]]
            elif uhdim == 2:
                self.matrixF = np.reshape(uh[i], (self.p, self.p))
            else:
                self.matrixF = uh[i]
            mp = Map2D(self.grid.points[ele])
            self.mapping = mp.mapping
            self.jacobi = mp.jacobi
            ans += self.__eleL2errorSquare__()
        ans = ans*self.matrixW
        return np.sqrt(ans.sum())/np.sqrt(self.nx*self.ny)

    def functionQuad(self):
        ans = np.zeros((self.N, self.N))
        for i, ele in enumerate(self.grid.elements):
            mp = Map2D(self.grid.points[ele])
            self.mapping = mp.mapping
            self.jacobi = mp.jacobi
            ans += self.__eleQuad__()
        ans = ans*self.matrixW
        return ans.sum()/(self.nx*self.ny)

    def fphiQuad(self, m, n):
        ans = np.zeros((self.N, self.N))
        for i, ele in enumerate(self.grid.elements):
            mp = Map2D(self.grid.points[ele])
            self.mapping = mp.mapping
            self.jacobi = mp.jacobi
            ans += self.__eleFphiQuad__(m, n)
        ans = ans*self.matrixW
        return ans.sum()/(self.nx*self.ny)


    def interpolateQuad(self):
        ans = np.zeros((self.N, self.N))
        for i, ele in enumerate(self.grid.elements):
            mp = Map2D(self.grid.points[ele])
            self.mapping = mp.mapping
            self.jacobi = mp.jacobi
            m = np.dot(self.matrixHt, self.__mathbbF__())
            ans += np.dot(m, self.matrixH)*self.__mathbbJ__(self.mapping)
        ans = ans*self.matrixW
        return ans.sum()



if __name__ == "__main__":
    # test function
    def f(x):
        r = x[0]*x[0]+x[1]*x[1]
        # return np.cos(np.pi*r)
        # x = np.array(x)
        # return x[0]
        return x[0]**2.5 + x[1]**2.5
        return np.sqrt((x[0]+x[1])**5)
        # # ans = ((x[0]+x[1])*(x[0]+x[1]))**(5.0/2.0)
        return ans
    # 9.14285714286
    grid = Grid2D()
    path = "..//testmesh//rectangle01//"
    filenames = ["meshR.dat", "meshRRR.dat", "AddDensity_1_meshRRR.dat",
                 "AddDensity_2_meshRRR.dat", "AddDensity_3_meshRRR.dat", "AddDensity_4_meshRRR.dat"]
    filename = filenames[1]

    # datafiles = ["meshRT.dat", "AddDensity_1_meshRT.dat",
    #             "AddDensity_2_meshRT.dat", "AddDensity_3_meshRT.dat", "AddDensity_4_meshRT.dat"]
    # filename = datafiles[1]
    # path = "..//testmesh//RT11//"

    grid.from_meshdat_get_pte(path+filename)
    # grid.setpte(points= [[-1,-1],[1,-1],[1,1],[-1,1]], elements=[[0,1,2,3]])
    # print grid.points
    # print grid.elements

    x0 = np.array([ -0.125,                0.625 ,               0.625  ,            -0.125])
    x1 = np.array([ -0.0559016994374947,    0.220491502812526 ,   0.934016994374947,  -0.0986067977499789])
    x2 = np.array([0.0559016994374947 ,  -0.184016994374947  ,  0.779508497187474   , 0.348606797749979])
    p = 3
    interp = Quadrature(p+1)
    interp.getLobattoPiontsWeights()

    t = 3
    print (interp.points**t*x0).sum()
    print (interp.points**t*x1).sum()
    print (interp.points**t*x2).sum()
    y = 0.5*interp.points + 0.5
    print interp.points
    print y
    print y**t


    p = 12
    interp = Quadrature(p+1)
    interp.getLobattoPiontsWeights()

    N = p+12
    quad = Quadrature(N)
    quad.getGuassPointsWeights()
    # quad.getLobattoPiontsWeights()

    fq = FuncQuad(f, quad, grid, interp.points)
    nn = 2
    fq.nx, fq.ny = nn, nn

    # print fq.matrixH

    # ans = 0
    # for i in range(grid.Nelement):
    #     subfq = FuncQuad(f, quad, grid.getsubgrid(i))
    #     print subfq.functionQuad()
    #     print subfq.__mathbbFHat__(subfq.mapping)
    #     ans += subfq.functionQuad()
    # print ans

    print "interpolateL2error for deg = ", p
    print fq.interpolateL2error()
    # print "interpolation quad = \n",fq.interpolateQuad()
    print "functional quad = \n",fq.functionQuad()
    print "fphiQuad quad = \n",fq.fphiQuad(0, 0)
    # print "functional exact quad = \n",9.0/5.0*4**(1.0/3.0)
    # print "functional exact quad = \n",36.0/13.0*2**(1.0/3.0)


