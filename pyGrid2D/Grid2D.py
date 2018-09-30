#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: Grid2D
@time: 2018/2/23  9:58
"""
import sys
sys.path.append(r'..')
import numpy as np
import matplotlib.pyplot as plt
from Function.mapping import Map2D


class Grid2D(object):
    def __init__(self):
        self.points = []  #点坐标
        self.elements = []  #单元信息
        self.bounds = []   #边界
        self.Mbound = []   #边界分段信息，它是个矩阵
        self.poly = 0
        self.Npoint = 0    #点的个数
        self.Nelement = 0  #单元个数
        self.NBPatch = 0   #边界段数

        self.tgindex = []
        # self.Nedge = 0
        # # self.Nedgepoint = 0
        # self.datafile = ""
        pass


    def getsubgrid(self, i):
        subgrid = Grid2D()
        if self.poly == 4:
            subgrid.setpte(self.points[self.elements[i]], [[0,1,2,3]])
        elif self.poly == 3:
            subgrid.setpte(self.points[self.elements[i]], [[0,1,2]])
        return subgrid

    def getEdgelength(self, elepoints, j):
        v = elepoints[(j+1) % self.poly] - elepoints[j]
        ans = v*v
        return np.sqrt(ans.sum())

    def getOutNorm(self, elepoints, j):
        v = elepoints[(j+1) % self.poly] - elepoints[j]
        return np.array([v[1], -v[0]])*1.0/self.getEdgelength(elepoints, j)


    def setpte(self, points=[], elements=[], bounds=[]):
        if points != []:
            self.points = np.array(points)
        if elements != []:
            self.elements = np.array(elements)
        if bounds != []:
            self.bounds = np.array(bounds)
        self.Npoint, self.Nelement = len(self.points), len(self.elements)
        return


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
        fp.write("#"+newlines)
        fp.write("# no. of nodes cells and boundaries" + newlines)
        fp.write(str(NPoint)+"     "+ str(Nele)+"     "+str(1)+newlines)
        fp.write("# BC"+newlines)
        fp.write("0   "+str(Nedge)+"   "+str(Nedge)+newlines)
        fp.write("# node coordinates" + newlines)
        savefile(p, "%1.11e")
        fp.write("# element connectivity" + newlines)
        savefile(t+1, "%d")
        fp.write("# bnodes" + newlines)
        savefile(e+1, "%d")
        fp.close()
        import os
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


    def readGrid(self):   #这个nod矩阵就是所谓的矩阵t
        self.Nedge = self.Npoint + self.Nelement - 1
        NeibEle = self.elements.copy()
        NeibEleEdge = self.elements.copy()
        (m, n) = self.elements.shape
        outEdge = []
        pointNeibEle = [[]]*self.Npoint
        eleGetEdgeIndex = self.elements.copy()
        EdgeMessage1 = [[]]*self.Nedge
        EdgeMessage2 = [[]]*self.Nedge
        # print pointNeibEle
        # print self.elements
        for ic, ele in enumerate(self.elements):
            for ie in ele:
                pointNeibEle[ie] = pointNeibEle[ie] + [ic]
        k = -1
        for ic, ele in enumerate(self.elements):
            for ie in range(self.poly):
                tmpL = set(pointNeibEle[ele[ie]])
                tmpR = set(pointNeibEle[ele[(ie+1) % self.poly]])
                edgeTwoele = list(tmpL & tmpR)
                if edgeTwoele[-1] == ic:
                    nele = edgeTwoele[0]
                else:
                    nele = edgeTwoele[-1]
                localindex = np.argwhere(self.elements[nele] == ele[ie])[0][0]
                localindex = (localindex + self.poly - 1) % self.poly
                NeibEle[ic][ie] = nele
                NeibEleEdge[ic][ie] = localindex

                # for out boundary
                if len(edgeTwoele) == 1:
                    outEdge += [[ic, ie]]
                    NeibEle[ic][ie] = ic
                    NeibEleEdge[ic][ie] = ie

                # set edge index
                if nele >= ic:
                    k += 1
                    eleGetEdgeIndex[ic][ie] = k
                else:
                    I = NeibEle[ic][ie]
                    J = NeibEleEdge[ic][ie]
                    eleGetEdgeIndex[ic][ie] = eleGetEdgeIndex[I][J]

                # get edge message
                I = eleGetEdgeIndex[ic][ie]
                if len(EdgeMessage1[I]) == 0:
                    EdgeMessage1[I] = [ic, ie]
                    EdgeMessage2[I] = [ic, ie]
                else:
                    EdgeMessage2[I] = [ic, ie]
        self.pointNeibEle = np.array(pointNeibEle)
        self.NeibEle = np.array(NeibEle)
        self.NeibEleEdge = np.array(NeibEleEdge)
        self.outEdge = np.array(outEdge)
        self.NumEdge = np.array(eleGetEdgeIndex)
        self.EdgeMessage1 = np.array(EdgeMessage1)
        self.EdgeMessage2 = np.array(EdgeMessage2)
        return

    def vertexTrembled(self, ratio=0.6, changeoutVertex=False):
        elepoints = self.points[self.elements[0]]
        self.poly = len(elepoints)
        eleedgeh = [self.getEdgelength(elepoints, j) for j in range(self.poly)]
        h = 0.35*min(eleedgeh)*ratio  # 0.35 equal approximately to 0.5 * \frac{\sqrt{2}}{2}
        rand = np.random.random(self.points.shape)*(2*h) - h

        if changeoutVertex == False:
            rand[self.bounds.T[0]] = 0
            rand[self.bounds.T[1]] = 0
            self.points += rand
        return




    # 只是针对矩形
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

    # 只是针对矩形
    def globalIndex(self, deg):
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

    # 只是针对矩形
    def quadToFreedom(self, deg):
        self.freedomToQuad(deg)
        index = [0]*((deg + 1)*(deg + 1))
        for i, vi in enumerate(self.freetoquad):
            index[vi] = i
        self.quadtofree = np.array(index)
        return

    def plotmesh2d(self, axes, pointsize=1,ftz=20,plotpointsnum=False, plotelementsnum=False, plotedgesnum=False):
        points, touch = self.points, self.elements
        newtouch  = np.hstack((touch, touch[:,0:1]))

        for i in newtouch:
            x, y = points[i, :].T
            axes.plot(x, y, color='black', linestyle='solid', markerfacecolor='black', linewidth=1)
        if plotpointsnum == True:
            for n, i in enumerate(points):
                x, y = i[:2]
                axes.plot(x, y, color='black', marker='o', markerfacecolor='black', markersize=pointsize)
                axes.text(x, y, str(n), color='blue', fontsize=ftz, verticalalignment='top', horizontalalignment='left')
        if plotelementsnum == True:
            for n, i in enumerate(touch):
                x, y = points[i, :].T
                x, y = sum(x)*1.0/len(x),  sum(y)*1.0/len(y)
                # axes.text(x, y, str(n), color='red', fontsize=ftz, verticalalignment='center', horizontalalignment='center')
                axes.text(x, y, str(n), color='blue', fontsize=ftz+15, verticalalignment='center', horizontalalignment='center')
        if plotedgesnum == True:
            for n, i in enumerate(touch):
                x, y = points[i, :].T
                for j in range(len(i)):
                    J = (j+1) % (len(i))
                    xx, yy = (x[j]+x[J])*0.5, (y[j]+y[J])*0.5
                    axes.text(xx, yy, str(self.NumEdge[n][j]), color='green', fontsize=ftz, verticalalignment='center', horizontalalignment='center')


        k = 1
        h = 0.05+pointsize*0.003
        x,y = points.T
        xmin = min(x); xmax = max(x); ymin = min(y); ymax = max(y)
        axes.set_xlim(k*xmin-h, k*xmax+h)
        axes.set_ylim(k*ymin-h, k*ymax+h)
        return

    def plotNodeDistribution(self, axes, xHat, plotnodenum=False, pointsize=6, ftz=12, linewidth=5):
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

        if plotnodenum == True:
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
    grid.readGrid()
    grid.vertexTrembled(0.8)

    fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
    axes = plt.subplot(111)
    grid.plotNodeDistribution(axes,  [-1,-0.333,0.333,1],pointsize=6,plotnodenum=True)
    grid.plotmesh2d(axes, pointsize=6,plotpointsnum=True, plotelementsnum=True, plotedgesnum=True)

    plotblank(axes)
    plt.savefig(Directoryname+datafile+".pdf",dip=120,bbox_inches='tight')
    plt.show()
    grid.outputCppGridDatafile("4times4_rectTrembled.dat")





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



