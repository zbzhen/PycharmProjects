# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:24:07 2016

@author: Administrator
"""


import numpy as np
import matplotlib.pyplot as plt
#设置坐标轴的范围
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)

plt.text(1.1,-1,r'$A$',color="blue",fontsize=20,ha="center")
plt.text(0.6,0,r'$B$',color="blue",fontsize=20,ha="center")
plt.text(0.1,1,r'$C$',color="blue",fontsize=20,ha="center")
plt.text(0.6,-0.6,r'$\Gamma_{-}$',color="blue",fontsize=20,ha="center")
plt.text(0.1,0.4,r'$\Gamma_{+}$',color="blue",fontsize=20,ha="center")
"""
plt.text(-1,-1.2,r'$\widehat{A}$',color="blue",fontsize=20,ha="center")
plt.text(0,-1.2,r'$\widehat{B}$',color="blue",fontsize=20,ha="center")
plt.text(1,-1.2,r'$\widehat{C}$',color="blue",fontsize=20,ha="center")
plt.text(-0.5,-0.9,r'$\widehat{\Gamma}_{-}$',color="blue",fontsize=20,ha="center")
plt.text(0.5,-0.9,r'$\widehat{\Gamma}_{+}$',color="blue",fontsize=20,ha="center")
"""

#画出点以及标出数字
plotpoint = plt.plot([1, 0.5, 0],[-1,0,1],'bo')
#plotpoint1 = plt.plot([0],[1],'bo')


Tx=[-1, 1, 0, -1]
Ty=[-1, -1, 1, -1]
plt.plot(Tx, Ty, "r")
"""
Rx=[-1, 1, 1, -1, -1]
Ry=[-1, -1, 1, 1, -1]
plt.plot(Rx, Ry, "c")
"""

plt.savefig("triangle0.pdf",dip=120)
plt.show()