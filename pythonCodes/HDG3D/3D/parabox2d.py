#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: parabox2d
@time: 2017-01-23 10:34
"""
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-0,1.)
plt.ylim(-0,1.)

#画出坐标轴

# plt.annotate("",(1.3,0),(-0.1,0),arrowprops={"arrowstyle": "->"},color="black",fontsize = 20)
# plt.annotate("",(0,1.3),(0,-0.1),arrowprops={"arrowstyle": "->"},color="black",fontsize = 20)
t=0
def mapping1D(a, b):
    return lambda x: 0.5*(b-a)*x + 0.5*(b+a)
plt.plot([0.2,0.7,0.9,0.3,0.2], [0.4,0.2,0.6,0.9,0.4])
x = np.array([0.2,0.7,0.9,0.3])
y = np.array([0.4,0.2,0.6,0.9])
xy = np.array([x, y]).T
xieta = np.array([-0.2, 0.4])
eetad = mapping1D(xy[0], xy[1])(xieta[0])
eetap = mapping1D(xy[3], xy[2])(xieta[0])
exid = mapping1D(xy[0], xy[3])(xieta[1])
exip = mapping1D(xy[1], xy[2])(xieta[1])

plt.text(0.16,0.35,'$ V_1 $',fontsize = 20)
plt.text(0.7,0.14,'$ V_2 $',fontsize = 20)
plt.text(0.9,0.61,'$ V_3 $',fontsize = 20)
plt.text(0.24,0.895,'$ V_4 $',fontsize = 20)


plt.text(0.53,0.65,'$  V $',fontsize = 20)
plt.text(0.37,0.26,'$ E_\\eta^- $',fontsize = 20)
plt.text(0.54,0.8,'$ E_\\eta^+ $',fontsize = 20)
plt.text(0.85,0.42,'$ E_\\xi^+ $',fontsize = 20)
plt.text(0.19,0.74,'$ E_\\xi^- $',fontsize = 20)




plt.plot(0.497, 0.6442, 'bo')
plt.plot(eetad[0], eetad[1], 'bo')
plt.plot(eetap[0], eetap[1], 'bo')
plt.plot(exid[0], exid[1], 'bo')
plt.plot(exip[0], exip[1], 'bo')
plt.plot([eetad[0],eetap[0]], [eetad[1], eetap[1]],"--")
plt.plot([exid[0],exip[0]], [exid[1], exip[1]],"--")
# plt.text(1.26,-0.08,'$ x$',fontsize = 20)
# plt.text(0.03,1.53-0.26,"$y $",fontsize = 20)

plt.savefig("parabox2d.pdf",dip=120)
plt.show()