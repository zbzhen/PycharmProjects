#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: zuobiaobianhuan
@time: 2017-01-22 22:37
"""
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,8), dpi=72, facecolor="white")
#设置坐标轴的范围
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)

#画出坐标轴
xieta = np.array([-0.2, 0.4])
# plt.annotate("",(1.4,0),(-1.4,0),arrowprops={"arrowstyle": "->"},color="black")
# plt.annotate("",(0,1.4),(0,-1.4),arrowprops={"arrowstyle": "->"},color="black")
plt.plot([-1,1,1,-1,-1],[-1,-1,1,1,-1],color="black")
plt.text(-1.2-0.1,-1.2,"$\widehat{V}_1(-1,-1)$",fontsize = 20)
plt.text(-1.2-0.1,1.03+0.05,"$\widehat{V}_4(-1, 1)$",fontsize = 20)
plt.text(1.03-0.3,-1.2,"$\widehat{V}_2( 1,-1)$",fontsize = 20)
plt.text(1.03-0.3,1.03+0.05,"$\widehat{V}_3( 1, 1)$",fontsize = 20)
plt.text(-0.1, 0.18,"$\widehat{V}( \\xi, \\eta)$",fontsize = 20)

plt.plot(xieta[0], -1, 'bo')
plt.plot(xieta[0],  1, 'bo')
plt.plot(-1,  xieta[1], 'bo')
plt.plot( 1,  xieta[1], 'bo')
plt.plot(xieta[0],  xieta[1], 'bo')
plt.plot([xieta[0],xieta[0]], [-1, 1],"--")
plt.plot([-1, 1], [xieta[1],xieta[1]], "--")

# plt.text(1.03,-0.13,"$1$",fontsize = 20)
# plt.text(1.33,-0.13,'$ \\xi $',fontsize = 20)
# plt.text(-1.03+0.06,-0.13,"$-1$",fontsize = 20)
# plt.text(0.03,-1.13,"$-1$",fontsize = 20)
# plt.text(0.03,1.13-0.26,"$1$",fontsize = 20)
# plt.text(0.03,1.53-0.26,"$\eta$",fontsize = 20)
plt.savefig("box2d.pdf",dip=120)
plt.show()
