#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: hdg2d
@time: 2018/1/28  15:46
HDG method solve poisson problem
- \lapalace u = f
"""
import sys
sys.path.append(r'..')
import numpy as np
from Function.mapping import mapping1D, Map2D
from Function.functionQuad import FuncQuad

class SHDG2D:
    def __init__(self, knownfunc, grid, interp, quad):
        self.knownfunc = knownfunc
        self.grid = grid
        self.interp = interp
        self.quad = quad
        self.MLM = []
        self.RHS = []
        self.taceRHS = []
        self.SMGM = []
        self.MtMhCtCh = interp.getMtMhCtCh()
        self.HDG_tau = 1.0
        pass
    def computeLocalMatrices(self, ic):
        elepoints = self.grid.points[self.grid.elements[ic]]
        mp = Map2D(elepoints)
        du = self.interp.pp*self.interp.pp
        dq = 2*du
        de = self.interp.pp
        deg = self.interp.deg
        poly = 4
        MLM = np.zeros((du+dq+poly*de, du+dq+poly*de))
        mathbbD = np.zeros((du, du))
        mathbbT = np.zeros((poly*de, du))
        mathbbTx = np.zeros((poly*de, du))
        mathbbTy = np.zeros((poly*de, du))
        mathbbN = np.zeros((poly*de, poly*de))
        mathbbM = mp.D1*self.mtmh + mp.D2*self.mhmt + mp.D3*self.mtmt
        mathbbCx = mp.alpha_1[1]*self.mtch + mp.alpha_3[1]*self.mtct - \
                   mp.alpha_1[1]*self.chmt - mp.alpha_2[1]*self.ctmt
        mathbbCy = - mp.alpha_1[0]*self.mtch - mp.alpha_3[0]*self.mtct + \
                     mp.alpha_1[0]*self.chmt + mp.alpha_2[0]*self.ctmt
        # example
        # deg = 2, de = 3
        # 6, 7, 8
        # 3, 4, 5
        # 0, 1, 2
        norm = mp.edgeOutNorm()
        edgeja = mp.edgeLength()*0.5
        index = np.array(range(de), dtype=int)
        xedni = np.array(range(deg, -1, -1), dtype=int)
        Mt = self.MtMhCtCh[0]
        mathbbD[np.ix_(index, index)] += edgeja[0]*Mt     # Be careful +=
        mathbbD[np.ix_(index*de+deg, index*de+deg)] += edgeja[1]*Mt
        mathbbD[np.ix_(xedni+deg*de, xedni+deg*de)] += edgeja[2]*Mt
        mathbbD[np.ix_(xedni*de, xedni*de)] += edgeja[3]*Mt
        mathbbT[np.ix_(index, index)] = edgeja[0]*Mt
        mathbbT[np.ix_(index+de*1, index*de+deg)] = edgeja[1]*Mt
        mathbbT[np.ix_(index+de*2, xedni+deg*de)] = edgeja[2]*Mt
        mathbbT[np.ix_(index+de*3, xedni*de)] = edgeja[3]*Mt
        mathbbTx[np.ix_(index, index)] = norm[0][0]*edgeja[0]*Mt
        mathbbTx[np.ix_(index+de*1, index*de+deg)] = norm[1][0]*edgeja[1]*Mt
        mathbbTx[np.ix_(index+de*2, xedni+deg*de)] = norm[2][0]*edgeja[2]*Mt
        mathbbTx[np.ix_(index+de*3, xedni*de)] = norm[3][0]*edgeja[3]*Mt
        mathbbTy[np.ix_(index, index)] = norm[0][1]*edgeja[0]*Mt
        mathbbTy[np.ix_(index+de*1, index*de+deg)] = norm[1][1]*edgeja[1]*Mt
        mathbbTy[np.ix_(index+de*2, xedni+deg*de)] = norm[2][1]*edgeja[2]*Mt
        mathbbTy[np.ix_(index+de*3, xedni*de)] = norm[3][1]*edgeja[3]*Mt
        mathbbN[np.ix_(index, index)] = edgeja[0]*Mt
        mathbbN[np.ix_(index+de*1, index+de*1)] = edgeja[1]*Mt
        mathbbN[np.ix_(index+de*2, index+de*2)] = edgeja[2]*Mt
        mathbbN[np.ix_(index+de*3, index+de*3)] = edgeja[3]*Mt
        """
        -----------------------------***  Assembly ****-----------------------------
         --------------------------------------------------------------------------
         du             du              du                   de*poly
         --------------------------------------------------------------------------
        -mathbbM        0              -mathbbCx              mathbbTx.T
         0             -mathbbM        -mathbbCy              mathbbTy.T
        -mathbbCx.T    -mathbbCy.T      mathbbD*HDG_tau      -mathbbT.T*HDG_tau
         mathbbTx       mathbbTy       -mathbbT*HDG_tau       mathbbN*HDG_tau
          _________________________________________________________________________
         -----------------------------***  Assembly ****----------------------------
        """
        MLM[:du, :du] = -mathbbM
        MLM[du:dq, du:dq] = -mathbbM
        MLM[:du, dq:dq+du] = -mathbbCx
        MLM[du:dq, dq:dq+du] = -mathbbCy
        MLM[dq:dq+du, :du] = -mathbbCx.T
        MLM[dq:dq+du, du:dq] = -mathbbCy.T
        MLM[dq:dq+du, dq:dq+du] = mathbbD*self.HDG_tau
        MLM[:du, dq+du:] = mathbbTx.T
        MLM[du:dq, dq+du:] = mathbbTy.T
        MLM[dq:dq+du, dq+du:] = -mathbbT.T*self.HDG_tau
        MLM[dq+du:, :du] = mathbbTx
        MLM[dq+du:, du:dq] = mathbbTy
        MLM[dq+du:, dq:dq+du] = -mathbbT*self.HDG_tau
        MLM[dq+du:, dq+du:] = mathbbN*self.HDG_tau

        return MLM

    def computeRHS(self):
        funcquad = FuncQuad(self.knownfunc.rhf, self.quad, self.grid, self.interp.ip)
        de = self.interp.pp
        du = de*de
        self.RHS = np.zeros((self.grid.Nelement, du))
        for ic in range(self.grid.Nelement):
            funcquad.grid = self.grid.getsubgrid(ic)
            for i in range(du):
                ix, iy = i / de, i % de
                self.RHS[ic][i] = funcquad.fphiQuad(ix, iy)
        return

    def assemble(self):
        poly = 4
        de = self.interp.pp
        du = de*de
        dq = 2*du
        tgdof = self.grid.Nedge * de
        self.taceRHS = np.zeros(tgdof)
        from scipy.sparse import lil_matrix
        self.SMGM = lil_matrix((tgdof, tgdof))
        # self.MLM = np.zeros((self.grid.Nelement, dq+du+poly*de, dq+du+poly*de))

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
        for ic in range(self.grid.Nelement):
            index = self.grid.tgindex[ic]
            # self.MLM[ic] = self.computeLocalMatrices(ic)
            # mathbbA = (self.MLM[ic])[:dq+du, :dq+du]
            # mathbbB = (self.MLM[ic])[:dq+du, dq+du:]
            # mathbbC = (self.MLM[ic])[dq+du:, :dq+du]
            # mathbbK33 = (self.MLM[ic])[dq+du:, dq+du:]
            MLM = self.computeLocalMatrices(ic)
            mathbbA = MLM[:dq+du, :dq+du]
            mathbbB = MLM[:dq+du, dq+du:]
            mathbbC = MLM[dq+du:, :dq+du]
            mathbbK33 = MLM[dq+du:, dq+du:]
            AinvF = np.linalg.solve(mathbbA, np.hstack((np.zeros(dq), self.RHS[ic])))
            right = np.dot(mathbbC, AinvF)
            AinvB = np.linalg.solve(mathbbA, mathbbB)
            left = mathbbK33 - np.dot(mathbbC, AinvB)
            for i in range(de*poly):
                self.taceRHS[index[i]] -= right[i]
                for j in range(de*poly):
                    self.SMGM[index[i], index[j]] += left[i][j]
        return

    def imposeBoundaryCondition(self):
        poly = 4
        de = self.interp.deg + 1
        for edge in self.grid.outEdge:
            ic, ie = edge   # element and local edge index
            iL, iR = self.grid.elements[ic][ie], self.grid.elements[ic][(ie+1) % poly]
            a, b = self.grid.points[[iL, iR]]         # edge two vertexes
            x = map(mapping1D(a, b), self.interp.ip)
            value = self.knownfunc.bc(np.array(x).T)
            edgeindex = self.grid.NumEdge[ic][ie]
            start = edgeindex*de
            self.taceRHS[start: start+de] = value
            self.SMGM[start: start+de] = 0.0
            self.SMGM[range(start, start+de), range(start, start+de)] = 1.0
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
        uhat = spsolve(self.SMGM.tocsc(), self.taceRHS)
        poly = 4
        de = self.interp.pp
        du = de*de
        dq = 2*du
        self.solution = np.zeros((self.grid.Nelement, dq+du))
        for ic in range(self.grid.Nelement):
            MLM = self.computeLocalMatrices(ic)
            LR = uhat[self.grid.tgindex[ic]]
            mathbbA = MLM[:dq+du, :dq+du]
            mathbbB = MLM[:dq+du, dq+du:dq+du+poly*de]
            mathbbF = np.hstack((np.zeros(dq), self.RHS[ic]))
            self.solution[ic] = np.linalg.solve(mathbbA, mathbbF - np.dot(mathbbB, LR))
        return
