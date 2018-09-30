#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/22 19:40
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : plotK1K2.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt

#设置坐标轴的范围
plt.xlim(-1,5)
plt.ylim(-1,4)

#画两个三角形
plt.plot([2,0,2.5],[3,0,-0.5],"b")
plt.plot([2.5,4,2],[-0.5,1,3],"g")

plt.plot([2,2.5],[3,-0.5],"r", linewidth=8)

# plotpoint1 = plt.plot([2.18],[1.5],'bo')
# plotpoint = plt.plot([2.35],[0.3],'*')
# plotpoint = plt.plot([2.42],[0.31],'bo')
# plt.text(1.95,1.4,r'$x^e_j$',color="blue",fontsize=20,ha="center")
# plt.text(2.15,0.27,r'$x^e_{i}$',color="blue",fontsize=20,ha="center")
# plt.text(2.67,0.28,r"$x^{e'}_{i'}$",color="green",fontsize=20,ha="center")

plt.annotate(r'$\Sigma$',(2.1,2.2),(3,3),fontsize=20,arrowprops={"arrowstyle": "->"},color="red")
plt.text(1.3,0.8,r'$K_1$',color="blue",fontsize=20,ha="center")
plt.text(3,1,r"$K_2$",color="green",fontsize=20,ha="center")
plt.savefig("K1K2.pdf",dip=120)
plt.show()