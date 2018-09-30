#!/usr/bin/env python
# encoding: utf-8
#---------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager as mft
#---------------------------------------------------

xmajorLocator   = MultipleLocator(0.2) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%0.1f') #设置x轴标签文本的格式
xminorLocator   = MultipleLocator(0.5) #将x轴次刻度标签设置为5的倍数


ymajorLocator   = MultipleLocator(1) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%0.1d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(0.2) #将此y轴次刻度标签设置为0.1的倍数

x = [4,8,12,16,20,24,28]
x = np.log(x)/np.log(10)
fig = plt.figure(figsize=(9,8), dpi=72, facecolor="white")
meshR = [6.636e-05,2.052e-07,1.039e-08,1.31e-09,2.661e-10,7.283e-11,2.387e-11]
meshT = [4.585e-05,1.852e-07,9.789e-09,1.254e-09,2.57e-10,7.074e-11,2.387e-11]
meshH = [6.843e-05,2.052e-07,1.039e-08,1.31e-09,2.661e-10,7.283e-11,2.447e-11]
meshD = [3.101e-05,3.278e-07,3.439e-08,7.413e-09,2.307e-09,8.981e-10,4.068e-10]
#meshS = [0.0001293,6.67e-07,3.845e-08,5.203e-09,1.109e-09,3.147e-10,1.086e-10]
meshTDuffy = [0.0004533, 5.609e-07, 3.113e-08, 4.324e-09, 9.566e-10,2.813e-10, 1.004e-10]
ax=plt.gca()

plt.xlim(0.5, 1.6)
plt.ylim( -11,-3)

plt.plot(x,np.log(meshR)/np.log(10), "--s--",label="meshR", markersize=12, linestyle='dashed' )
plt.plot(x,np.log(meshT)/np.log(10), "--v--",label="meshT", markersize=12, linestyle='solid')
plt.plot(x,np.log(meshTDuffy)/np.log(10), "--^--",label="meshTDuffy", markersize=12, linestyle='solid')
plt.plot(x,np.log(meshH)/np.log(10), "--d--",label="meshH", markersize=12, linestyle='solid' )
plt.plot(x,np.log(meshD)/np.log(10), "--*--",label="meshD", markersize=12, linestyle='dashed' )


#plt.text(1,-6,r"log $_{10}(L^2 $ error $)$",color="black",fontsize=18,ha="center",rotation ='vertical' )


plt.xlabel(r"log $_{10}(N)$",fontsize = 20)
plt.text(0.4,-6.0,r"log $_{10}(L^2 $ error $)$",color="black",fontsize=20,ha="center",rotation ='vertical' )


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
plt.savefig("hcgerror_1.pdf",dip=120)
plt.show()

