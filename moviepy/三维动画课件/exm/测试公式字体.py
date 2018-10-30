#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 19:40
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 测试公式字体.py
# @version : Python 2.7.6
import numpy as np
from mayavi import mlab
from pointLinePlane import spaceElement, Frame, Axis, getcubepoints, setSCALING
import matplotlib.pyplot as plt
from matplotlib import mathtext
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei', "FangSong"][-1]


love = np.loadtxt("love5151.data")
# plt.imshow(love)
# plt.show()



figure =mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
mlab.clf()

parser = mathtext.MathTextParser("bitmap")
tmp,x = parser.to_mask('zhen_love_', dpi=200, fontsize=20)
tmp = np.where(tmp>0,2,0)


# tb,x = parser.to_mask(u'几何图霸', dpi=200, fontsize=20)
# tb = np.where(tb>0,2,0)

# print s,t
# tmp = np.array(tmp,dtype=int)
# np.savetxt("22.data", tmp, fmt='%d')

s,t = np.shape(tmp)
s1,t1 = np.shape(love)
# s2,t2 = np.shape(tb)
ps = getcubepoints(L=[0,0,0], R=[2,2,2])
a = [spaceElement(p) for p in ps]
Frame(a[:4], a[4:]).plot(linesize=0.03)
a0167 = spaceElement(a[0],a[1],a[6],a[7])
mx = 100
my = 50
def cf(x):
    ans = x
    ans[mx:mx+s, my:my+t] += tmp*0.01
    ans[mx:mx+s1, my+t:my+t+t1] += love*0.01
    # ans[mx+s1+20:mx+s1+20+s2, my*2:my*2+t2] += tb*0.01
    return ans
a0167.plot(colormap="Spectral", opacity=0.8, scalarsfunction=cf, num=400)
mlab.show()