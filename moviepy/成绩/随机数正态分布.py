#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1 22:43
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 随机数正态分布.py
# @version : Python 2.7.6
import numpy as np
from matplotlib import pyplot as plt
fig,ax=plt.subplots()

np.random.seed(4) #设置随机数种子
Gaussian=np.random.normal(0,1,1000) #创建一组平均数为0，标准差为1，总个数为1000的符合标准正态分布的数据
# ax.hist(Gaussian,bins=200,histtype="stepfilled",normed=True,alpha=0.6)
ax.hist(Gaussian,bins=25,histtype="bar",normed=True,alpha=0.6)

plt.show()
