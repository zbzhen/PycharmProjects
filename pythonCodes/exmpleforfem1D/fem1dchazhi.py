#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: fem1dchazhi
@time: 2016-05-20 14:42
"""


import numpy as np
import matplotlib.pyplot as plt
#设置坐标轴的范围
plt.xlim(-2.5,1.7)
plt.ylim(-0.7,1.5)

#画出坐标轴和箭头

#plotx = plt.plot([-1.2,1.2], [0,0],"k")
#ploty = plt.plot([-0.2,-0.2], [-0.5, 1.2],"k")

plotx_1 = plt.plot([-2.2,1.5], [1,1],"--")
#箭头
plt.annotate("",(-2.2,0),(1.5,0),arrowprops={"arrowstyle": "<-"})
plt.annotate("",(-2,-0.5),(-2,1.2),arrowprops={"arrowstyle": "<-"})


#画出点以及标出数字
plt.plot([-1,1],[0,0],'bo')
plt.plot([-1.0/3,1.0/3],[0,0],'*')
plt.plot([0-2],[1],'bo')


plt.text(-1,-0.1,r'$x_e$',color="blue",fontsize=20,ha="center")
#plt.text(-0.333,-0.1,r'$P^e_1$',color="blue",fontsize=20,ha="center")
#plt.text(0.333,-0.1,r'$P^e_2$',color="blue",fontsize=20,ha="center")
plt.text(1,-0.1,r'$x_{e+1}$',color="blue",fontsize=20,ha="center")

plt.text(0.07-2,0.85,r'$1$',color="blue",fontsize=20,ha="center")



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

plt.annotate(r"$\varphi^e_1(x)$",(0.03,0.48),(0.2,0.7),fontsize = 20,arrowprops={"arrowstyle": "->"})
plt.annotate(r"$\varphi^e_0(x)$",(0.68,0.08),(0.8,0.3),fontsize = 20,arrowprops={"arrowstyle": "->"})



#plt.legend()
plt.savefig("putongjihanshu.pdf",dip=120)
plt.show()