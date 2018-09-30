#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 8:54
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : Tcubemapping2.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-0.2,0.9)
plt.ylim(-0.7,1.3)

p1 = np.array([0,0])
p5 = np.array([0,1])
p4 = np.array([0.48,0.2])
p2 = np.array([0.16,-0.5])
p3 = 0.5*(p2+p4)
p8 = 0.5*(p4+p5)
p6 = 0.5*(p2+p5)
p7 = 0.33333333*(p2+p4+p5)
plt.plot(p1[0],p1[1],'ko')
plt.plot(p2[0],p2[1],'ko')
plt.plot(p3[0],p3[1],'ko')
plt.plot(p4[0],p4[1],'ko')
plt.plot(p5[0],p5[1],'ko')
plt.plot(p6[0],p6[1],'ko')
plt.plot(p7[0],p7[1],'ko')
plt.plot(p8[0],p8[1],'ko')

plt.text(p1[0],p1[1],"$P_1$",fontsize = 20, verticalalignment='top', horizontalalignment='right')
plt.text(p2[0],p2[1],"$P_2$",fontsize = 20, verticalalignment='top', horizontalalignment='right')
plt.text(p3[0],p3[1],"$P_3$",fontsize = 20, verticalalignment='top', horizontalalignment='left')
plt.text(p4[0],p4[1],"$P_4$",fontsize = 20, verticalalignment='top', horizontalalignment='left')
plt.text(p5[0],p5[1],"$P_5$",fontsize = 20, verticalalignment='top', horizontalalignment='right')
plt.text(p6[0],p6[1],"$P_6$",fontsize = 20, verticalalignment='bottom', horizontalalignment='left')
plt.text(p7[0],p7[1],"$P_7$",fontsize = 20, verticalalignment='bottom', horizontalalignment='left')
plt.text(p8[0],p8[1],"$P_8$",fontsize = 20, verticalalignment='bottom', horizontalalignment='left')



xz1 = 0.25*(p1+p2+p6+p5)
xz2 = 0.25*(p4+p3+p7+p8)
plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "bo")
# plt.text(xz1[0], xz1[1], "$F_\\eta^-$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "b")
# plt.text(xz2[0], xz2[1], "$F_\\eta^+$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "b")
xz1 = 0.25*(p1+p4+p8+p5)
xz2 = 0.25*(p2+p3+p7+p6)
plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "go")
# plt.text(xz1[0], xz1[1], "$F_\\xi^-$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "g")
# plt.text(xz2[0], xz2[1], "$F_\\xi^+$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "g")
xz1 = 0.25*(p1+p2+p3+p4)
xz2 = 0.25*(p5+p6+p7+p8)
plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "--")
plt.plot([xz1[0], xz2[0]], [xz1[1], xz2[1]], "ro")
# plt.text(xz1[0], xz1[1], "$F_\\zeta^-$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "r")
# plt.text(xz2[0], xz2[1], "$F_\\zeta^+$", fontsize=18, verticalalignment='top', horizontalalignment='left',color = "r")

tt = 0.5*np.array([p1+p4, p2+p3, p6+p7, p5+p8, p1+p4]).T
plt.fill(tt[0], tt[1], 'red', alpha = 0.3)
tt = 0.5*np.array([p1+p2, p4+p3, p8+p7, p5+p6, p1+p2]).T
plt.fill(tt[0], tt[1], 'b', alpha = 0.3)
tt = 0.5*np.array([p1+p5, p2+p6, p3+p7, p4+p8, p1+p5]).T
plt.fill(tt[0], tt[1], 'g', alpha = 0.3)







plt.plot([p1[0], p2[0], p4[0], p5[0], p1[0]], [p1[1], p2[1], p4[1], p5[1], p1[1]], "black")
plt.plot([p1[0], p4[0]], [p1[1], p4[1]], "--", color = "black")
plt.plot([p2[0], p5[0]], [p2[1], p5[1]], "black")
plt.plot([p7[0], p3[0]], [p7[1], p3[1]], color = "black")
plt.plot([p7[0], p6[0]], [p7[1], p6[1]], color = "black")
plt.plot([p7[0], p8[0]], [p7[1], p8[1]], color = "black")

plt.savefig("Tcubemapping2.pdf",dip=120)
plt.show()