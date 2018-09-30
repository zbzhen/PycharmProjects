#!/usr/bin/env python
# encoding: utf-8
# ---------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager as mft
# ---------------------------------------------------

xmajorLocator   = MultipleLocator(1) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%d') #设置x轴标签文本的格式
xminorLocator   = MultipleLocator(0.5) #将x轴次刻度标签设置为5的倍数


ymajorLocator   = MultipleLocator(1) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%5.1d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(0.2) #将此y轴次刻度标签设置为0.1的倍数

x = [8,16,32,64,128]
fig = plt.figure(figsize=(9,8), dpi=72, facecolor="white")
meshR = [7.0742198e-06,2.4835130e-07,1.0616374e-08,5.3321964e-10,2.9647442e-11]
meshT = [5.6494939e-06,2.1887560e-07,9.9083284e-09,5.1418885e-10 ,2.9099095e-11 ]
meshH = [1.2105065e-05,6.0065204e-07,3.2192107e-08,1.8443941e-09,1.1009150e-10]
meshD = [0.1134,0.0002159,8.813e-08,6.843e-12,1.429e-13,1.492e-13]
#meshS = [0.01541,5.842e-06,5.475e-09,5.773e-13,3.436e-15,4.413e-15]
x = np.log(x)/np.log(2)

ax=plt.gca()
#ax.set_xticks = [8,16,32,64,128]
#ax.set_yscale("log")
#ax.set_yticks = [1e-16, 1e-13, 1e-10, 1e-7, 1e-4]
#ax.set_xticklabels(("5", "10", "15", "20", "25", "30"))
plt.xlim(2.8, 7.2)
plt.ylim(-11, -4.5)
#plt.plot(x, hperro, label="hp-mesh")
myfont = mft.FontProperties(size=20)
plt.plot(x,np.log(meshR)/np.log(10), "--s--",label=r"$\epsilon=0,\;\sigma^0=1$", markersize=14, linestyle='dashed' )
plt.plot(x,np.log(meshT)/np.log(10), "--v--",label=r"$\epsilon=1,\;\sigma^0=1$", markersize=14, linestyle='dashed')
plt.plot(x,np.log(meshH)/np.log(10), "--d--",label=r"$\epsilon=1,\;\sigma^0=0$", markersize=14, linestyle='dashed' )
#plt.plot(x,np.log(meshD)/np.log(10), "--*--",label="meshD", markersize=14, linestyle='dashed' )

plt.xlabel(r"log $_{\frac{1}{2}}{\;h}$",fontproperties=myfont)
#plt.ylabel(r"log $_{\frac{1}{2}}{\;h}$",fontproperties=myfont,rotation ='vertical')
plt.text(2.4,-7,r"log $_{10}(L^2 $ error $)$",color="black",fontproperties=myfont,ha="center",rotation ='vertical' )
#plt.text(5,-12,r"log $_{\frac{1}{2}}{\;h}$",fontproperties=myfont )


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
plt.legend(prop = myfont)
plt.savefig("DG1Drror.pdf",dip=120)
plt.show()
