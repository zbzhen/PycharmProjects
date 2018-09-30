#!/usr/bin/env python
# encoding: utf-8
#---------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager as mft
#---------------------------------------------------

xmajorLocator   = MultipleLocator(1) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%0.1d') #设置x轴标签文本的格式
xminorLocator   = MultipleLocator(0.5) #将x轴次刻度标签设置为5的倍数


ymajorLocator   = MultipleLocator(1) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%0.1d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(0.2) #将此y轴次刻度标签设置为0.1的倍数



x = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
x = np.array(x)
x = 2.0/x
x = np.log(x)/np.log(10)

#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－plt.figure(figsize=(9,8), dpi=72, facecolor="white")
I1error = [0.001794, 0.0004415, 0.0001093, 2.731e-05, 6.809e-06, 1.702e-06, 4.253e-07,1.063e-07, 2.658e-08, 6.645e-09, 1.661e-09]
H1error = [0.00321, 0.0008942, 0.0002454, 5.748e-05, 1.468e-05, 3.666e-06, 7.953e-07,1.989e-07, 5.064e-08, 1.364e-08, 3.756e-09]
Hinf1error = [0.006934, 0.002184, 0.0006145, 0.0001524, 3.915e-05, 9.894e-06, 1.959e-06,4.932e-07, 1.326e-07, 3.702e-08, 1.013e-08]
I1error = np.log(I1error)/np.log(10)
H1error = np.log(H1error)/np.log(10)
Hinf1error = np.log(Hinf1error)/np.log(10)
ax=plt.gca()
#ax.set_xticks = [3, 4, 5, 6, 7]
plt.xlim(-4, -0.8)
plt.ylim(-9, -2)

plt.plot(x,Hinf1error, "--*--",label="$L^\infty$error", markersize=10, linestyle='dashed' )
plt.plot(x,H1error, "--s--",label="$L^2$error", markersize=10, linestyle='solid' )



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


plt.ylabel("log$_{10}($error$)$",fontsize = 20)
plt.xlabel(r"log$_{10}(h)$",fontsize = 20)
myfont = mft.FontProperties(size=20)
plt.legend(loc='lower right',prop = myfont)
plt.savefig("newerror1D_3_52.pdf",dip=120)
plt.show()
