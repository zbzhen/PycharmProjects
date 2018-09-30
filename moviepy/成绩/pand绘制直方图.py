#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 22:03
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : pand绘制直方图.py
# @version : Python 2.7.6
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
# https://blog.csdn.net/xiaomuworld/article/details/52057804


# dates = pd.date_range('20190101', periods=6)
# df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
# df.to_excel('foo.xlsx', sheet_name='Sheet1')
df = pd.read_excel('test.xlsx', sheet_name='Sheet1')
# print df.head()
# print df.tail(3)
# print df.index
# print df.columns
# print df.values
# print df.sort_index(axis=1, ascending=False)
# print df.sort_values(by='C')
# print df.loc['20190102':'20190104', 'A':'B']
# print df.iloc[3:5,0:2]
# df.loc[:,'D'] = np.array([5] * len(df))
# df.iat[0,1] = 0
# df1 = df.reindex(index=df.index[1:5], columns=list(df.columns) + ['E'])
# df1.loc[df.index[0]:df.index[1],'E'] = 1
df1 = df.copy()
# df1.insert(0, 'e', 'NaN')

df1.insert(1,'e',df1['a'])

# dd = df1.columns.tolist()
# df1.reindex(columns=dd.insert(3,"F"))
# df1.drop(['B','C'], axis=1, inplace=True)
df1.drop(['b','c'], axis=1, inplace=True)
# df1 = df1[df1.A<0]
# print df1
# print df1.mean(1)
ct = df['a'].value_counts()
# df1['a'].hist(bins=100,histtype="bar",normed=1,alpha=0.6).get_figure().savefig("test.png")

datalist = df['a']
max = datalist.max()
min = datalist.min()
elelen = 3   # 单元长度
ct = (max/elelen - min/elelen) + 1
tmp = [0]*ct
for i in datalist:
    for j in range(ct):
        if min/elelen*elelen+j*elelen <= i < min/elelen*elelen+elelen*(j+1):
            tmp[j] += 1
plt.figure('This is a test')
x = [min/elelen*elelen+j*elelen*0.5 for j in range(1,ct+1)]
rects =plt.bar(x, tmp, width=elelen*0.5, align="center", yerr=0)
for rect in rects:
    height = rect.get_height()
    if height != 0:
        plt.text(rect.get_x()+rect.get_width()/2., height, '%s' % int(height), ha="center", va="bottom" )
xtext = ["[" + str(min/elelen*elelen+j*elelen)+','+str(min/elelen*elelen+elelen*(j+1))+')' for j in range(ct)]
plt.xticks(x, xtext)
plt.show()