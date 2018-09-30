#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 14:15
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : femdiffusion2dT.py
# @version : Python 2.7.6
import sys
sys.path.append(r'..')
sys.path.append(r'../..')
import numpy as np
from Function.mapping import Map2DT


class CG2DT(object):
    def __init__(self, knownfunc, grid, interp):
        self.knownfunc = knownfunc
        self.grid = grid
        self.interp = interp
        self.MLM = []
        self.RHS = []
        self.SMGM = []
        self.solution = []
        pass

    def getGloabIndex(self, ic):
        index = []
        index += (self.grid.elements[ic]).tolist()
        index += (self.grid.Npoint + self.grid.NumEdge[ic]).tolist()
        return index

    def getTrailCoord(self):
        ans = np.array([[1, 0, 0, 0.5, 0, 0.5], [0, 1, 0, 0.5, 0.5, 0]])
        return ans


    def computeLocalMatricestest(self, ic):
        elepoints = self.grid.points[self.grid.elements[ic]]
        mp = Map2DT(elepoints)
        ja = mp.jacobi()
        tmp = mp.jAdTDotJAd()
        deg = 1
        du = 3*deg
        MLM = np.zeros((du, du))
        kxx, kxy, kyy = self.interp.mathbbK(deg)
        for i in range(du):
            for j in range(du):
                MLM[i][j] = (kxx[i][j]*tmp[0][0] +
                             kxy[i][j]*tmp[0][1] +
                             kxy[j][i]*tmp[1][0] +
                             kyy[i][j]*tmp[1][1])/ja
        return MLM


    def computeLocalMatrices(self, ic):
        elepoints = self.grid.points[self.grid.elements[ic]]
        mp = Map2DT(elepoints)
        ja = mp.jacobi()
        tmp = mp.jAdTDotJAd()
        du = 6
        MLM = np.zeros((du, du))
        kxx, kxy, kyy = self.interp.mathbbK(2)
        for i in range(du):
            for j in range(du):
                MLM[i][j] = (kxx[i][j]*tmp[0][0] +
                             kxy[i][j]*tmp[0][1] +
                             kxy[j][i]*tmp[1][0] +
                             kyy[i][j]*tmp[1][1])/ja
        self.MLM = MLM
        return MLM


    def computeRHS(self):
        du = 6
        phi = self.interp.phi(self.interp.qp, 2)

        self.RHS = np.zeros(self.grid.Npoint + self.grid.Nedge)
        for ic in range(self.grid.Nelement):
            tmp = np.zeros(du)
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            fx = self.knownfunc.rhf(x)
            index = self.getGloabIndex(ic)
            for i in range(du):
                tmp[i] = (fx*self.interp.qw*phi[i]).sum()*ja
                self.RHS[index[i]] += tmp[i]
        return


    def assemble(self):
        du = 6
        Dof = self.grid.Npoint + self.grid.Nedge
        from scipy.sparse import lil_matrix
        self.SMGM = lil_matrix((Dof, Dof))
        for ic in range(self.grid.Nelement):
            self.computeLocalMatrices(ic)
            index = self.getGloabIndex(ic)
            for i in range(du):
                for j in range(du):
                    self.SMGM[index[i], index[j]] += self.MLM[i][j]
        return

    def getBoundaryInformation(self):
        poly = 3
        deg = 2
        # boundary vertex
        bindex = set(self.grid.bounds.T[0]) | set(self.grid.bounds.T[1])
        bindex = list(bindex)
        bvalue = self.knownfunc.bc((self.grid.points[bindex]).T)
        # boundary inner node
        for edge in self.grid.outEdge:
            ic, ie = edge   # element and local edge index
            iL, iR = self.grid.elements[ic][ie], self.grid.elements[ic][(ie+1) % poly]
            a, b = self.grid.points[[iL, iR]]         # edge two vertexes
            x = 0.5*(a + b)  # remove two vertexes
            value = self.knownfunc.bc(np.array(x))
            edgeindex = self.grid.NumEdge[ic][ie]
            start = self.grid.Npoint + edgeindex*(deg - 1)
            bindex += range(start, start+deg-1)
            bvalue = np.hstack((bvalue, [value]))
        self.bindex = bindex
        self.bvalue = bvalue
        return

    def solve(self):
        print "begin computeRHS"
        self.computeRHS()
        print "begin assemble"
        self.assemble()
        print "begin getBoundaryInformation"
        self.getBoundaryInformation()

        Dof = self.grid.Npoint + self.grid.Nedge
        tmp = np.zeros(Dof)
        tmp[self.bindex] = self.bvalue
        self.RHS -= self.SMGM.dot(tmp)
        self.RHS[self.bindex] = self.bvalue
        self.SMGM[self.bindex, :] = 0.0
        self.SMGM[:, self.bindex] = 0.0
        self.SMGM[self.bindex, self.bindex] = 1.0

        # print "begin imposeBoundaryCondition"
        # self.imposeBoundaryCondition()
        print "begin solve linear system"
        from scipy.sparse.linalg import spsolve
        # from scipy.sparse.spmatrix import toarray
        import time
        start = time.clock()

        # print "np.linalg.cond(self.SMGM.toarray())"
        # print np.linalg.cond(self.SMGM.toarray())

        self.solution = spsolve(self.SMGM.tocsc(), self.RHS)
        self.solution[self.bindex] = self.bvalue

        end = time.clock()
        print "Solve linear system time = ", end-start
        return

    def interpL2error(self):
        ans = 0.0
        phi = self.interp.phi(self.interp.qp, 2)
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            elenodecoord = mp.mapping(self.getTrailCoord())
            eleui = self.knownfunc.exactsolution(elenodecoord)
            tmp = self.knownfunc.exactsolution(x) - np.dot(eleui, phi)
            ans += (tmp*tmp).sum()*ja
        return np.sqrt(ans)

    def L2error(self):
        ans = 0.0
        phi = self.interp.phi(self.interp.qp, 2)
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            index = self.getGloabIndex(ic)
            eleuh = self.solution[index]
            tmp = self.knownfunc.exactsolution(x) - np.dot(eleuh, phi)
            ans += (tmp*tmp).sum()*ja
        return np.sqrt(ans)