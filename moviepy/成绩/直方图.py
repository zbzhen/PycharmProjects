#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 18:00
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 直方图.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
from matplotlib import rcParams
fig1 = plt.figure(2)
x = (0.2,1)
y = (1,0.5)
c = ('r', 'g')
rects =plt.bar(x, y, color=c, width=0.2, align="center", yerr=0.000001)
plt.title('Pe')
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x()+rect.get_width()/2., height, '%s' % float(height), ha="center", va="bottom" )
plt.xticks(x, ('frst','second'))
plt.show()