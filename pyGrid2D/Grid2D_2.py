#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: pyGrid2D
@time: 2017-03-24 22:34
"""
import numpy as np
import os
import copy
import matplotlib.pyplot as plt
from Function.mapping import Map2D

class Grid2D(object):
    def __init__(self):
        # self.points = []  #点坐标
        # self.elements = []  #单元信息
        # self.bounds = []   #边界
        # self.Mbound = []   #边界分段信息，它是个矩阵
        self.getNeibEle_indexmark = 0
        self.getNumEdgemark = 0
        self.getEdgeMessagemark = 0
        self.globalIndexmark = 0
        self.freedomToQuadmark = 0
        self.quadToFreedommark = 0
        # self.poly = 0
        # self.Npoint = 0    #点的个数
        # self.Nelement = 0  #单元个数
        # self.NBPatch = 0   #边界段数
        # # self.Nedge = 0
        # # self.Nedgepoint = 0
        # self.datafile = ""
        pass


    def getsubgrid(self, i):
        subgrid = Grid2D()
        subgrid.setpte(self.points[self.elements[i]], [[0,1,2,3]])
        return subgrid

    def getEdgelength(self, elepoints, j):
        v = elepoints[(j+1) % self.poly] - elepoints[j]
        ans = v*v
        return np.sqrt(ans.sum())

    def getOutNorm(self, elepoints, j):
        poly = len(elepoints)
        v = elepoints[(j+1) % self.poly] - elepoints[j]
        return np.array([v[1], -v[0]])*1.0/self.getEdgelength(elepoints, j)


    def setpte(self, points=[], elements=[], bounds=[]):
        if points != []:
            self.points = np.array(points)
        if elements != []:
            self.elements = np.array(elements)
        if bounds != []:
            self.bounds = np.array(bounds)
        return

    # def readGrid(self, inputs):
    #     if(type(inputs[0]) != "str" and type(inputs) != "str"):
    #         if(len(inputs) == 2):
    #             inputs = np.array(inputs).T
    #         self.points = inputs
    #         self.elements = range(len(self.points))
    #         print inputs,0
    #         return
    #     elif(type(inputs) == "str"):
    #         print inputs,1
    #         self.from_meshdat_get_pte(inputs)
    #         return
    #     elif(type(inputs) != "str" and len(inputs)==3):
    #         print inputs,2
    #         p,t,e = input
    #         self.from_matlab_get_pte(p,t,e)
    #         return
    #     else:
    #         print("Grid2D::readGrid()>>> error!")
    #     return

    def from_meshdat_get_pte(self, datafile):
        self.datafile = datafile
        with open(datafile) as f:
            lines = f.readlines()
            self.Npoint, self.Nelement, self.NBPatch = np.loadtxt(lines[3: 4], int)
            self.Mbound = np.loadtxt(lines[5: 5+self.NBPatch], int)
            self.points = np.loadtxt(lines[6+self.NBPatch: (6+self.NBPatch+self.Npoint)], float)
            self.elements = np.loadtxt(lines[7+self.NBPatch+self.Npoint: (7+self.NBPatch+self.Npoint+self.Nelement)], int)-1
            self.bounds = np.loadtxt(lines[8+self.NBPatch+self.Npoint+self.Nelement: ], int)-1
        if(self.Nelement == 1):
            self.elements = np.array([self.elements])
        self.poly = self.elements.shape[1]
        return

    def outputCppGridDatafile(self, outputfilename):
        # if os.path.exists(outputfilename):
        #     os.remove(outputfilename)
        newlines = "\r\n"
        import platform
        if platform.system() == "Windows":
            newlines = "\n"
        def savefile(xxxx, fmts):
            np.savetxt("Grid2Dtemp.txt", xxxx, fmt=fmts)
            with open("Grid2Dtemp.txt") as f:
                lines = f.readlines()
                fp.writelines(lines)
            return
        p,t,e = self.points, self.elements, self.bounds
        NPoint, Nele, Nedge = len(self.points), len(self.elements), len(self.bounds)

        fp = open(outputfilename,"w")
        fp.write("# unstructured grid for a domain" + newlines)
        fp.write("#\n")
        fp.write("# no. of nodes cells and boundaries" + newlines)
        fp.write(str(NPoint)+"     "+ str(Nele)+"     "+str(1)+newlines)
        fp.write("# BC\n")
        fp.write("0   "+str(Nedge)+"   "+str(Nedge)+newlines)
        fp.write("# node coordinates" + newlines)
        savefile(p, "%1.11e")
        fp.write("# element connectivity" + newlines)
        savefile(t+1, "%d")
        fp.write("# bnodes" + newlines)
        savefile(e+1, "%d")
        fp.close()
        os.remove("Grid2Dtemp.txt")
        return

    def from_matlab_get_pte(self, pfile,tfile,efile):
        import scipy.io as sio
        datap = sio.loadmat(pfile)
        self.points = np.array(datap['p']).T
        datat = sio.loadmat(tfile)
        tt = datat['t'][0:-1, :]
        tt = np.array(tt) - 1
        self.elements = tt.T
        datae = sio.loadmat(efile)
        eee = np.array(datae['e'][0:2, :]) - 1
        eee0 = map(int, eee[0])
        eee1 = map(int, eee[1])
        self.bounds = np.array([eee0, eee1]).T
        self.poly = self.elements.shape[1]
        return

    #第n个点的相邻的单元
    def nthPointNeibElement(self, n):
        return np.where(self.elements == n)


    def getNeibEle_index(self):   #这个nod矩阵就是所谓的矩阵t
        if self.getNeibEle_indexmark == 1:
            return
        self.getNeibEle_indexmark = 1
        nod = self.elements
        NeibEle = copy.deepcopy(nod)
        NeibEleEdge = copy.deepcopy(nod)
        (m, n) = nod.shape
        outEdge = []
        #先对每一个单元进行循环
        for h in range(m):               #主（host）单元循环
            for i in range(n):
                k = 0
                for g in range(m):       #客体（gues）匹配单元循环
                    if g != h:           #主客单元不能相同
                        for j in range(n):
                            a = (j+1) % n
                            if nod[h][i] == nod[g][a] and nod[h][(i+1)%n] == nod[g][j]:
                                NeibEle[h][i] = g
                                NeibEleEdge[h][i] = j
                                k = 1
                                break
                    if k == 1:
                        break
                if k == 0:
                    NeibEle[h][i] = h
                    NeibEleEdge[h][i] = i
                    outEdge += [[h,i]]
        self.NeibEle = np.array(NeibEle)
        self.NeibEleEdge = np.array(NeibEleEdge)
        self.outEdge = np.array(outEdge)
        return

    #要找第i个单元的第j条边的全局编号，果断找NumEdge[i][j]
    def getNumEdge(self):
        if self.getNumEdgemark == 1:
            return
        self.getNumEdgemark = 1
        if self.getNeibEle_indexmark == 0:
            self.getNeibEle_index()
        NeibEle, NeibEleEdge = self.NeibEle, self.NeibEleEdge
        (m, n) = NeibEle.shape
        NumEdge = copy.deepcopy(NeibEle)
        k = -1
        for h in range(m):
            for i in range(n):
                if NeibEle[h][i] >= h:
                    k += 1
                    NumEdge[h][i] = k
                else:
                    I = NeibEle[h][i]
                    J = NeibEleEdge[h][i]
                    NumEdge[h][i] = NumEdge[I][J]
        self.NumEdge = np.array(NumEdge)
        self.Nedge = k+1
        return

    #得到边的相邻两个单元以及边所在的局部标号，分别存放在两个矩阵中
    def getEdgeMessage(self):
        if self.getEdgeMessagemark == 1:
            return
        self.getEdgeMessagemark = 1
        if self.getNumEdgemark == 0:
            self.getNumEdge()
        NumEdge = self.NumEdge
        k = self.Nedge
        EdgeMessage1 = [[]]*k
        EdgeMessage2 = [[]]*k
        (m, n) = NumEdge.shape
        for h in range(m):
            for i in range(n):
                I = NumEdge[h][i]
                if len(EdgeMessage1[I]) == 0:
                    EdgeMessage1[I] = [h,i]
                    EdgeMessage2[I] = [h,i]
                else:
                    EdgeMessage2[I] = [h,i]
        self.EdgeMessage1 = np.array(EdgeMessage1)
        self.EdgeMessage2 = np.array(EdgeMessage2)
        return


    def getElementTraceGlobalIndex(self, deg):
        self.tgindex = []
        de = deg + 1
        for i, ele in enumerate(self.elements):
            ti = []
            for j in range(4):
                t = self.NumEdge[i][j]*de
                if self.NeibEle[i][j] < i:
                    ti += range(t+deg, t-1, -1)
                else:
                    ti += range(t, t+de)
                    pass
            self.tgindex += [ti]
        self.tgindex = np.array(self.tgindex)
        return

    def globalIndex(self, deg):
        if self.globalIndexmark == 1:
            return
        self.globalIndexmark = 1
        if self.getEdgeMessagemark == 0:
            self.getEdgeMessage()
        self.gindex = []
        # 顺序为顶点，边界， 内部
        instart = self.Npoint + self.Nedge*(deg-1)
        innum = (deg-1)*(deg-1)
        self.gdof = instart + innum*self.Nelement
        for i, ele in enumerate(self.elements):
            ti = []
            for j in range(4):
                t = self.Npoint + self.NumEdge[i][j]*(deg-1)
                if self.NeibEle[i][j] < i:
                    ti += range(t+deg-2, t-1, -1)
                else:
                    ti += range(t, t+deg-1)
            tmp = instart + i*innum
            self.gindex += [ele.tolist() + ti + range(tmp, tmp+innum)]
        self.gindex = np.array(self.gindex)
        return

    # 只是针对矩形
    def freedomToQuad(self, deg):
        if self.freedomToQuadmark == 1:
            return
        self.freedomToQuadmark = 1
        pd = deg + 1
        ed = deg - 1
        ct = deg * 4
        index = [0]*(pd*pd)
        index[1] = pd-1
        index[2] = pd*pd-1
        index[3] = pd*(pd-1)
        for i in range(1, deg):
            index[3     +i] = index[0]+i
            index[3  +ed+i] = index[1]+pd*i
            index[3+2*ed+i] = index[2]-i
            index[3+3*ed+i] = index[0]+pd*(ed-i+1)
        for i in range(1, deg):
            for j in range(1, deg):
                index[ct] = i*pd+j
                ct += 1
        self.freetoquad = np.array(index)
        return self.freetoquad

    def quadToFreedom(self, deg):
        if self.quadToFreedommark == 1:
            return
        if self.freedomToQuadmark == 0:
            self.freedomToQuad(deg)
        index = [0]*((deg + 1)*(deg + 1))
        for i, vi in enumerate(self.freetoquad):
            index[vi] = i
        self.quadtofree = np.array(index)
        return

    def plotmesh2d(self, axes, pointsize=1,ftz=20,plotpointsnum="y", plotelementsnum="y", plotedgesnum="n"):
        points, touch = self.points, self.elements
        newtouch  = np.hstack((touch, touch[:,0:1]))

        for i in newtouch:
            x,y = points[i,:].T
            axes.plot(x,y, color='black', linestyle='solid', markerfacecolor='black', linewidth=1)
        if plotpointsnum == "y":
            for n,i in enumerate(points):
                x,y = i[:2]
                axes.plot(x, y, color='black', marker='o',markerfacecolor='black', markersize=pointsize)
                axes.text(x, y, str(n), color='blue', fontsize = ftz, verticalalignment='top', horizontalalignment='left')
        if plotelementsnum=="y":
            for n,i in enumerate(touch):
                x,y = points[i,:].T
                x,y = sum(x)*1.0/len(x),  sum(y)*1.0/len(y)
                axes.text(x, y, str(n), color='red', fontsize = ftz, verticalalignment='center', horizontalalignment='center')
        if plotedgesnum=="y":
            for n,i in enumerate(touch):
                x, y = points[i,:].T
                for j in range(len(i)):
                    J = (j+1)%(len(i))
                    xx, yy = (x[j]+x[J])*0.5, (y[j]+y[J])*0.5
                    axes.text(xx, yy, str(self.NumEdge[n][j]), color='green', fontsize = ftz, verticalalignment='center', horizontalalignment='center')


        k = 1; h = 0.05+pointsize*0.003
        x,y = points.T
        xmin = min(x); xmax = max(x); ymin = min(y); ymax = max(y)
        axes.set_xlim(k*xmin-h, k*xmax+h)
        axes.set_ylim(k*ymin-h, k*ymax+h)
        return

    def plotNodeDistribution(self, axes, xHat, plotnodenum="n", pointsize=6, ftz=12, linewidth=5):
        points, touch = self.points, self.elements
        newtouch  = np.hstack((touch, touch[:, 0:1]))

        for i in newtouch:
            x,y = points[i,:].T
            axes.plot(x,y, color='blue', linestyle='solid', markerfacecolor='blue', linewidth=linewidth)

        # for i, bd in enumerate(self.bounds):
        #     x,y = self.points[bd].T
        #     axes.plot(x,y, color='blue', linestyle='solid', markerfacecolor='black', linewidth=4)

        pd = len(xHat)

        xhat2d = np.array(np.meshgrid(xHat, xHat))
        for n, ele in enumerate(touch):
            map2d = Map2D(self.points[ele])
            xx = map2d.mapping(xhat2d)
            for i in range(pd):
                x,y = xx[0][i], xx[1][i]
                xt,yt = xx[0].T[i], xx[1].T[i]
                axes.plot(x, y, '--o--', color='black', markerfacecolor='red', markersize=pointsize, linestyle='dashed')
                axes.plot(xt, yt, '--o--', color='black', markerfacecolor='red', markersize=pointsize, linestyle='dashed')

        if plotnodenum == "y":
            self.globalIndex(pd-1)
            self.quadToFreedom(pd-1)
            xhat2d = np.array(np.meshgrid(xHat, xHat))
            for n, ele in enumerate(touch):
                map2d = Map2D(self.points[ele])
                xx = map2d.mapping(xhat2d)
                for i in range(pd):
                    for j in range(pd):
                        x, y = xx[0][i][j], xx[1][i][j]
                        ij = i*pd + j
                        t = self.gindex[n][self.quadtofree[ij]]
                        axes.text(x, y, str(t), color='g', fontsize=ftz, verticalalignment='top', horizontalalignment='left')

        k = 1; h = 0.05+pointsize*0.003
        x,y = points.T
        xmin = min(x); xmax = max(x); ymin = min(y); ymax = max(y)
        axes.set_xlim(k*xmin-h, k*xmax+h)
        axes.set_ylim(k*ymin-h, k*ymax+h)
        return


def plotblank(axes):
    axes.set_xticks([])
    axes.set_yticks([])
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['bottom'].set_color('none')
    axes.spines['left'].set_color('none')
    return
if __name__ == '__main__':
    Directoryname = ".//testmesh//"
    # datafile = "meshHDuffy.dat"
    # datafile = "meshH.dat"
    datafile = "sixbianxing.dat"
    datafile = "4times4_rect.dat"
    outputdatafile = "new"+datafile
    grid = Grid2D()
    grid.from_meshdat_get_pte(Directoryname+datafile)
    p, t, e = grid.points, grid.elements, grid.bounds
    grid.getEdgeMessage()

    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    grid.plotmesh2d(axes, pointsize=6,plotpointsnum="y", plotelementsnum="y")
    plotblank(axes)
    plt.savefig(Directoryname+datafile+".pdf",dip=120,bbox_inches='tight')
    plt.show()






    # print np.where(len(t&set(t[0]))==2)[0]
    # goodvalues = t[0][-2:]
    # print t[0]
    # print goodvalues
    # it = np.in1d(t.ravel(), goodvalues).reshape(t.shape)
    # print np.where(it)
    #help(np.where)
    # m,n =  np.shape(t)
    # ele =  t.reshape(1,m*n)[0]

    # grid.outputCppGridDatafile(Directoryname+outputdatafile)
    # Directoryname = ".//testmatlabpet//"
    # ptefiles = ["p.mat", "t.mat", "e.mat"]
    # grid1 = Grid2D()
    # grid1.from_matlab_get_pte(Directoryname+ptefiles[0], Directoryname+ptefiles[1], Directoryname+ptefiles[2])
    # grid1.outputCppGridDatafile(Directoryname+"matlabmesh.dat")




