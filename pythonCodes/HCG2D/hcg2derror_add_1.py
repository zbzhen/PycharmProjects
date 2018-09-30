#!/usr/bin/env python  
#-*- coding: utf-8 -*-   
#---------------------------------------------------  
#演示MatPlotLib中设置坐标轴主刻度标签和次刻度标签.  
  
#对于次刻度显示,如果要使用默认设置只要matplotlib.pyplot.minorticks_on()  
  
#---------------------------------------------------  
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.font_manager as mft
#---------------------------------------------------  
  
xmajorLocator   = MultipleLocator(1) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%d') #设置x轴标签文本的格式
xminorLocator   = MultipleLocator(0.5) #将x轴次刻度标签设置为5的倍数
  
  
ymajorLocator   = MultipleLocator(1) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%5.1d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(0.2) #将此y轴次刻度标签设置为0.1的倍数
  

x = [0,1,2,3,4]
fig = plt.figure(figsize=(9,8), dpi=72, facecolor="white")

addmeshH_1 = [5.656e-07,4.999e-08,4.418e-09,3.905e-10,3.508e-11]

addmeshD_1 = [7.146e-07,1.169e-07,1.977e-08,3.411e-09,5.954e-10]

ax=plt.gca()

plt.xlim(-0.2, 4.2)
plt.ylim(-11,-6)



plt.plot(x,np.log(addmeshH_1)/np.log(10), "--d--",label="Rough solution meshH" , markersize=12, linestyle='solid')
plt.plot(x,np.log(addmeshD_1)/np.log(10), "--*--",label="Rough solution meshD" , markersize=12, linestyle='dashed')

plt.xlabel("Degree of add mesh density",fontsize = 20)
#plt.xlabel(r" log$_{ 2}\;({\frac{h}{h_0}})$",fontsize = 18)
#plt.xlabel("$log_{10}^{(N)}$")
#plt.ylabel("log $_{10}(L^2 $ error $)$",fontsize = 15,horizontalalignment='center')
plt.text(-0.55,-7.8,r"log $_{10}(L^2 $ error $)$",color="black",fontsize=20,ha="center",rotation ='vertical' )
#plt.ylim(1e-16, 1e-4)
myfont = mft.FontProperties(size=20)
plt.legend(prop = myfont)

  
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
plt.savefig("addhcgerror_1.pdf",dip=120)
plt.show()
#help(plt.plot)
##########################################################  