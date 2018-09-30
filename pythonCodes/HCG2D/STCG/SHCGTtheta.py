#!/usr/bin/env python
# encoding: utf-8

import scipy.io as sio
import copy
import re
import os
import shutil
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#A standard  code to get the lobatto points and the weights
def getlobattop(n):
    n = n-3
    if n==0:
        print "n i stoo small"
        return
    u = [np.sqrt(1.0*j/(2*j+1)*(j+2)/(2*j+3)) for j in range(1, n+1)]
    [bp, vc] = np.linalg.eig(np.diag(u, 1) + np.diag(u, -1))
    bp = np.sort(bp)          #bp the integration points
    bp = np.hstack(( bp, np.array([1])))
    bp = np.hstack(( np.array([-1]), bp))
    return bp

def mappingT_theta(theta):
    def T_theta(xi, eta):
        x = 0.25*(1+xi)*(2-(1-theta)*(1+eta))
        y = 0.25*(1+eta)*(2-theta*(1+xi))
        return x,y
    return T_theta

#绘制标准矩形区域上的点
n = 8
lglpoints = getlobattop(n)

fig = plt.figure(figsize=(8,8), dpi=72,facecolor="white")
axes = plt.subplot(111)

#设置坐标轴的范围


xedge = [lglpoints[0], lglpoints[-1], lglpoints[-1], lglpoints[0], lglpoints[0]]
yedge = [lglpoints[0], lglpoints[0], lglpoints[-1], lglpoints[-1], lglpoints[0]]
xedge = np.array(xedge)
yedge = np.array(yedge)

theta = 0.5
xedge, yedge = mappingT_theta(theta)(xedge, yedge)
axes.plot(xedge, yedge, color='blue', linestyle='solid', marker='',
         markerfacecolor='blue', linewidth=8)
for i in lglpoints[1:-1]:
    x, y = mappingT_theta(theta)(np.array([i,i]), np.array([-1,1]))
    axes.plot(x, y, color='black', linestyle='dashed', marker='',
             markerfacecolor='black', linewidth=0.3)
    x, y = mappingT_theta(theta)(np.array([-1,1]), np.array([i,i]))
    axes.plot(x, y, color='black', linestyle='dashed', marker='',
             markerfacecolor='black', linewidth=0.3)
for i in lglpoints:
    for j in lglpoints:
        x, y = mappingT_theta(theta)(np.array([i]), np.array([j]))
        axes.plot(x, y, color='red', linestyle='dashed', marker='o',
             markerfacecolor='red', markersize=8)
for i in range(4):
    x,y = xedge[i], yedge[i]
    axes.plot(x, y, color='red', linestyle='dashed', marker='o',
             markerfacecolor='red', markersize=12)

k = 1; h = 0.02
ftz = 40; a = ftz*0.0005
axes.set_xlim(k*xedge.min()-h, k*xedge.max()+h)
axes.set_ylim(k*yedge.min()-h, k*yedge.max()+h)
axes.text(theta, 1-theta,"$(\\frac{1}{2}, \\frac{1}{2})$",fontsize = ftz, verticalalignment='bottom', horizontalalignment='left')
axes.text(0, 1+a*0.5,"$(0, 1)$",fontsize = ftz, verticalalignment='bottom', horizontalalignment='center')
axes.text(0, -a,"$(0,0)$",fontsize = ftz, verticalalignment='top', horizontalalignment='center')
axes.text(1, -a,"$(1,0)$",fontsize = ftz, verticalalignment='top', horizontalalignment='center')
axes.set_xticks([])
axes.set_yticks([])
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['bottom'].set_color('none')
axes.spines['left'].set_color('none')
#axes.set_axticks(minor = False)
plt.savefig("Ttheta.pdf",dip=120)
plt.show()
#help(plt.plot)
