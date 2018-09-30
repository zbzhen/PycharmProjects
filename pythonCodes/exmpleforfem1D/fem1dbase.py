# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:24:07 2016

@author: Administrator
"""


import numpy as np
import matplotlib.pyplot as plt

#设置坐标轴的范围
plt.xlim(-1.5,1.5)
plt.ylim(-0.7,1.5)

#画出坐标轴

plotx = plt.plot([-1.2,1.2], [0,0],"k")
ploty = plt.plot([0,0], [-0.5, 1.2],"k")

plotx_1 = plt.plot([-1.2,1.2], [1,1],"--")
#箭头
plt.annotate("",(1.201,0),(1.2,0),arrowprops={"arrowstyle": "->"})
plt.annotate("",(0,1.21),(0,1.2),arrowprops={"arrowstyle": "->"})


#画出点以及标出数字
plotpoint = plt.plot([-1,1],[0,0],'bo')
plotpoint = plt.plot([-1.0/3,1.0/3],[0,0],'*')
plotpoint1 = plt.plot([0],[1],'bo')


plt.text(-1,-0.2,r'$-1$',color="blue",fontsize=20,ha="center")
plt.text(-0.333,-0.2,r'$-\frac{1}{3}$',color="blue",fontsize=20,ha="center")
plt.text(0.333,-0.2,r'$\frac{1}{3}$',color="blue",fontsize=20,ha="center")
plt.text(1,-0.2,r'$1$',color="blue",fontsize=20,ha="center")

plt.text(0.07,0.85,r'$1$',color="blue",fontsize=20,ha="center")



def f1(x):
    return (x-1.0/3)*(x+1.0/3)*(x-1)
    
def f2(x):
    return (x+1)*(3*x-1)*(x-1)
    
def f3(x):
    return (x+1)*(x-1)*(x+1.0/3)

def f4(x):
    return (x+1)*(x+1.0/3)*(x-1.0/3)
    


x = np.linspace(-1, 1, 20*3+1)
#y1 = (x-1.0/3)*(x+1.0/3)*(x-1)*(-9.0)/16
y1 = f1(x)/f1(-1)
y2 = f2(x)*9.0/16
y3 = f3(x)/f3(1.0/3)
y4 = f4(x)/f4(1)

#r"$\varphi_0(x)$"   r"$\varphi_1(x)$"
plt.plot(x, y1, "r",label = r"$\hat{\varphi_0}(x)$")
plt.plot([-1,-1],[0,1],"--")
plt.plot(x, y2, "c", label = r"$\hat{\varphi_1}(x)$")
plt.plot([-1.0/3,-1.0/3],[0,1],"--")

plt.annotate(r"$\widehat\varphi_1(x)$",(0.03,0.48),(0.2,0.7),fontsize = 20,arrowprops={"arrowstyle": "->"})
plt.annotate(r"$\widehat\varphi_0(x)$",(0.68,0.08),(0.8,0.3),fontsize = 20,arrowprops={"arrowstyle": "->"})



#plt.legend()
plt.savefig("biaozhunjihanshu.pdf",dip=120)
plt.show()

#plt.savefig("jihanshu.pdf",dip=120)