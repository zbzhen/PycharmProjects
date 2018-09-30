#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: hcg2d
@time: 2018/1/30  12:31
"""
import sys
sys.path.append(r'..')
import numpy as np
from Function.mapping import mapping1D, Map2D
from Function.functionQuad import FuncQuad
class SHCG2D(object):
    def __init__(self, knownfunc, grid, interp, rhquad):
        self.knownfunc = knownfunc
        self.grid = grid
        self.interp = interp
        self.quad = rhquad    # right hand quadrature
        self.MLM = []
        self.RHS = []
        self.bindex = []
        self.bvalue = []
        self.solution = []
        mt, mh, ct, ch = interp.getMtMhCtCh()
        self.mhmt = np.tensordot(mh, mt, 0)
        self.mtmh = np.tensordot(mt, mh, 0)
        self.mtmt = np.tensordot(mt, mt, 0)
        self.chmt = np.tensordot(ch, mt, 0)
        self.mtch = np.tensordot(mt, ch, 0)
        self.mtct = np.tensordot(mt, ct, 0)
        self.ctmt = np.tensordot(ct, mt, 0)
        self.mhmt = np.concatenate(np.concatenate(self.mhmt, 1), 1)
        self.mtmh = np.concatenate(np.concatenate(self.mtmh, 1), 1)
        self.mtmt = np.concatenate(np.concatenate(self.mtmt, 1), 1)
        self.chmt = np.concatenate(np.concatenate(self.chmt, 1), 1)
        self.mtch = np.concatenate(np.concatenate(self.mtch, 1), 1)
        self.mtct = np.concatenate(np.concatenate(self.mtct, 1), 1)
        self.ctmt = np.concatenate(np.concatenate(self.ctmt, 1), 1)
        pass

    def getBoundaryInformation(self):
        poly = 4
        deg = self.interp.deg
        # boundary vertex
        bindex = set(self.grid.bounds.T[0]) | set(self.grid.bounds.T[1])
        bindex = list(bindex)
        bvalue = self.knownfunc.bc((self.grid.points[bindex]).T)
        # boundary inner node
        if deg > 1:
            for edge in self.grid.outEdge:
                ic, ie = edge   # element and local edge index
                iL, iR = self.grid.elements[ic][ie], self.grid.elements[ic][(ie+1) % poly]
                a, b = self.grid.points[[iL, iR]]         # edge two vertexes
                x = map(mapping1D(a, b), self.interp.ip[1: deg])   # remove two vertexes
                value = self.knownfunc.bc(np.array(x).T)
                edgeindex = self.grid.NumEdge[ic][ie]
                start = self.grid.Npoint + edgeindex*(deg - 1)
                bindex += range(start, start+deg-1)
                bvalue = np.hstack((bvalue, value))
        self.bindex = bindex
        self.bvalue = bvalue
        return

    def computeRHS(self):
        funcquad = FuncQuad(self.knownfunc.rhf, self.quad, self.grid, self.interp.ip)
        du = self.interp.pp*self.interp.pp
        de = self.interp.pp
        self.RHS = np.zeros(self.grid.gdof)
        for ic in range(self.grid.Nelement):
            funcquad.grid = self.grid.getsubgrid(ic)
            index = (self.grid.gindex[ic])[self.grid.quadtofree]
            for i in range(du):
                ix, iy = i / de, i % de
                self.RHS[index[i]] += funcquad.fphiQuad(ix, iy)
        return

    def computeLocalMatrices(self):
        du = self.interp.pp*self.interp.pp
        self.MLM = np.empty((self.grid.Nelement, du, du), float)
        for ic in range(self.grid.Nelement):
            elepoints = self.grid.points[self.grid.elements[ic]]
            mp = Map2D(elepoints)
            mathbbM = mp.D1*self.mhmt + mp.D2*self.mtmh + mp.D3*self.mtmt
            mathbbCx = mp.alpha_1[1]*self.mtch + mp.alpha_3[1]*self.mtct - \
                       mp.alpha_1[1]*self.chmt - mp.alpha_2[1]*self.ctmt
            mathbbCy = - mp.alpha_1[0]*self.mtch - mp.alpha_3[0]*self.mtct + \
                         mp.alpha_1[0]*self.chmt + mp.alpha_2[0]*self.ctmt
            if abs(mathbbM[-1][-1]) < 1.0e-13:
                mathbbM[-1][-1] = 1.0
            Mx = np.linalg.solve(mathbbM, mathbbCx.T)
            My = np.linalg.solve(mathbbM, mathbbCy.T)
            MLM = np.dot(mathbbCx, Mx) + np.dot(mathbbCy, My)
            self.MLM[ic] = MLM
        return

    def globalMatrixProdVector(self, gx):
        gAx = np.zeros(self.grid.gdof)
        for ic in range(self.grid.Nelement):
            index = (self.grid.gindex[ic])[self.grid.quadtofree]
            gAx[index] += np.dot(self.MLM[ic], gx[index])
        gAx[self.bindex] = 0
        return gAx




    def solve(self):
        print "begin getBoundaryInformation"
        self.getBoundaryInformation()
        print "begin computeRHS"
        self.computeRHS()
        import time
        print "begin computeLocalMatrices"
        self.computeLocalMatrices()
        print "begin solve linear system"
        from scipy.sparse.linalg import spsolve, cg, gmres, LinearOperator
        start = time.clock()
        # # gmres
        # A = LinearOperator((self.grid.gdof, self.grid.gdof), self.globalMatrixProdVector)
        # self.solution, exitCode = gmres(A, self.RHS, tol=1e-12, maxiter=20000)
        # self.solution[self.bindex] = self.bvalue
        # print "exitCode = ", exitCode

        # cg
        A = LinearOperator((self.grid.gdof, self.grid.gdof), self.globalMatrixProdVector)
        tmp = np.zeros(self.grid.gdof)
        tmp[self.bindex] = self.bvalue
        self.RHS -= self.globalMatrixProdVector(tmp)
        self.RHS[self.bindex] = 0
        self.solution, exitCode = cg(A, self.RHS, tol=1e-12, maxiter=50000)
        self.solution[self.bindex] = self.bvalue
        print "exitCode = ", exitCode

        end = time.clock()
        print "Solve linear system time = ", end-start
        return

