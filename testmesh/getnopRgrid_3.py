#!/usr/bin/env python
# encoding: utf-8
import scipy.io as sio
import numpy as np
import copy
import re
import os
import shutil
#�ڵ�������
def changeNodeIndex(p):
    pp = copy.deepcopy(p)
    NP = pp.shape[1]
    def swap(a, b):
        return b, a
    #����ð������
    ans = range(NP)   #���Ž���
    ansv = range(NP) #����ans����
    for j in range(NP-1):
        for i in range(NP-j-1): #�Խڵ�ѭ��
            if pp[0][i] > pp[0][i+1]:
                (pp[0][i], pp[0][i+1]) = swap(pp[0][i], pp[0][i+1])
                (pp[1][i], pp[1][i+1]) = swap(pp[1][i],pp[1][i+1])
                (ans[i],ans[i+1]) = swap(ans[i],ans[i+1])
            else:
                if (pp[0][i] == pp[0][i+1]) and (pp[1][i] > pp[1][i+1]):
                    (pp[1][i], pp[1][i+1]) = swap(pp[1][i], pp[1][i+1])
                    (ans[i],ans[i+1]) = swap(ans[i],ans[i+1])
    for i in range(NP):
        ansv[ans[i]] = i
    return pp,ans,ansv

#�õ��������Ĺ�������
def getnewtt(tt, v):
    newtt = copy.deepcopy(tt)
    (m, n) = tt.shape
    for i in range(m):
        for j in range(n):
            newtt[i][j] = v[tt[i][j]]
    return newtt


def fromNodGetee(nod):   #���nod���������ν�ľ���t
    (m, n) = nod.shape
    ee = []
    #�ȶ�ÿһ����Ԫ����ѭ��
    for h in range(m):               #����host����Ԫѭ��
        for i in range(n):
            k = 0
            for g in range(m):       #���壨gues��ƥ�䵥Ԫѭ��
                if g != h:           #���͵�Ԫ������ͬ
                    for j in range(n):
                        a = (j+1)%n
                        if nod[h][i] == nod[g][a] and nod[h][(i+1)%n] == nod[g][j]:
                            k = 1
                            break
                if k == 1:
                    break
            if k == 0:
                ee += [[nod[h][i], nod[h][(i+1)%n]]]
    ee = np.array(ee)
    return ee   #outEdge��������߽�ĵ�Ԫ�źͱ߽��


def outputCppGridDatafile(p,t,e,outputfilename):
    if os.path.exists(outputfilename):
        os.remove(outputfilename)
    NPoint = len(p)
    Nele = len(t)
    Nedge = len(e)

    fp = open(outputfilename,"w")
    fp.write("# unstructured grid for a domain\n")
    fp.write("#\n")
    fp.write("# no. of nodes cells and boundaries\n")
    fp.write(str(NPoint)+"     "+ str(Nele)+"     "+str(1)+"\n")
    fp.write("# BC\n")
    fp.write("0   "+str(Nedge)+"   "+str(Nedge)+"\n")
    fp.write("# node coordinates\n")
    for px in p:
        for pxx in px:
             fp.write(str(pxx)+"   ")
        fp.write("\n")
    fp.write("# element connectivity\n")
    for tx in t:
        for txx in tx:
             fp.write(str(txx+1)+"   ")
        fp.write("\n")
    fp.write("# bnodes\n")
    for ex in e:
        for exx in ex:
             fp.write(str(exx+1)+"   ")
        fp.write("\n")

#    np.savetxt("test.dat", p, fmt='%.10e')
    fp.close()
    return

##�õ��������ı߽�ڵ�ָ��
#def getnewee(ee, v):
#    newee = []
#    for i in range(len(ee)):
#        J = np.int8(ee[i])
#        newee += [v[J]]
#    return newee

class Discrete_2D:
    def __init__(self, tfile, pfile, efile):
        datap = sio.loadmat(pfile)   #��
        pp = np.array(datap['p'])

        datat = sio.loadmat(tfile)
        #print datat['t']
        tt =  datat['t'][0:-1,:]
        tt = np.array(tt) - 1
        tt = tt.T



        datae = sio.loadmat(efile)
        #ee = np.array(datae['e'][0:1,:])[0] - 1
        eee = np.array(datae['e'][0:2,:]) - 1
        eee0 = map(int, eee[0])
        eee1 = map(int, eee[1])
        self.eee = np.array([eee0,eee1])

        #print self.eee
        self.pp = pp     #�ڵ�����
        self.ppT = pp.T
        self.tt = tt     #��������
        #self.ee = ee     #�߽�ڵ�
        (self.newpp,self.argsortpp, self.argsortppv) =  changeNodeIndex(pp)

        self.NC =  tt.shape[0]#��Ԫ����
        self.NP = pp.shape[1]#�ڵ����
        self.NE = self.NC + self.NP - 1#�ܱ߽�����,��һ��������ŷ����ʽ

        self.newtt = getnewtt(tt, self.argsortppv)
        self.newee = getnewtt(self.eee, self.argsortppv)
        #print self.newee


    #def __del__(self):
        #class_name = self.__class__.__name__

    #n����ÿ����Ԫ��n���ߣ�ÿ������Ψһһ�����ڵ�Ԫ
    #��ÿ����Ԫ�ϵ�0,1�������ʾ��0���ߣ�������ans�����¼ÿ����Ԫ���ڵ�Ԫ�����
    #��ansx�����¼����Ԫ��ÿ�����ڿ͵�Ԫ������λ��
    def nodbd(self):
        nod = self.tt
        ans = copy.deepcopy(nod)
        ansx = copy.deepcopy(nod)
        (m, n) = nod.shape
        #�ȶ�ÿһ����Ԫ����ѭ��
        for h in range(m):               #����host����Ԫѭ��
            for i in range(n):
                k = 0
                for g in range(m):       #���壨gues��ƥ�䵥Ԫѭ��
                    if g != h:           #���͵�Ԫ������ͬ
                        for j in range(n):
                            a = (j+1)%n
                            if nod[h][i] == nod[g][a] and nod[h][(i+1)%n] == nod[g][j]:
                                ans[h][i] = g
                                ansx[h][i] = j
                                k = 1
                                break
                    if k == 1:
                        break
                if k == 0:
                    ans[h][i] = h
                    ansx[h][i] = i
        return ans, ansx


    #ÿ���ڵ㶼�����ڵĵ�Ԫ����ppnod��¼����
    def ppnod(self):
        eans = []   #���������anum���ڵ�����ڵĵ�Ԫ�ı��
        kans = []   #���������anum���ڵ������ڿ͵�Ԫ��Ӧ�ĵ�Ԫ�ڵ��
        for anum in range(self.NP):
            aa = []
            bb = []
            (m, n) = self.newtt.shape
            for i in range(m):
                for j in range(n):
                    if self.newtt[i][j] == anum:
                        aa += [i]
                        bb += [j]
            eans += [aa]
            kans += [bb]
        return eans, kans


    def findStretchEdge(self, filename):
        newtt = copy.deepcopy(self.tt)
        A = set(self.newee[0]) | set(self.newee[1])

        def rotatenodel(v, n):
            ans = copy.deepcopy(v)
            N = len(v)
            for i, e in enumerate(v):
                ans[i] = v[(n+i)%N]
            return ans

        def findele(v, ob):
            i = 0
            while v[i] != ob:
                i += 1
            return i

        ans, ansx = self.nodbd()
        eans, kans = self.ppnod()
        markele = []  #��Ǳ��Ὺ�ĵ�Ԫ
        newpp = copy.deepcopy(self.pp)
        newpp = newpp.T
        #print "newpp.shape",newpp.shape
        newpp = newpp.tolist()
        markmark = [] #��Ǳ߽类���ı�
        markedge = []
        markmarkp = np.zeros(self.NC)#��Ǳ������ȫ�ֽڵ��
        for i in range(self.NP): #�Խڵ����ѭ��
            temp = []
            if len(eans[i]) == 1:
                markele += eans[i]
                #markele += eans[i]
                ele = eans[i][0]
                I = findele(ans[ele], ele)
                newtt[ele] = rotatenodel(newtt[ele], I)
                a, b =  newtt[ele][0], newtt[ele][1]
                newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                markmarkp[ele] = len(newpp)
                #print i,"=ii"
                markmark += [[a,b]]
                markedge += [len(newpp)-1]
            else:
                eans[i] = list( set(eans[i]) -  set(markele) ) #ȥ���Ѿ��Ὺ�ĵ�Ԫ
                if len(eans[i]) == 0:
                    pass
                #�ж��Ƿ�Ϊ�����ĵ�Ԫ
                elif len(eans[i]) == 1:
                    B = set(self.newtt[eans[i][0]])
                    B = B - A #B������3��Ԫ�أ������ų�����������ֻʣ��һ���Ǳ߽��Ԫ��
                    if len(B)==1: #�ж����е�һ����Ԫ�Ƿ����������ڱ߽���
                        markele += eans[i]
                        #markele += eans[i]
                        ele = eans[i][0]
                        I = findele(ans[ele], ele)
                        newtt[ele] = rotatenodel(newtt[ele], I)
                        a, b =  newtt[ele][0], newtt[ele][1]
                        #print i,"=i"
                        newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                        markmarkp[ele] = len(newpp)
                        markmark += [[a,b]]
                        markedge += [len(newpp)-1]
                        #print "i=",i,"a,b=",a,b
                        #newpp += [0.5*(self.pp[a][0]+self.pp[b][0]), 0.5*(self.pp[a][1]+self.pp[b][1])]
                    else:
                        pass
                else:
                    for e in eans[i]:
                        temp += list(self.newtt[e])  #ѭ����Ϻ���������˽ڵ�J��Χ�Ľڵ�
                    #����ڵ�J��Χ�ڵ����С����ŵ�һ����,Ҫע���ų������Ǹ���
                    mintemp = min(set(temp) - set([i]))
                    #����Ȼ�ҵ�����С�ĵ�ֻ����һ������
                    #�ҵ���С�ĵ������ڵĵ�Ԫ���Լ������ڵ�һ����Ԫ���������Ǽ�¼��markele��
                    for j, p in enumerate(temp):
                        if p == mintemp:
                            minele = eans[i][j/3]
                            break
                    neighborp = min( set(self.newtt[minele]) - set([i, mintemp]) ) #���ȡ��Сֵ�൱��ȡ���ϵ�Ԫ�أ���Ϊ�ǵ�Ԫ�ؼ���
                    for j, p in enumerate(temp):
                        if p == neighborp and minele != eans[i][j/3]:
                            mineleneighbor = eans[i][j/3]
                            break
                    markele += [minele, mineleneighbor]
                    I = findele(ans[minele], mineleneighbor)#IΪ��������minele�еı߽����
                    newtt[minele] = rotatenodel(newtt[minele], I)
                    J = ansx[minele][I]
                    newtt[mineleneighbor] = rotatenodel(newtt[mineleneighbor], J)
                    a, b =  newtt[minele][0], newtt[minele][1]
                    newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                    markmarkp[minele] = len(newpp)
                    markmarkp[mineleneighbor] = len(newpp)
                    #newpp += [0.5*(self.pp[a][0]+self.pp[b][0]), 0.5*(self.pp[a][1]+self.pp[b][1])]
            if  len(eans[i]) == 4:
                AA = list(  set(eans[i]) - set([minele, mineleneighbor])  )
                markele += AA
                I = findele(ans[AA[0]], AA[1])
                newtt[AA[0]] = rotatenodel(newtt[AA[0]], I)
                J = ansx[AA[0]][I]
                newtt[AA[1]] = rotatenodel(newtt[AA[1]], J)
                a, b =  newtt[AA[0]][0], newtt[AA[0]][1]
                newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                markmarkp[AA[0]] = len(newpp)
                markmarkp[AA[1]] = len(newpp)
                #newpp += [0.5*(self.pp[a][0]+self.pp[b][0]), 0.5*(self.pp[a][1]+self.pp[b][1])]
            #print np.array(markele)+1 ,i,"markele,i"
            #print set(markele)
            if len(set(markele)) == self.NC:
                break
        markmarkp = map(int, markmarkp)
        nod = []
        for i in range(self.NC):
            nod += [[newtt[i][2], newtt[i][0], markmarkp[i]-1, newtt[i][1]]]
        nod = np.array(nod)
        newee = fromNodGetee(nod)
        outputCppGridDatafile(newpp,nod,newee,filename)
        return



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



class Discrete_2D_cpp:
    def __init__(self, pp, tt, ee):

        self.eee = ee.T
        self.pp = pp.T     #�ڵ�����
        self.ppT = self.pp.T
        self.tt = tt     #��������
        #self.ee = ee     #�߽�ڵ�
        (self.newpp,self.argsortpp, self.argsortppv) =  changeNodeIndex(self.pp)

        self.NC =  tt.shape[0]#��Ԫ����
        self.NP = pp.shape[0]#�ڵ����
        self.NE = self.NC + self.NP - 1#�ܱ߽�����,��һ��������ŷ����ʽ

        self.newtt = getnewtt(tt, self.argsortppv)
        self.newee = getnewtt(self.eee, self.argsortppv)
        #print self.newee


    #def __del__(self):
        #class_name = self.__class__.__name__

    #n����ÿ����Ԫ��n���ߣ�ÿ������Ψһһ�����ڵ�Ԫ
    #��ÿ����Ԫ�ϵ�0,1�������ʾ��0���ߣ�������ans�����¼ÿ����Ԫ���ڵ�Ԫ�����
    #��ansx�����¼����Ԫ��ÿ�����ڿ͵�Ԫ������λ��
    def nodbd(self):
        nod = self.tt
        ans = copy.deepcopy(nod)
        ansx = copy.deepcopy(nod)
        (m, n) = nod.shape
        #�ȶ�ÿһ����Ԫ����ѭ��
        for h in range(m):               #����host����Ԫѭ��
            for i in range(n):
                k = 0
                for g in range(m):       #���壨gues��ƥ�䵥Ԫѭ��
                    if g != h:           #���͵�Ԫ������ͬ
                        for j in range(n):
                            a = (j+1)%n
                            if nod[h][i] == nod[g][a] and nod[h][(i+1)%n] == nod[g][j]:
                                ans[h][i] = g
                                ansx[h][i] = j
                                k = 1
                                break
                    if k == 1:
                        break
                if k == 0:
                    ans[h][i] = h
                    ansx[h][i] = i
        return ans, ansx


    #ÿ���ڵ㶼�����ڵĵ�Ԫ����ppnod��¼����
    def ppnod(self):
        eans = []   #���������anum���ڵ�����ڵĵ�Ԫ�ı��
        kans = []   #���������anum���ڵ������ڿ͵�Ԫ��Ӧ�ĵ�Ԫ�ڵ��
        for anum in range(self.NP):
            aa = []
            bb = []
            (m, n) = self.newtt.shape
            for i in range(m):
                for j in range(n):
                    if self.newtt[i][j] == anum:
                        aa += [i]
                        bb += [j]
            eans += [aa]
            kans += [bb]
        return eans, kans


    def findStretchEdge(self, filename):
        newtt = copy.deepcopy(self.tt)
        A = set(self.newee[0]) | set(self.newee[1])
        def rotatenodel(v, n):
            ans = copy.deepcopy(v)
            N = len(v)
            for i, e in enumerate(v):
                ans[i] = v[(n+i)%N]
            return ans

        def findele(v, ob):
            i = 0
            while v[i] != ob:
                i += 1
            return i

        ans, ansx = self.nodbd()
        eans, kans = self.ppnod()
        markele = []  #��Ǳ��Ὺ�ĵ�Ԫ
        newpp = copy.deepcopy(self.pp) #����ط����׳���Ҫע�ⲻ��self.pp
        newpp = newpp.T
        #print "newpp.shape",newpp.shape
        newpp = newpp.tolist()
#        print self.newpp
        markmark = [] #��Ǳ߽类���ı�
        markedge = []
        markmarkp = np.zeros(self.NC)#��Ǳ������ȫ�ֽڵ��
        for i in range(self.NP): #�Խڵ����ѭ��
            temp = []
            if len(eans[i]) == 1:
                markele += eans[i]
                #markele += eans[i]
                ele = eans[i][0]
                I = findele(ans[ele], ele)
                newtt[ele] = rotatenodel(newtt[ele], I)
                a, b =  newtt[ele][0], newtt[ele][1]
                newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                markmarkp[ele] = len(newpp)
                #print i,"=ii"
                markmark += [[a,b]]
                markedge += [len(newpp)-1]
            else:
                eans[i] = list( set(eans[i]) -  set(markele) ) #ȥ���Ѿ��Ὺ�ĵ�Ԫ
                if len(eans[i]) == 0:
                    pass
                #�ж��Ƿ�Ϊ�����ĵ�Ԫ
                elif len(eans[i]) == 1:
                    B = set(self.newtt[eans[i][0]])
                    B = B - A #B������3��Ԫ�أ������ų�����������ֻʣ��һ���Ǳ߽��Ԫ��
                    if len(B)==1: #�ж����е�һ����Ԫ�Ƿ����������ڱ߽���
                        markele += eans[i]
                        #markele += eans[i]
                        ele = eans[i][0]
                        I = findele(ans[ele], ele)
                        newtt[ele] = rotatenodel(newtt[ele], I)
                        a, b =  newtt[ele][0], newtt[ele][1]
                        #print i,"=i"
                        newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                        markmarkp[ele] = len(newpp)
                        markmark += [[a,b]]
                        markedge += [len(newpp)-1]
                        #print "i=",i,"a,b=",a,b
                        #newpp += [0.5*(self.pp[a][0]+self.pp[b][0]), 0.5*(self.pp[a][1]+self.pp[b][1])]
                    else:
                        pass
                else:
                    for e in eans[i]:
                        temp += list(self.newtt[e])  #ѭ����Ϻ���������˽ڵ�J��Χ�Ľڵ�
                    #����ڵ�J��Χ�ڵ����С����ŵ�һ����,Ҫע���ų������Ǹ���
                    mintemp = min(set(temp) - set([i]))
                    #����Ȼ�ҵ�����С�ĵ�ֻ����һ������
                    #�ҵ���С�ĵ������ڵĵ�Ԫ���Լ������ڵ�һ����Ԫ���������Ǽ�¼��markele��
                    for j, p in enumerate(temp):
                        if p == mintemp:
                            minele = eans[i][j/3]
                            break
                    neighborp = min( set(self.newtt[minele]) - set([i, mintemp]) ) #���ȡ��Сֵ�൱��ȡ���ϵ�Ԫ�أ���Ϊ�ǵ�Ԫ�ؼ���
                    for j, p in enumerate(temp):
                        if p == neighborp and minele != eans[i][j/3]:
                            mineleneighbor = eans[i][j/3]
                            break
                    markele += [minele, mineleneighbor]
                    I = findele(ans[minele], mineleneighbor)#IΪ��������minele�еı߽����
                    newtt[minele] = rotatenodel(newtt[minele], I)
                    J = ansx[minele][I]
                    newtt[mineleneighbor] = rotatenodel(newtt[mineleneighbor], J)
                    a, b =  newtt[minele][0], newtt[minele][1]
                    newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                    markmarkp[minele] = len(newpp)
                    markmarkp[mineleneighbor] = len(newpp)
                    #newpp += [0.5*(self.pp[a][0]+self.pp[b][0]), 0.5*(self.pp[a][1]+self.pp[b][1])]
            if  len(eans[i]) == 4:
                AA = list(  set(eans[i]) - set([minele, mineleneighbor])  )
                markele += AA
                I = findele(ans[AA[0]], AA[1])
                newtt[AA[0]] = rotatenodel(newtt[AA[0]], I)
                J = ansx[AA[0]][I]
                newtt[AA[1]] = rotatenodel(newtt[AA[1]], J)
                a, b =  newtt[AA[0]][0], newtt[AA[0]][1]
                newpp +=[[0.5*(self.ppT[a][0]+self.ppT[b][0]), 0.5*(self.ppT[a][1]+self.ppT[b][1])]]
                markmarkp[AA[0]] = len(newpp)
                markmarkp[AA[1]] = len(newpp)
                #newpp += [0.5*(self.pp[a][0]+self.pp[b][0]), 0.5*(self.pp[a][1]+self.pp[b][1])]
            #print np.array(markele)+1 ,i,"markele,i"
            #print set(markele)
            if len(set(markele)) == self.NC:
                break
        markmarkp = map(int, markmarkp)
        nod = []
        for i in range(self.NC):
            nod += [[newtt[i][2], newtt[i][0], markmarkp[i]-1, newtt[i][1]]]
        nod = np.array(nod)
        newee = fromNodGetee(nod)

        pp = np.array(newpp)
        outputCppGridDatafile(pp,nod,newee,filename)
        return





if __name__ == '__main__':

#    �򵥵������
#    tfile = "tsmall.mat"
#    pfile = "psmall.mat"
#    efile = "esmall.mat"
#    a = Discrete_2D(tfile, pfile, efile)
#    a.findStretchEdge("smallRmesh11111.dat")


#    tfile = "tt.mat"
#    pfile = "pp.mat"
#    efile = "ee.mat"
#    a = Discrete_2D(tfile, pfile, efile)
#    a.findStretchEdge("newRT_"+"dumbbell_mesh1.dat")

    Directoryname = ".//Tdumbbell//"
    datafiles = ["newdumbbell_mesh1.dat", "Add_1_newdumbbell_mesh1.dat"]
    datafile = datafiles[1]
    # datafile = "dumbbell_mesh1.dat"
#    datafile = "Tmesh4x4.dat"
    p, t, e = getCppGrid_pte(Directoryname+datafile)
    a = Discrete_2D_cpp(p*1.5, t, e)
    a.findStretchEdge("newRT_"+datafile)


