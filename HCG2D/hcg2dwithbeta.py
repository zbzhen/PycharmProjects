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
from Function.functionQuad import Quadrature, FuncQuad
from Function.interp import Interp
class SHCG2D(object):
    def __init__(self, knownfunc, grid, interp, rhquad):
        self.knownfunc = knownfunc
        self.grid = grid
        self.interp = interp
        self.quad = rhquad    # right hand quadrature
        self.MLM = []
        self.RHS = []
        self.SMGM = []
        self.solution = []
        self.MtMhCtCh = interp.getMtMhCtCh()

        gsquad = Quadrature(self.interp.pp + 5)
        gsquad.getGuassPointsWeights()
        gshh = Interp(self.interp.ip, gsquad)
        self.gsmh = gshh.mhat(-1, -1)
        self.gsmt = gshh.mtilde(-1, -1)
        pass

    def computeLocalMatrices(self, ic):
        elepoints = self.grid.points[self.grid.elements[ic]]
        mp = Map2D(elepoints)
        mathbbM = mp.D1*self.mhmt + mp.D2*self.mtmh + mp.D3*self.mtmt
        mathbbCx = mp.alpha_1[1]*self.mtch + mp.alpha_3[1]*self.mtct - \
                   mp.alpha_1[1]*self.chmt - mp.alpha_2[1]*self.ctmt
        mathbbCy = - mp.alpha_1[0]*self.mtch - mp.alpha_3[0]*self.mtct + \
                     mp.alpha_1[0]*self.chmt + mp.alpha_2[0]*self.ctmt
        mm = mathbbM.copy()
        if abs(mp.D1 + mp.D2 + mp.D3) < 1.0e-10:
            mathbbM[-1][-1] = mp.D1*self.gsmh*self.gsmt + \
                              mp.D2*self.gsmt*self.gsmh + mp.D3*self.gsmt*self.gsmt

        x = mp.mapping(self.ip2d)
        betax = self.knownfunc.beta(x)
        Mx = np.linalg.solve(mathbbM, (mathbbCx*betax).T)
        My = np.linalg.solve(mathbbM, (mathbbCy*betax).T)
        self.MLM = np.dot(mathbbCx, Mx) + np.dot(mathbbCy, My) + mm
        # self.MLM = np.where(abs(self.MLM) > 1.0e-13, self.MLM, 0)    # filter too small number
        return self.MLM

    def computeRHS(self):
        funcquad = FuncQuad(self.knownfunc.rhf, self.quad, self.grid, self.interp.ip)
        funcquad.nx = 1
        funcquad.ny = 1
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

    def imposeBoundaryCondition(self):
        poly = 4
        deg = self.interp.deg

        # boundary vertex
        bv = set(self.grid.bounds.T[0]) | set(self.grid.bounds.T[1])
        bv = list(bv)
        self.RHS[bv] = self.knownfunc.bc((self.grid.points[bv]).T)
        self.SMGM[bv] = 0.0
        self.SMGM[bv, bv] = 1.0
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
                self.RHS[start: start+deg-1] = value
                self.SMGM[start: start+deg-1] = 0.0
                self.SMGM[range(start, start+deg-1), range(start, start+deg-1)] = 1.0
        return

    def assemble(self):
        du = self.interp.pp*self.interp.pp
        self.ip2d = np.array(np.meshgrid(self.interp.ip, self.interp.ip)).reshape((2, du))

        mt, mh, ct, ch = self.MtMhCtCh
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
        from scipy.sparse import lil_matrix
        self.SMGM = lil_matrix((self.grid.gdof, self.grid.gdof))

        for ic in range(self.grid.Nelement):
            self.computeLocalMatrices(ic)
            index = (self.grid.gindex[ic])[self.grid.quadtofree]
            for i in range(du):
                for j in range(du):
                    self.SMGM[index[i], index[j]] += self.MLM[i][j]
        return

    def solve(self):
        print "begin computeRHS"
        self.computeRHS()
        print "begin assemble"
        self.assemble()
        print "begin imposeBoundaryCondition"
        self.imposeBoundaryCondition()
        print "begin solve linear system"
        from scipy.sparse.linalg import spsolve
        import time
        start = time.clock()
        print "np.linalg.cond(self.SMGM.toarray())"
        print np.linalg.cond(self.SMGM.toarray())
        self.solution = spsolve(self.SMGM.tocsc(), self.RHS)
        # self.solution = spsolve(self.SMGM, self.RHS)
        end = time.clock()
        print "Solve linear system time = ", end-start
        return

