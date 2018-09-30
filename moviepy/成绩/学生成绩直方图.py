#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 19:37
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 学生成绩直方图.py
# @version : Python 2.7.6
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

sheet1name = u'7'
df = pd.read_excel(u'test测试.xlsx', sheet_name=sheet1name)
elelen = 10   # 单元长度



ct = df[u'成绩'].value_counts()
datalist = df[u'成绩']
max = datalist.max()
min = datalist.min()

ct = (max/elelen - min/elelen) + 1
tmp = [0]*ct
for i in datalist:
    for j in range(ct):
        if min/elelen*elelen+j*elelen <= i < min/elelen*elelen+elelen*(j+1):
            tmp[j] += 1
plt.figure()
avrenge = datalist.sum()*1.0/len(datalist)
plt.xlabel(sheet1name + u"班数学成绩直方图（平均分:"+str(round(avrenge, 2))+u"）", fontsize=20)
# import time
# date = time.strftime('%Y.%m.%d',time.localtime(time.time()))
# plt.ylabel(date, fontsize=20)

x = [min/elelen*elelen+j*elelen*0.5 for j in range(1,ct+1)]
rects =plt.bar(x, tmp, width=elelen*0.5, align="center", yerr=0)
for rect in rects:
    height = rect.get_height()
    if height != 0:
        plt.text(rect.get_x()+rect.get_width()/2., height, '%s' % int(height), ha="center", va="bottom", fontsize=20)
xtext = ["[" + str(min/elelen*elelen+j*elelen)+','+str(min/elelen*elelen+elelen*(j+1))+')' for j in range(ct)]
plt.xticks(x, xtext, fontsize=15)
plt.yticks(fontsize=20)
plt.savefig(sheet1name + u"班.png")
plt.show()
