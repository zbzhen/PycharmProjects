#!/usr/bin/env python
# encoding: utf-8
import scipy.io as sio
import numpy as np
import copy
import re
import os
import shutil

#ֻ��Ҫ����������Ϣ�������������p����Ԫ�Ĺ�������t
#����ʵ�����¹���
#
#��������
#1.�õ�NeibEle�����Լ�NeibEleEdge����outEdge
#NeibEle[i][j]��NeibEleEdge[i][j]�ֱ��ʾ��i����Ԫ�ĵ�j���ߵ�
#���ڵ�Ԫ����Լ��ñ������ڵ�Ԫ�ıߵı��
#
#2.�õ�NumEdge�����Լ�EdgeMessage����
#NumEdge[i][j]��ʾ��i����Ԫ�ĵ�j���ߵ�ȫ�ֱ��
#EdgeMessage[I]��ʾȫ�ֱ��ΪI�ı߽磬�ľֲ��߽���
#ÿ���߶����������ڵ�Ԫ����߽���Ȼֻ��һ������һ�����Լ��������Ի�������
#EdgeMessage[I][0]ΪI�ű߽����С���ڵ�Ԫ���
#EdgeMessage[I][1]ΪI�ű߽��ڸñ߽����С���ڵ�Ԫ�ľֲ����
#EdgeMessage[I][2]ΪI�ű߽��������ڵ�Ԫ���
#EdgeMessage[I][3]ΪI�ű߽��ڸñ߽��������ڵ�Ԫ�ľֲ����
#
#3.�õ�OutEdgeGlobIndex�����ͱ߽����t
#OutEdgeGlobIndex�����������߽�����
#
#
#
#ʵ�ù���
#1.���룺���Ե���matlab��CppGrid�����ļ����Ӷ���ȡp,e,t
#���õ�pet����ȫ������CppGrid���������з�ʽ�ŷţ�ͬʱ���Ǵ�0����
#2.������ͨ��p,e,t,���Ե���c++���������ļ�
#
#
#���ù���
#1.����������õ��ı�������
#2.��ȥ����ĳ��С����õ��µ�����
#3.�����е����
#4.�ڵ�������
def getCppGrid_pte(datafile):
    lines = open(datafile).readlines() #���ļ�������ÿһ��
    f1 = open("numxxx.dat",'w')
    f2 = open("btypexxx.dat",'w')
    f3 = open("pxxx.dat",'w')
    f4 = open("txxx.dat",'w')
    f5 = open("exxx.dat",'w')
    f1.write(lines[3])
    f1.close() # �ر��ļ�

    vnum = np.loadtxt("numxxx.dat")
    vnum = map(int, vnum)
    for f in lines[5 : vnum[2]+5]:
        f2.write(f)

    for f in lines[vnum[2]+6 : vnum[0]+vnum[2]+6]:
        f3.write(f)

    for f in lines[vnum[0]+vnum[2]+7:vnum[0]+vnum[2]+7+vnum[1]]:
        f4.write(f)

    for f in lines[vnum[0]+vnum[2]+8+vnum[1]:]:
        f5.write(f)


    f2.close() # �ر��ļ�
    f3.close() # �ر��ļ�
    f4.close() # �ر��ļ�
    f5.close() # �ر��ļ�

    p = np.loadtxt("pxxx.dat")
    t = np.loadtxt("txxx.dat")
    e = np.loadtxt("exxx.dat")
    newp = []
    for i in range(len(p.T)):
        newp += [map(float, p.T[i])]
    newt = []
    for i in range(len(t.T)):
        newt += [map(int, t.T[i])]
    newe = []
    for i in range(len(e.T)):
        newe += [map(int, e.T[i])]


    os.remove("numxxx.dat")
    os.remove("btypexxx.dat")
    os.remove("pxxx.dat")
    os.remove("txxx.dat")
    os.remove("exxx.dat")
    newp = np.array(newp).T
    newt = np.array(newt).T-1
    newe = np.array(newe).T-1
    return newp, newt, newe

def getMatlabGrid_pte(pfile,tfile,efile):
    datap = sio.loadmat(pfile)   #��
    pp = np.array(datap['p']).T
    datat = sio.loadmat(tfile)
    tt =  datat['t'][0:-1,:]
    tt = np.array(tt) - 1
    tt = tt.T
    datae = sio.loadmat(efile)
    eee = np.array(datae['e'][0:2,:]) - 1
    eee0 = map(int, eee[0])
    eee1 = map(int, eee[1])
    ee  = np.array([eee0,eee1]).T
    return pp, tt, ee

#�������̫���˴�����
def outputCppGridDatafile(p,t,e,outputfilename):
    if os.path.exists(outputfilename):
        os.remove(outputfilename)
    NPoint = len(p)
    Nele = len(t)
    Nedge = len(e)

    fp = open(outputfilename,"w")
    fp.write("# unstructured grid for a domain\r\n")
    fp.write("#\r\n")
    fp.write("# no. of nodes cells and boundaries\r\n")
    fp.write(str(NPoint)+"     "+ str(Nele)+"     "+str(1)+"\r\n")
    fp.write("# BC\r\n")
    fp.write("0   "+str(Nedge)+"   "+str(Nedge)+"\r\n")
    fp.write("# node coordinates\r\n")
    for px in p:
        for pxx in px:
             fp.write(str(pxx)+"   ")
        fp.write("\r\n")
    fp.write("# element connectivity\r\n")
    for tx in t:
        for txx in tx:
             fp.write(str(txx+1)+"   ")
        fp.write("\r\n")
    fp.write("# bnodes\r\n")
    for ex in e:
        for exx in ex:
             fp.write(str(exx+1)+"   ")
        fp.write("\r\n")

#    np.savetxt("test.dat", p, fmt='%.10e')
    fp.close()
    return

def getNeibEle_index(nod):   #���nod���������ν�ľ���t
    NeibEle = copy.deepcopy(nod)
    NeibEleEdge = copy.deepcopy(nod)
    (m, n) = nod.shape
    outEdge = []
    #�ȶ�ÿһ����Ԫ����ѭ��
    for h in range(m):               #����host����Ԫѭ��
        for i in range(n):
            k = 0
            for g in range(m):       #���壨gues��ƥ�䵥Ԫѭ��
                if g != h:           #���͵�Ԫ������ͬ
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
    return NeibEle, NeibEleEdge, outEdge   #outEdge��������߽�ĵ�Ԫ�źͱ߽��


#Ҫ�ҵ�i����Ԫ�ĵ�j���ߵ�ȫ�ֱ�ţ�������NumEdge[i][j]
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


#�õ��ߵ�����������Ԫ�Լ������ڵľֲ���ţ��ֱ���������������
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

#�õ��߽��������
def fromEdgeGetPoint(p,nod, EdgeMessage):
    (m, n) = nod.shape
    EdgeTwoP = []
    for edge in EdgeMessage:
        i,j = edge
        I = nod[i][j]
        J = nod[i][(j+1)%n]
        EdgeTwoP += [[p[I].tolist(), p[J].tolist()]]
    return EdgeTwoP

#�߽��е�
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

#�ȿ���ֻ����һ�ε�,ע����������Ѿ�Ĭ����n=4
def QuadrilateralAddDensity(p, t, e, outputfilename):
    (m, n) = t.shape
    if n != 4:
        print "please put Quadrilateral mesh"
        return
    newp = copy.deepcopy(p).tolist()
    #�����Ǻ�����ĸ��ֵ���
    NeibEle, NeibEleEdge, outEdge = getNeibEle_index(t)
    NumEdge, k = getNumEdge(NeibEle,NeibEleEdge)
    EdgeMessage1, EdgeMessage2 = getEdgeMessage(NumEdge, k)
    EdgeMidP = getEdgeMidpoint(p,t, EdgeMessage1)
    EleMidP = getELeMidpoint(p,t)

    #���������ӵĵ�
    newp += EdgeMidP + EleMidP

    #�����������Ĺ�������
    newt = []
    Np = len(p)
    for i in range(m):
        #�ж���α�����λ����ı���
        if abs(2*p[t[i][2]][0] - p[t[i][1]][0] - p[t[i][3]][0]) < 1.0e-10   and abs(2*p[t[i][2]][1] - p[t[i][1]][1] - p[t[i][3]][1]) < 1.0e-10 :
            newt += [[t[i][0], Np+NumEdge[i][0], Np+k+i, Np+NumEdge[i][3]]]
            newt += [[Np+NumEdge[i][0], t[i][1], Np+NumEdge[i][1], t[i][2]]]
            newt += [[Np+NumEdge[i][3], t[i][2], Np+NumEdge[i][2], t[i][3]]]
            newt += [[t[i][2], Np+NumEdge[i][3], Np+k+i, Np+NumEdge[i][0]]]
        else:
            newt += [[t[i][0], Np+NumEdge[i][0], Np+k+i, Np+NumEdge[i][3]]]
            newt += [[Np+NumEdge[i][0], t[i][1], Np+NumEdge[i][1], Np+k+i]]
            newt += [[Np+NumEdge[i][3], Np+k+i, Np+NumEdge[i][2], t[i][3]]]
            newt += [[Np+k+i, Np+NumEdge[i][1], t[i][2], Np+NumEdge[i][2]]]

    #������ܺ�����ı߽�
    newe = []
    for oe in outEdge:
        i, j = oe
        newe += [[t[i][j], Np+NumEdge[i][j]]]
        newe += [[Np+NumEdge[i][j] , t[i][(j+1)%n]]]
    outputCppGridDatafile(newp,newt,newe,outputfilename)
    return

#���Ǽ���d�ε�,ע����������Ѿ�Ĭ����n=4
#def QuadrilateralAddDensity(p, t, e, outputfilename,d):
#    return

if __name__ == '__main__':

    #�򵥵������
#    tfile = "tsmall.mat"
#    pfile = "psmall.mat"
#    efile = "esmall.mat"
#    datafileR = "Rmesh4x4.dat"
#    datafileT = "Tmesh4x4.dat"
#    newp, newt, newe = getCppGrid_pte(datafileR)
#    pp, tt, ee = getMatlabGrid_pte(pfile,tfile,efile)

#    outputfilename = "new" + datafileT
#    pp,tt,ee = getCppGrid_pte(datafileT)
#    outputCppGridDatafile(pp,tt,ee,outputfilename)
#
#    nod = tt
#    NeibEle, NeibEleEdge, outEdge = getNeibEle_index(nod)
#    NumEdge, k = getNumEdge(NeibEle,NeibEleEdge)
#    EdgeMessage1, EdgeMessage2 = getEdgeMessage(NumEdge, k)
#
#    EdgeTwoP = fromEdgeGetPoint(pp,nod, EdgeMessage1)
#    EdgeMidP = getEdgeMidpoint(pp,nod, EdgeMessage1)

    #inputfilename = "newRT_dumbbell_mesh1.dat"
    #inputfilename = "meshH.dat"
    #inputfilename = "meshRRR.dat"


#    inputfilename = "AddDensity_2_meshRRR.dat"
##    inputfilename = "meshRT.dat"
#    p, t, e = getCppGrid_pte(inputfilename)
##    p = 2*p-1
#    p = 0.5*(p+1)
##    print p
#    outputCppGridDatafile(p,t,e,inputfilename)

    dr = ".//rectTrembled//"
    p, t, e = getCppGrid_pte(dr + "AddDensity_3_4times4_rectTrembled.dat")
    QuadrilateralAddDensity(p, t, e, dr + "AddDensity_4_4times4_rectTrembled.dat")



#    inputfilename = "meshRT.dat"

#    outputfilename = "AddDensity_" + str(1) + "_" + inputfilename
#    p, t, e = getCppGrid_pte(inputfilename)
#    QuadrilateralAddDensity(p, t, e, outputfilename)
#
#    for d in range(1,4):
#        datafile = "AddDensity_" + str(d) + "_" + inputfilename
#        outputfilename = "AddDensity_" + str(d+1) + "_" + inputfilename
#        p, t, e = getCppGrid_pte(datafile)
#        QuadrilateralAddDensity(p, t, e, outputfilename)

