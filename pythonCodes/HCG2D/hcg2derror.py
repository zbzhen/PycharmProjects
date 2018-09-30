#!/usr/bin/env python
# encoding: utf-8
#---------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager as mft
#---------------------------------------------------

xmajorLocator   = MultipleLocator(4) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%d') #设置x轴标签文本的格式
xminorLocator   = MultipleLocator(0.5) #将x轴次刻度标签设置为5的倍数


ymajorLocator   = MultipleLocator(4) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%5.1d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(0.2) #将此y轴次刻度标签设置为0.1的倍数

x = [4,8,12,16,20,24]
fig = plt.figure(figsize=(9,8), dpi=72, facecolor="white")
meshR = [0.01375,6.508e-06,1.423e-09,1.188e-13,6.493e-15,1.902e-15]
meshT = [0.007491,2.248e-06,5.311e-10,4.93e-14,6.547e-14,6.773e-14]
meshH = [0.09972,0.0002325,9.616e-08,6.695e-11,2.053e-14,9.434e-15]
meshD = [0.1134,0.0002159,8.813e-08,6.843e-12,1.429e-13,1.492e-13]
meshTDuffy = [0.02335,1.335e-05,5.009e-09,9.206e-13,8.497e-15,1.176e-14]
#meshS = [0.01541,5.842e-06,5.475e-09,5.773e-13,3.436e-15,4.413e-15]

ax=plt.gca()
ax.set_xticks = [4,8,12,16,20,24]
#ax.set_yscale("log")
#ax.set_yticks = [1e-16, 1e-13, 1e-10, 1e-7, 1e-4]
#ax.set_xticklabels(("5", "10", "15", "20", "25", "30"))
plt.xlim(3, 25)
plt.ylim(-16, 0)
#plt.plot(x, hperro, label="hp-mesh")
plt.plot(x,np.log(meshR)/np.log(10), "--s--",label="meshR", markersize=12, linestyle='dashed' )
plt.plot(x,np.log(meshT)/np.log(10), "--v--",label="meshT", markersize=12, linestyle='solid')
plt.plot(x,np.log(meshTDuffy)/np.log(10), "--^--",label="meshTDuffy", markersize=12, linestyle='solid')
plt.plot(x,np.log(meshH)/np.log(10), "--d--",label="meshH", markersize=12, linestyle='solid' )
plt.plot(x,np.log(meshD)/np.log(10), "--*--",label="meshD", markersize=12, linestyle='dashed' )

plt.xlabel("N",fontsize = 20)
plt.text(1,-6,r"log $_{10}(L^2 $ error $)$",color="black",fontsize=20,ha="center",rotation ='vertical' )


#设置主刻度标签的位置,标签文本的格式
ax.xaxis.set_major_locator(xmajorLocator)
ax.xaxis.set_major_formatter(xmajorFormatter)

ax.yaxis.set_major_locator(ymajorLocator)
ax.yaxis.set_major_formatter(ymajorFormatter)

#显示次刻度标签的位置,没有标签文本
#ax.xaxis.set_minor_locator(xminorLocator)
#ax.yaxis.set_minor_locator(yminorLocator)

#ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
#ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(20)

for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(20)
myfont = mft.FontProperties(size=20)
plt.legend(prop = myfont)
plt.savefig("hcgerror.pdf",dip=120)
plt.show()
