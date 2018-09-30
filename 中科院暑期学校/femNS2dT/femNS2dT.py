#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 16:14
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : femNS2dT.py
# @version : Python 2.7.6
import sys
sys.path.append(r'..')
sys.path.append(r'../..')
import numpy as np
from Function.mapping import Map2DT
from scipy.sparse.linalg import gmres, LinearOperator, qmr, aslinearoperator, spsolve, bicg, bicgstab, cg, cgs

class CG2DT(object):
    def __init__(self, knownfunc, grid, interp):
        self.knownfunc = knownfunc
        self.grid = grid
        self.interp = interp
        self.MLM = []
        self.RHS = []
        self.SMGM = []
        self.solution = []
        self.Dof = (grid.Npoint + grid.Nedge)*2 + grid.Npoint
        kxx, kxy, kyy = self.interp.mathbbK(2)
        cx, cy = self.interp.mathbbCP2P1()
        self.kxy = np.where(abs(kxy) < 1.0e-12, 0, kxy)
        self.kyx = self.kxy.T
        self.kxyyx = self.kxy + self.kyx
        self.kyy = np.where(abs(kyy) < 1.0e-12, 0, kyy)
        self.kxx = np.where(abs(kxx) < 1.0e-12, 0, kxx)
        self.cy = np.where(abs(cy) < 1.0e-12, 0, cy)
        self.cx = np.where(abs(cx) < 1.0e-12, 0, cx)

        # 2--100
        # 4--
        self.alpha = 1.0
        self.beta = 0.0

        pass

    def getGloabIndex(self, ic):
        eledof = 15
        index = np.array(range(eledof))
        a = self.grid.elements[ic]
        c = self.grid.Npoint + self.grid.NumEdge[ic]
        t = np.array(range(3))
        udof = (self.grid.Npoint + self.grid.Nedge)*2
        index[t] = a*2
        index[t+3] = c*2
        index[t+6] = a*2+1
        index[t+9] = c*2+1
        index[t+12] = a + udof
        return index

    def getTrailCoord(self):
        ans = np.array([[1, 0, 0, 0.5, 0, 0.5], [0, 1, 0, 0.5, 0.5, 0]])
        return ans

    # def


    def computeLocalMatrices(self):
        du = 6
        dp = 3
        eledof = 2*du + dp
        phi = self.interp.phi(self.interp.qp, 1)
        self.MLM = np.empty((self.grid.Nelement, eledof, eledof), float)
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            jastar = mp.jacobiAdjoint()
            ja = mp.jacobi()
            tmp = mp.jAdTDotJAd()*(1.0/ja)
            MLM = tmp[0][0]*self.kxx + tmp[0][1]*self.kxyyx + tmp[1][1]*self.kyy
            mathbbCx = -(jastar[0][0]*self.cx + jastar[0][1]*self.cy)
            mathbbCy = -(jastar[1][0]*self.cx + jastar[1][1]*self.cy)
            Txx = jastar[0][0]*jastar[0][0]*self.kxx + jastar[0][0]*jastar[0][1]*self.kxyyx +\
                  jastar[0][1]*jastar[0][1]*self.kyy
            Tyy = jastar[1][0]*jastar[1][0]*self.kxx + jastar[1][0]*jastar[1][1]*self.kxyyx +\
                  jastar[1][1]*jastar[1][1]*self.kyy
            Txy = jastar[0][0]*jastar[1][0]*self.kxx + jastar[0][0]*jastar[1][1]*self.kxy + \
                  jastar[0][1]*jastar[1][0]*self.kyx + jastar[0][1]*jastar[1][1]*self.kyy
            Tyx = jastar[0][0]*jastar[1][0]*self.kxx + jastar[0][0]*jastar[1][1]*self.kyx + \
                  jastar[0][1]*jastar[1][0]*self.kxy + jastar[0][1]*jastar[1][1]*self.kyy

            Txx *= self.alpha/ja
            Txy *= self.alpha/ja
            Tyx *= self.alpha/ja
            Tyy *= self.alpha/ja

            tmpMLM = np.zeros((eledof, eledof))
            tmpMLM[:du, :du] = MLM + Txx
            tmpMLM[du:2*du, du:2*du] = MLM + Tyy
            tmpMLM[:du, du:2*du] = Txy
            tmpMLM[du:2*du, :du] = Tyx
            tmpMLM[2*du:, :du] = mathbbCx
            tmpMLM[2*du:, du:2*du] = mathbbCy
            tmpMLM[:du, 2*du:] = mathbbCx.T
            tmpMLM[du:2*du, 2*du:] = mathbbCy.T
            tmpMLM[-3][2*du:] = self.beta*np.dot(phi, self.interp.qw)
            tmpMLM[-2][2*du:] = self.beta*np.dot(phi, self.interp.qw)
            tmpMLM[-1][2*du:] = self.beta*np.dot(phi, self.interp.qw)

            self.MLM[ic] = tmpMLM
        return


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

    def globalMatrixProdVector(self, gx):
        gAx = np.zeros(self.Dof)
        for ic in range(self.grid.Nelement):
            index = self.getGloabIndex(ic)
            gAx[index] += np.dot(self.MLM[ic], gx[index])
        gAx[self.bindex] = 0
        return gAx




    def preconditionfree(self, gx):
        beta = -1.0/(1.0+self.alpha)
        gAx = np.zeros(self.Dof)
        for ic in range(self.grid.Nelement):
            index = self.getGloabIndex(ic)
            mlm = self.MLM[ic]
            mlm[-3:0] = 0
            gAx[index] += np.dot(mlm, gx[index])
        gAx[self.bindex] = 0
        gAx[self.Dof-self.grid.Npoint:] = beta*gx[self.Dof-self.grid.Npoint:]
        return gAx

    def precondition(self):
        beta = -1.0/(1.0+self.alpha)
        eledof = 15
        du = 6
        from scipy.sparse import lil_matrix
        pSMGM = lil_matrix((self.Dof, self.Dof))
        for ic in range(self.grid.Nelement):
            MLM = self.MLM[ic].copy()
            MLM[2*du:, :2*du] = 0
            index = self.getGloabIndex(ic)
            for i in range(eledof):
                for j in range(eledof):
                    pSMGM[index[i], index[j]] += MLM[i][j]
        for i in range(self.Dof - self.grid.Npoint, self.Dof):
            pSMGM[i, i] = beta
        return pSMGM

    def assemble(self):
        eledof = 15
        from scipy.sparse import lil_matrix
        self.SMGM = lil_matrix((self.Dof, self.Dof))
        for ic in range(self.grid.Nelement):
            MLM = self.MLM[ic]
            index = self.getGloabIndex(ic)
            for i in range(eledof):
                for j in range(eledof):
                    self.SMGM[index[i], index[j]] += MLM[i][j]
        return



    def solve(self):
        print "begin computeRHS"
        self.computeRHS()
        print "begin computeLocalMatrices"
        self.computeLocalMatrices()
        print "begin assemble"
        self.assemble()
        print "begin getBoundaryInformation"
        self.getBoundaryInformation()
        # print self.RHS
        # print self.SMGM
        # print "-------------------------------"

        # print self.RHS - self.SMGM.dot(self.getUpVector())
        # print self.SMGM.T
        tmp = np.zeros(self.Dof)
        tmp[self.bindex] = self.bvalue
        self.RHS -= self.SMGM.dot(tmp)
        self.RHS[self.bindex] = 0
        self.SMGM[self.bindex, :] = 0.0
        self.SMGM[:, self.bindex] = 0.0
        self.SMGM[self.bindex, self.bindex] = 1.0
        pSMGM = self.precondition()
        pSMGM[self.bindex, :] = 0.0
        pSMGM[self.bindex, self.bindex] = 1.0
        pSMGM = pSMGM.tocsc()
        print "begin solve linear system"
        # https://docs.scipy.org/doc/scipy-0.18.1/reference/sparse.linalg.html
        # from scipy.sparse.spmatrix import toarray
        import time
        start = time.clock()

        def pp(xx):
            x = spsolve(pSMGM, xx)
            x[self.bindex] = 0
            return self.SMGM.dot(x)
        A = LinearOperator((self.Dof, self.Dof), pp)
        self.solution, exitCode = gmres(A, self.RHS, tol=1e-11)
        self.solution = spsolve(pSMGM, self.solution)
        self.solution[self.bindex] = self.bvalue

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
            elep = self.knownfunc.exactsolutionp(elenodecoord)[:3]
            index = self.getGloabIndex(ic)
            UpVector[index] = np.hstack((eleu[0], eleu[1], elep))
        return UpVector



    def solve1(self):
        print "begin computeRHS"
        self.computeRHS()
        print "begin computeLocalMatrices"
        self.computeLocalMatrices()
        print "begin getBoundaryInformation"
        self.getBoundaryInformation()
        print "begin solve linear system"


        import time

        tmp = np.zeros(self.Dof)
        tmp[self.bindex] = self.bvalue
        self.RHS -= self.globalMatrixProdVector(tmp)
        self.RHS[self.bindex] = 0
        start = time.clock()

        self.pA = LinearOperator((self.Dof, self.Dof), self.preconditionfree)
        def pp(xx):
            x,t = bicgstab(self.pA, xx, tol=1.0e-8)
            x[self.bindex] = 0
            return self.globalMatrixProdVector(x)
        A = LinearOperator((self.Dof, self.Dof), pp)
        self.solution, exitCode = gmres(A, self.RHS, tol=1e-8)
        self.solution, exitCode = bicgstab(self.pA, self.solution, tol=1e-8)

        self.solution[self.bindex] = self.bvalue
        print "exitCode = ", exitCode
        end = time.clock()
        print "Solve linear system time = ", end-start
        return

    #
    # def interpL2errorU(self):
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


    def interpL2errorU(self):
        ans = 0.0
        du = 6
        upvector = self.getUpVector()
        phi = self.interp.phi(self.interp.qp, 2)
        t = np.array(range(du))
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            index = self.getGloabIndex(ic)[:du*2]
            eleuh = upvector[index]
            eleu = self.knownfunc.exactsolution(x)
            tmp0 = eleu[0] - np.dot(eleuh[t], phi)
            tmp1 = eleu[1] - np.dot(eleuh[t+du], phi)
            ans += (tmp0*tmp0 + tmp1*tmp1).sum()*ja
        return np.sqrt(ans)



    def L2errorU(self):
        ans = 0.0
        du = 6
        phi = self.interp.phi(self.interp.qp, 2)
        t = np.array(range(du))
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            index = self.getGloabIndex(ic)[:du*2]
            eleuh = self.solution[index]
            eleu = self.knownfunc.exactsolution(x)
            tmp0 = eleu[0] - np.dot(eleuh[t], phi)
            tmp1 = eleu[1] - np.dot(eleuh[t+du], phi)
            ans += (tmp0*tmp0 + tmp1*tmp1).sum()*ja
        return np.sqrt(ans)


    # def interpL2errorp(self):
    #     ans = 0.0
    #     phi = self.interp.phi(self.interp.qp, 1)
    #     for ic in range(self.grid.Nelement):
    #         elepoints = self.grid.points[self.grid.elements[ic]]
    #         mp = Map2DT(elepoints)
    #         ja = mp.jacobi()
    #         x = mp.mapping(self.interp.qp)
    #         elenodecoord = mp.mapping(self.getTrailCoord())[:,:3]
    #         eleui = self.knownfunc.exactsolutionp(elenodecoord)
    #         eleu = self.knownfunc.exactsolutionp(x)
    #         tmp = eleu - np.dot(eleui, phi)
    #         ans += (tmp*tmp).sum()*ja
    #     return np.sqrt(ans)


    def interpL2errorp(self):
        ans = 0.0
        phi = self.interp.phi(self.interp.qp, 1)
        bsdu = 12
        upvector = self.getUpVector()
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            index = self.getGloabIndex(ic)[bsdu:]
            eleuh = upvector[index]
            eleu = self.knownfunc.exactsolutionp(x)
            tmp = eleu - np.dot(eleuh, phi)
            ans += (tmp*tmp).sum()*ja
        return np.sqrt(ans)



    def L2errorp(self):
        ans = 0.0
        phi = self.interp.phi(self.interp.qp, 1)
        bsdu = 12
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2DT(elepoints)
            ja = mp.jacobi()
            x = mp.mapping(self.interp.qp)
            index = self.getGloabIndex(ic)[bsdu:]
            eleuh = self.solution[index]
            eleu = self.knownfunc.exactsolutionp(x)
            tmp = eleu - np.dot(eleuh, phi)
            ans += (tmp*tmp).sum()*ja
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