#!/usr/bin/env python
# encoding: utf-8
from pyGrid2D.Grid2D import Grid2D, plotblank
import matplotlib.pyplot as plt
import numpy as np
from Function.functionQuad import Quadrature

# Directoryname = ".//testmesh//"
# # Directoryname = "..//testmesh//RTdumbbell//"
# # datafile = "newRT_dumbbell_mesh1.dat"
# datafile = "4times4_rect.dat"

# datafile = "meshRT.dat"
# Directoryname = "..//testmesh//RT11//"


# Directoryname = "..//testmesh//rectangle01//"
# datafiles = ["meshR.dat", "meshRRR.dat", "AddDensity_1_meshRRR.dat",
#              "AddDensity_2_meshRRR.dat", "AddDensity_3_meshRRR.dat", "AddDensity_4_meshRRR.dat"]
# datafile = datafiles[2]


Directoryname = "..//testmesh//RTdumbbell//"
datafiles = ["newRT_dumbbell_mesh1.dat", "AddDensity_1_newRT_dumbbell_mesh1.dat"]
datafile = datafiles[0]

#
# Directoryname = "..//testmesh//"
# datafile = "newRT_Add_1_newdumbbell_mesh1.dat"

# datafile = "sixbianxing.dat"
# outputdatafile = "new"+datafile
grid = Grid2D()
grid.from_meshdat_get_pte(Directoryname+datafile)


def changeNodeIndex(p):
    pp = p.copy()
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
    newtt = tt.copy()
    (m, n) = tt.shape
    for i in range(m):
        for j in range(n):
            newtt[i][j] = v[tt[i][j]]
    return newtt
p,t,e = grid.points, grid.elements, grid.bounds
start = t.T[2].min()
# (newpp,argsortpp, argsortppv) = changeNodeIndex(grid.points)
# newtt = getnewtt(grid.elements, argsortppv)
# grid.points, grid.elements = newpp, newtt

grid.readGrid()











fig = plt.figure(figsize=(20,10), dpi=72,facecolor="white")
# fig_mpl, ax = plt.subplots(1,figsize=(5,3), facecolor='white')
axes = plt.subplot(111)

#
quad = Quadrature(3)
quad.getLobattoPiontsWeights()
# grid.plotmesh2d(axes)
# grid.plotNodeDistribution(axes, [], plotnodenum=False, pointsize=0.1, ftz=20, linewidth=5)
# grid.plotNodeDistribution(axes, quad.points, plotnodenum=True, pointsize=0.1, ftz=20, linewidth=5)
# grid.plotNodeDistribution(axes, quad.points, False)

grid.plotmesh2d(axes, pointsize=6,plotpointsnum=False, plotelementsnum=False, plotedgesnum=False)

plotblank(axes)



import imageio,os
images = []
for i in range(start, len(p)):
    for ele in grid.pointNeibEle[i]:
        x,y = grid.points[t[ele]].T
        x = np.hstack((x, x[0]))
        y = np.hstack((y, y[0]))
        axes.fill(x, y, "g", alpha=0.7)
    axes.plot(p[i][0], p[i][1], "o", color="red")
    # axes.text(p[i][0], p[i][1], str(i - start), color='blue', fontsize=35, verticalalignment='center', horizontalalignment='center')
    # plt.savefig('.//figs//'+datafile+'%d.png' % (i - start))
    plt.savefig("tmp.png")
    images.append(imageio.imread("tmp.png"))
if os.path.exists("tmp.png"):
    os.remove("tmp.png")

# plt.savefig('.//figs//'+datafile+'.pdf')
#
imageio.mimsave(datafile+'.gif', images, duration=0.6)
