#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:03
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : femdiffusionVector2dT.py
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
        self.Dof = (self.grid.Npoint + self.grid.Nedge)*2
        pass

    def getGloabIndex(self, ic):
        index = np.array(range(12))
        a = (self.grid.elements[ic])
        c = (self.grid.Npoint + self.grid.NumEdge[ic])
        t = np.array(range(3))
        index[t] = a*2
        index[t+3] = c*2
        index[t+6] = a*2+1
        index[t+9] = c*2+1
        return index

    def getTrailCoord(self):
        ans = np.array([[1, 0, 0, 0.5, 0, 0.5], [0, 1, 0, 0.5, 0.5, 0]])
        return ans


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
        self.MLM = np.zeros((du*2, du*2))
        self.MLM[:du, :du] = MLM
        self.MLM[du:, du:] = MLM
        return self.MLM


    def computeRHS(self):
        du = 6
        phi = self.interp.phi(self.interp.qp, 2)
        self.RHS = np.zeros(self.Dof)
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            fx0 = self.knownfunc.rhf(x)[0]
            fx1 = self.knownfunc.rhf(x)[1]
            index = self.getGloabIndex(ic)
            for i in range(du):
                tmp0 = (fx0*self.interp.qw*phi[i]).sum()*ja
                tmp1 = (fx1*self.interp.qw*phi[i]).sum()*ja
                self.RHS[index[i]] += tmp0
                self.RHS[index[i+du]] += tmp1
        return


    def assemble(self):
        eledof = 6*2
        from scipy.sparse import lil_matrix
        self.SMGM = lil_matrix((self.Dof, self.Dof))
        for ic in range(self.grid.Nelement):
            self.computeLocalMatrices(ic)
            index = self.getGloabIndex(ic)
            for i in range(eledof):
                for j in range(eledof):
                    self.SMGM[index[i], index[j]] += self.MLM[i][j]
        return

    def getBoundaryInformation(self):
        poly = 3
        deg = 2
        # boundary vertex
        bi = set(self.grid.bounds.T[0]) | set(self.grid.bounds.T[1])
        bi = np.array(list(bi))
        bv = self.knownfunc.bc((self.grid.points[bi]).T)
        nv = len(bi)
        t = np.array(range(nv))
        bindex = np.array(range(nv*2))
        bindex[t*2] = bi*2
        bindex[t*2+1] = bi*2+1
        bvalue = np.zeros(nv*2)
        bvalue[t*2] = bv[0]
        bvalue[t*2+1] = bv[1]
        # boundary inner node
        for edge in self.grid.outEdge:
            ic, ie = edge   # element and local edge index
            iL, iR = self.grid.elements[ic][ie], self.grid.elements[ic][(ie+1) % poly]
            a, b = self.grid.points[[iL, iR]]         # edge two vertexes
            x = 0.5*(a + b)
            value = self.knownfunc.bc(np.array(x))
            tt = self.grid.Npoint + self.grid.NumEdge[ic][ie]
            bindex = np.hstack((bindex, [tt*2, tt*2+1]))
            bvalue = np.hstack((bvalue, value))
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

        tmp = np.zeros(self.Dof)
        tmp[self.bindex] = self.bvalue
        self.RHS -= self.SMGM.dot(tmp)
        self.RHS[self.bindex] = self.bvalue
        self.SMGM[self.bindex, :] = 0.0
        self.SMGM[:, self.bindex] = 0.0
        self.SMGM[self.bindex, self.bindex] = 1.0
        # print self.RHS - self.SMGM.dot(self.getUpVector())

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
        # print self.RHS - self.SMGM.dot(self.solution)
        end = time.clock()
        print "Solve linear system time = ", end-start
        return

    def getUpVector(self):
        UpVector = np.zeros(self.Dof)
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            elenodecoord = mp.mapping(self.getTrailCoord())
            eleu = self.knownfunc.exactsolution(elenodecoord)
            index = self.getGloabIndex(ic)
            UpVector[index] = np.hstack((eleu[0], eleu[1]))
        return UpVector

    # def interpL2error(self):
    #     ans = 0.0
    #     phi = self.interp.phi(self.interp.qp, 2)
    #     for ic in range(self.grid.Nelement):
    #         elepoints = self.grid.points[self.grid.elements[ic]]
    #         mp = Map2DT(elepoints)
    #         ja = mp.jacobi()
    #         x = mp.mapping(self.interp.qp)
    #         elenodecoord = mp.mapping(self.getTrailCoord())
    #         eleui = self.knownfunc.exactsolution(elenodecoord)
    #         eleu = self.knownfunc.exactsolution(x)
    #         tmp0 = eleu[0] - np.dot(eleui[0], phi)
    #         tmp1 = eleu[1] - np.dot(eleui[1], phi)
    #         ans += (tmp0*tmp0 + tmp1*tmp1).sum()*ja
    #     return np.sqrt(ans)
    #

    def interpL2error(self):
        ans = 0.0
        phi = self.interp.phi(self.interp.qp, 2)
        t = np.array(range(6))
        ui = self.getUpVector()
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            index = self.getGloabIndex(ic)
            eleuh = ui[index]
            eleu = self.knownfunc.exactsolution(x)
            tmp0 = eleu[0] - np.dot(eleuh[t], phi)
            tmp1 = eleu[1] - np.dot(eleuh[t+6], phi)
            ans += (tmp0*tmp0 + tmp1*tmp1).sum()*ja
        return np.sqrt(ans)


    def L2error(self):
        ans = 0.0
        phi = self.interp.phi(self.interp.qp, 2)
        t = np.array(range(6))
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            index = self.getGloabIndex(ic)
            eleuh = self.solution[index]
            eleu = self.knownfunc.exactsolution(x)
            tmp0 = eleu[0] - np.dot(eleuh[t], phi)
            tmp1 = eleu[1] - np.dot(eleuh[t+6], phi)
            ans += (tmp0*tmp0 + tmp1*tmp1).sum()*ja
        return np.sqrt(ans)

    def plotuh(self, axes):
        from pylab import quiver, quiverkey
        # self.grid.plotmesh2d(axes)
        for edge in self.grid.outEdge:
            ic, ie = edge   # element and local edge index
            iL, iR = self.grid.elements[ic][ie], self.grid.elements[ic][(ie+1) % self.grid.poly]
            pp = self.grid.points[[iL, iR]].T
            axes.plot(pp[0], pp[1], color='black', linestyle='solid', markerfacecolor='black', linewidth=1)

        sDof = self.grid.Npoint + self.grid.Nedge
        id = np.array(range(sDof))
        u = self.solution[id*2]
        v = self.solution[id*2+1]
        xtmp, ytmp = self.grid.points.T
        x = np.zeros(sDof)
        y = np.zeros(sDof)
        x[:self.grid.Npoint] = xtmp
        y[:self.grid.Npoint] = ytmp
        t = 0
        for edge in self.grid.EdgeMessage1:
            ic, ie = edge   # element and local edge index
            iL, iR = self.grid.elements[ic][ie], self.grid.elements[ic][(ie+1) % self.grid.poly]
            a, b = self.grid.points[[iL, iR]]         # edge two vertexes
            mid = 0.5*(a + b)
            x[t+self.grid.Npoint] = mid[0]
            y[t+self.grid.Npoint] = mid[1]
            t += 1
            pass
        Q = quiver(x, y, u, v,
                   pivot='mid', color='r', units='inches')
        quiverkey(Q, 0.5, 0.03, 1, r'${\bf u} = (1,0)$', fontproperties={'weight': 'bold'})
        # axes.plot( x, y, 'k.')
        return