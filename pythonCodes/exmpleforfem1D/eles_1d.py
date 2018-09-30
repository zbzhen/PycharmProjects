#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: eles_1d
@time: 2016-05-20 15:27
"""

import numpy as np
import matplotlib.pyplot as plt
ee = 1
bl = 5 #缩放比例
#--------------------------这一步是标准区域插值与坐标变换-------------------
#插值基函数
#标准三次插值
def baseinter():
    def f(x):
        return [(3*x-1)*(3*x+1)*(x-1), (x+1)*(3*x-1)*(x-1), (x+1)*(x-1)*(3*x+1), (x+1)*(3*x+1)*(3*x-1)]
    def ff(x):
        ans = [f(x)[0]*1.0/f(-1)[0], f(x)[1]*1.0/f(-1.0/3)[1], f(x)[2]*1.0/f(1.0/3)[2], f(x)[3]*1.0/f(1)[3]]
        return np.array(ans)
    return ff

#坐标变换
def coordtransform(D, x):
    s = (2*x - (D[0]+D[-1]))*1.0/(D[-1]-D[0])
    return s

def coordtansform_v(D, s):
    x = 0.5*(D[0]+D[-1]) + 0.5*s*(D[-1]-D[0])
    return x

def putongchazhi(D, x):
    s = coordtransform(D, x)
    return baseinter()(s)

#------------------------这一步是画图--------------------------------------

plotpointpp = plt.plot([2],[bl],'bo')


#画出点以及标出编号
p = list(np.linspace(3, 9, 10))
pp = [3,5,7,9]
ap =  np.sort(list(set(p).difference(set(pp))))
plotpointp = plt.plot(pp, 0*np.array(pp),'bo')
plotpointj = plt.plot(ap, 0*ap, '*')

s = np.linspace(-1, 1, 65)

D1 = [3, 5]
D2 = [5, 7]
D3 = [7, 9]
D4 = [9, 11]
D = [D1, D2, D3, D4]
def plotinter(D, k):
    plt.plot(coordtansform_v(D, s), putongchazhi(D, coordtansform_v(D, s))[k],"r")
    return


plt.text(8,1.2,r'$y=1$',color="blue",fontsize=20,ha="center")
plt.text(3,-0.4,r'$x_{e-1}$',color="blue",fontsize=20,ha="center")
plt.text(5,-0.4,r'$x_e$',color="blue",fontsize=20,ha="center")
plt.text(7,-0.4,r'$x_{e+1}$',color="blue",fontsize=20,ha="center")
plt.text(9,-0.4,r'$x_{e+2}$',color="blue",fontsize=20,ha="center")

plotx_1 = plt.plot([0, 11], [ee, ee], "--")

plt.plot([0, 3], [0, 0], 'k')
plt.plot([9, 11], [0, 0], 'k')
plt.plot([5, 7], [0, 0], 'k')

plt.plot(D3+D1, [0, 0]*2, 'r')
#plotinter(D1, -1)
plotinter(D2, 1)
plt.plot([5+2.0/3, 5+2.0/3], [0,1], 'b--')
plt.plot([5+2.0/3], [0], 'r*')
plt.plot([5, 7], [0, 0], 'k')

plt.show()