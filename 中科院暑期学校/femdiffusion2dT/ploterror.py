#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 23:56
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : ploterror.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager as mft
#-----
#x = [10, 15, 20, 25,30,35,40,50]
xmajorLocator   = MultipleLocator(1) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%d') #设置x轴标签文本的格式
# xminorLocator   = MultipleLocator() #将x轴次刻度标签设置为5的倍数


ymajorLocator   = MultipleLocator(1) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%5.1d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(0.2) #将此y轴次刻度标签设置为0.1的倍数

x = [1,2,3,4,5]
fig = plt.figure(figsize=(9,8), dpi=72, facecolor="white")

ax=plt.gca()

#ax.set_yscale("log")

#ax.set_yticks = [1e-16, 1e-13, 1e-10, 1e-7, 1e-4]
#ax.set_xticklabels(("5", "10", "15", "20", "25", "30"))
plt.xlim(-0.2+1, 4.2+1)
plt.ylim(-4, 0.8)
#plt.plot(x, hperro, label="hp-mesh")
a = 0.6
ee = [a, a/8, a/8**2, a/8**3, a/8**4]
ei = [1.2767941181632623, 0.21935798845340007, 0.029828146797621767, 0.0038089447096181757, 0.00047867391058364976]
eh = [1.248156850951234, 0.1965103332873122, 0.028488517494611728, 0.0037489738270144366, 0.0004759774821982502]

# plt.plot(x,np.log(addmeshH)/np.log(10), "--d--",label="Smooth solution meshH", markersize=12, linestyle='solid' )
# plt.plot(x,np.log(addmeshD)/np.log(10), "--*--",label="Smooth solution meshD", markersize=12, linestyle='dashed' )
plt.plot(x,np.log(ee)/np.log(10), linestyle='dashed' )
plt.plot(x,np.log(ei)/np.log(10), "--*--",label=r"$||{\bf u}-{\bf u}_I ||_{{\bf L}^2(\Omega)}$", markersize=12, linestyle='solid' )
# plt.plot(x,np.log(eh)/np.log(10), "--^--",label="$|| {\bm u} - {\bm u}_h ||_{{\bm L}^2(\Omega)}$", markersize=12, linestyle='dashed' )
plt.plot(x,np.log(eh)/np.log(10), "--^--",label=r"$||{\bf u}-{\bf u}_h ||_{{\bf L}^2(\Omega)}$", markersize=12, linestyle='solid' )

plt.xlabel("log $\\frac{1}{2}(h)$",fontsize = 20)
plt.ylabel(r"log $_{10}(L^2 $ error $)$",fontsize = 20)

ax.yaxis.set_major_locator(ymajorLocator)
ax.yaxis.set_major_formatter(ymajorFormatter)

ax.xaxis.set_major_locator(xmajorLocator)
ax.xaxis.set_major_formatter(xmajorFormatter)

#显示次刻度标签的位置,没有标签文本
#ax.xaxis.set_minor_locator(xminorLocator)
#ax.yaxis.set_minor_locator(yminorLocator)

#ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
#ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(20)

for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(20)

#plt.ylim(1e-16, 1e-4)
myfont = mft.FontProperties(size=20)
plt.legend(prop = myfont)
plt.savefig("diffusionerror.pdf",dip=120)
plt.show()
