#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: DuffyAdd
@time: 2017-03-13 18:50
"""
#---------------------------------------------------
import copy
import re
import numpy as np
import matplotlib.pyplot as plt
import os
#---------------------------------------------------
#这个函数太慢了待处理
# def outputCppGridDatafile(p,t,e,outputfilename):
#     if os.path.exists(outputfilename):
#         os.remove(outputfilename)
#     NPoint = len(p)
#     Nele = len(t)
#     Nedge = len(e)
#
#     fp = open(outputfilename,"w")
#     fp.write("# unstructured grid for a domain\r\n")
#     fp.write("#\r\n")
#     fp.write("# no. of nodes cells and boundaries\r\n")
#     fp.write(str(NPoint)+"     "+ str(Nele)+"     "+str(1)+"\r\n")
#     fp.write("# BC\r\n")
#     fp.write("0   "+str(Nedge)+"   "+str(Nedge)+"\r\n")
#     fp.write("# node coordinates\r\n")
#     for px in p:
#         for pxx in px:
#              fp.write(str(pxx)+"   ")
#         fp.write("\r\n")
#     fp.write("# element connectivity\r\n")
#     for tx in t:
#         for txx in tx:
#              fp.write(str(txx+1)+"   ")
#         fp.write("\r\n")
#     fp.write("# bnodes\r\n")
#     for ex in e:
#         for exx in ex:
#              fp.write(str(exx+1)+"   ")
#         fp.write("\r\n")
#
# #    np.savetxt("test.dat", p, fmt='%.10e')
#     fp.close()
#     return
def outputCppGridDatafile(p,t,e, outputfilename):
    # if os.path.exists(outputfilename):
    #     os.remove(outputfilename)
    p = np.array(p)
    t = np.array(t)
    e = np.array(e)
    newlines = "\r\n"
    import platform
    if  platform.system() == "Windows":
        newlines = "\n"
    def savefile(xxxx, fmts):
        np.savetxt("Grid2Dtemp.txt", xxxx, fmt=fmts)
        with open("Grid2Dtemp.txt") as f:
            lines = f.readlines()
            fp.writelines(lines)
        return
    NPoint, Nele, Nedge = len(p), len(t), len(e)

    fp = open(outputfilename,"w")
    fp.write("# unstructured grid for a domain" + newlines)
    fp.write("#" + newlines)
    fp.write("# no. of nodes cells and boundaries" + newlines)
    fp.write(str(NPoint)+"     "+ str(Nele)+"     "+str(1)+newlines)
    fp.write("# BC" + newlines)
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
def getNeibEle_index(nod):   #这个nod矩阵就是所谓的矩阵t
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
                        a = (j+1)%n
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
    outEdge = np.array(outEdge)
    return NeibEle, NeibEleEdge, outEdge   #outEdge矩阵是外边界的单元号和边界号


#要找第i个单元的第j条边的全局编号，果断找NumEdge[i][j]
def getNumEdge(NeibEle,NeibEleEdge):
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
    return NumEdge,k+1


#得到边的相邻两个单元以及边所在的局部标号，分别存放在两个矩阵中
def getEdgeMessage(NumEdge, k):
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
    return EdgeMessage1, EdgeMessage2

#def fromEdgeGetPoint(node,NeibEle,NeibEleEdge):
#    EdgeTwoP = []
#    k = -1
#    for h in range(m):
#        for i in range(n):
#            if NeibEle[h][i] >= h:
#                EdgeTwoP += [[]]
#
#    return

#得到边界的两个点
def fromEdgeGetPoint(p,nod, EdgeMessage):
    (m, n) = nod.shape
    EdgeTwoP = []
    for edge in EdgeMessage:
        i,j = edge
        I = nod[i][j]
        J = nod[i][(j+1)%n]
        EdgeTwoP += [[p[I].tolist(), p[J].tolist()]]
    return EdgeTwoP

#边界中点
def getEdgeMidpoint(p,nod, EdgeMessage):
    (m, n) = nod.shape
    EdgeMidP = []
    for edge in EdgeMessage:
        i,j = edge
        I = nod[i][j]
        J = nod[i][(j+1)%n]
        EdgeMidP += [[0.5*(p[I][0]+p[J][0]), 0.5*(p[I][1]+p[J][1])]]
    return EdgeMidP


def getELeMidpoint(p,nod):
    (m, n) = nod.shape
    EleMidP = []
    for ele in nod:
        I,J = ele[0], ele[2]
        EleMidP += [[0.5*(p[I][0]+p[J][0]), 0.5*(p[I][1]+p[J][1])]]
    return EleMidP

#先考虑只加密一次的,注意这个函数已经默认了n=4
def QuadrilateralAddDensity(p, t, e, outputfilename):
    (m, n) = t.shape
    if n != 3:
        print "please put triangluar mesh"
        return
    newp = copy.deepcopy(p).tolist()
    #下面是函数间的各种调用
    NeibEle, NeibEleEdge, outEdge = getNeibEle_index(t)
    NumEdge, k = getNumEdge(NeibEle,NeibEleEdge)
    EdgeMessage1, EdgeMessage2 = getEdgeMessage(NumEdge, k)
    EdgeMidP = getEdgeMidpoint(p,t, EdgeMessage1)
    EleMidP = getELeMidpoint(p,t)

    #处理新增加的点
    newp += EdgeMidP

    #处理加密网格的关联矩阵
    newt = []
    Np = len(p)
    for i in range(m):
        newt += [[Np+NumEdge[i][0], Np+NumEdge[i][2], t[i][0]]]
        newt += [[Np+NumEdge[i][0],t[i][1], Np+NumEdge[i][1] ]]
        newt += [[Np+NumEdge[i][1],Np+NumEdge[i][2], Np+NumEdge[i][0]]]
        newt += [[t[i][2],Np+NumEdge[i][2], Np+NumEdge[i][1]]]
    #处理加密后网格的边界
    newe = []
    for k,oe in  enumerate(outEdge) :
        i, j = oe
        newe += [[t[i][j], Np+NumEdge[i][j]]]
        newe += [[Np+NumEdge[i][j] , t[i][(j+1)%n]]]
    outputCppGridDatafile(newp,newt,newe,outputfilename)
    return

# def from_meshdat_get_pet(datafile):
#     with open(datafile) as f:
#         lines = f.readlines()
#         npoint, nelement = np.loadtxt(lines[3:4],int)[0:2]
#         #nedgepoint, nedge = np.loadtxt(lines[5:6],int)[1:3]
#         points = np.loadtxt(lines[7:(7+npoint)],float)
#         elements = np.loadtxt(lines[8+npoint:(8+npoint+nelement)],int)-1
#         edges = np.loadtxt(lines[9+npoint+nelement:],int)-1
#     return points, elements, edges

def from_meshdat_get_pet(datafile):
    with open(datafile) as f:
        lines = f.readlines()
        Npoint, Nelement, NBPatch = np.loadtxt(lines[3 : 4], int)
        Mbound = np.loadtxt(lines[5:5+NBPatch], int)
        points = np.loadtxt(lines[6+NBPatch : (6+NBPatch+Npoint)], float)
        elements = np.loadtxt(lines[7+NBPatch+Npoint : (7+NBPatch+Npoint+Nelement)], int)-1
        bounds = np.loadtxt(lines[8+NBPatch+Npoint+Nelement : ], int)-1
    return points, elements, bounds
if __name__ == '__main__':
    # path = "..//mesh_one//"
    # inputfilename = "mesh4x4.dat"
    path = "..//mesh_one//"
    inputfilenames = ["mesh2x2.dat","mesh4x4.dat","mesh8x8.dat","mesh16x16.dat","mesh32x32.dat","mesh64x64.dat","mesh128x128.dat"]
    # inputfilename = "mesh4x4.dat"
    # for inputfilename in inputfilenames:
        # points, elements, edges = from_meshdat_get_pet(path+inputfilename)
        # outputfilename = path+"zero" + inputfilename
        # outputCppGridDatafile(0.5+0.5*points, elements, edges, outputfilename)
    inputfilename = "zeromesh64x64.dat"
    points, elements, edges = from_meshdat_get_pet(inputfilename)
    points = points*2 - 1
    QuadrilateralAddDensity(points, elements, edges, inputfilename)


#    points, elements, edges = from_meshdat_get_pet(path+inputfilename)
#    outputfilename = "Add_1_" + inputfilename
#    QuadrilateralAddDensity(points, elements, edges, path+outputfilename)


    # for d in range(1,5):
        # datafile = "Add_" + str(d) + "_" + inputfilename
        # outputfilename = "Add_" + str(d+1) + "_" + inputfilename
        # p, t, e = from_meshdat_get_pet(datafile)
        # QuadrilateralAddDensity(p, t, e, outputfilename)
