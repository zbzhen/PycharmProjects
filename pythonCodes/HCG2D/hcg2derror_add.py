#!/usr/bin/env python
# encoding: utf-8
#---------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager as mft
#-----
#x = [10, 15, 20, 25,30,35,40,50]
xmajorLocator   = MultipleLocator(1) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%d') #设置x轴标签文本的格式
xminorLocator   = MultipleLocator(0.5) #将x轴次刻度标签设置为5的倍数


ymajorLocator   = MultipleLocator(1) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%5.1d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(0.2) #将此y轴次刻度标签设置为0.1的倍数

x = [0,1,2,3,4]
fig = plt.figure(figsize=(9,8), dpi=72, facecolor="white")

#这个数据是k=7，
addmeshH = [0.000752,1.313e-05,8.632e-08,6.8e-10,5.317e-12]
addmeshH_1 = [5.656e-07,4.999e-08,4.418e-09,3.905e-10,3.508e-11]

addmeshD = [0.0004244,9.956e-06,6.96e-08,5.471e-10,4.315e-12]
addmeshD_1 = [7.146e-07,1.169e-07,1.977e-08,3.411e-09,5.954e-10]


ax=plt.gca()

#ax.set_yscale("log")

#ax.set_yticks = [1e-16, 1e-13, 1e-10, 1e-7, 1e-4]
#ax.set_xticklabels(("5", "10", "15", "20", "25", "30"))
plt.xlim(-0.2, 4.2)
plt.ylim(-12, -2.6)
#plt.plot(x, hperro, label="hp-mesh")

plt.plot(x,np.log(addmeshH)/np.log(10), "--d--",label="Smooth solution meshH", markersize=12, linestyle='solid' )
plt.plot(x,np.log(addmeshD)/np.log(10), "--*--",label="Smooth solution meshD", markersize=12, linestyle='dashed' )

plt.xlabel("Degree of add mesh density",fontsize = 20)
plt.text(-0.59,-6.8,r"log $_{10}(L^2 $ error $)$",color="black",fontsize=20,ha="center",rotation ='vertical' )

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

#plt.ylim(1e-16, 1e-4)
myfont = mft.FontProperties(size=20)
plt.legend(prop = myfont)
plt.savefig("addhcgerror.pdf",dip=120)
plt.show()
