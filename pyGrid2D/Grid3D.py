#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: Grid3D
@time: 2017-11-15 10:50
"""

import sys
sys.path.append(r'..')
import numpy as np
import os
import copy
import matplotlib.pyplot as plt


class Grid3D_T(object):
    def __init__(self):
        self.points = []  #点坐标
        self.elements = []  #单元信息
        self.bounds = []   #边界
        self.Mbound = []   #边界分段信息，它是个矩阵

        self.Npoint = 0    #点的个数
        self.Nelement = 0  #单元个数
        self.NBPatch = 1   #边界段数
        pass

    def setpte(self, points=[], elements=[], bounds=[]):
        if points != []:
            self.points = np.array(points)
        if elements != []:
            self.elements = np.array(elements)
        if bounds != []:
            self.bounds = np.array(bounds)
        return

    def from_meshdat_get_pte(self, datafile):
        self.datafile = datafile
        with open(datafile) as f:
            lines = f.readlines()
            self.Npoint, self.Nelement, self.NBPatch = np.loadtxt(lines[3 : 4], int)
            self.Mbound = np.loadtxt(lines[5:5+self.NBPatch], int)
            self.points = np.loadtxt(lines[6+self.NBPatch : (6+self.NBPatch+self.Npoint)], float)
            self.elements = np.loadtxt(lines[7+self.NBPatch+self.Npoint : (7+self.NBPatch+self.Npoint+self.Nelement)], int)-1
            self.bounds = np.loadtxt(lines[8+self.NBPatch+self.Npoint+self.Nelement : ], int)-1
        return


    def outputCppGridDatafile(self, outputfilename):
        # if os.path.exists(outputfilename):
        #     os.remove(outputfilename)
        newlines = "\r\n"
        import platform
        if  platform.system() == "Windows":
            newlines = "\n"
        def savefile(xxxx, objectfile, fmts):
            np.savetxt("Grid3D_Ttemp.txt", xxxx, fmt=fmts)
            with open("Grid3D_Ttemp.txt") as f:
                lines = f.readlines()
                objectfile.writelines(lines)
            return
        fp = open(outputfilename,"w")
        fp.write("# unstructured grid for a domain" + newlines)
        fp.write("#\n")
        fp.write("# no. of nodes cells and boundaries" + newlines)
        fp.write(str(self.Npoint)+"     "+ str(self.Nelement)+"     "+str(self.NBPatch)+newlines)
        fp.write("# BC  boundary type  no. of facets\n")
        if self.Mbound == [] or self.NBPatch==1:
            Nbface = len(self.bounds)
            Nbpoint = len(set(self.bounds.flatten()))
            Nbedge = Nbpoint + Nbface - 2 # Euler formula
            fp.write("0   "+str(Nbface)+"   "+str(Nbedge)+"   "+str(Nbpoint)+newlines)
        else:
            savefile(self.Mbound, fp, "%d")
        fp.write("# node coordinates" + newlines)
        savefile(self.points, fp, "%1.11e")
        fp.write("# element connectivity" + newlines)
        savefile(self.elements+1, fp, "%d")
        fp.write("# bnodes" + newlines)
        savefile(self.bounds+1, fp, "%d")
        fp.close()
        os.remove("Grid3D_Ttemp.txt")
        return



    def adjustmentDirection(self):
        def tetrahedronVolum(v): #v---4*3
            h =  np.vstack(([1]*4, v.T))
            return np.linalg.det(h)/6.0
        for i,ele in enumerate(self.elements):
            if(tetrahedronVolum(self.points[ele])>0):
                tmp = self.elements[i][1]
                self.elements[i][1] = self.elements[i][2]
                self.elements[i][2] = tmp
        return

if __name__ == '__main__':
    Directoryname = ".//testmesh//"
    # datafile = "tetramesh4x4.dat"
    datafile = "tetrahedrommesh6.dat"
    outputdatafile = "new"+datafile
    grid = Grid3D_T()
    grid.from_meshdat_get_pte(Directoryname+datafile)

    grid.adjustmentDirection()
    grid.outputCppGridDatafile(outputdatafile)