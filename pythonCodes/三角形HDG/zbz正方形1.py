# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:24:07 2016

@author: Administrator
"""


import numpy as np
import matplotlib.pyplot as plt
#设置坐标轴的范围
plt.xlim(-2,2)
plt.ylim(-1.6,1.6)

#画出点以及标出数字
plotpoint = plt.plot([-1,-1,-1],[-1, 0, 1],'bo')
#plotpoint1 = plt.plot([0],[1],'bo')

plt.text(-1.2,0.9,r'$\widehat{A}$',color="blue",fontsize=20,ha="center")
plt.text(-1.2,-0.1,r'$\widehat{B}$',color="blue",fontsize=20,ha="center")
plt.text(-1.2,-1.1,r'$\widehat{C}$',color="blue",fontsize=20,ha="center")
plt.text(-0.8,-0.6,r'$\widehat{\Gamma}_{+}$',color="blue",fontsize=20,ha="center")
plt.text(-0.8,0.4,r'$\widehat{\Gamma}_{-}$',color="blue",fontsize=20,ha="center")

Rx=[-1, 1, 1, -1, -1]
Ry=[-1, -1, 1, 1, -1]
plt.plot(Rx, Ry, "r")

plt.savefig("rectangle1.pdf",dip=120)
plt.show()