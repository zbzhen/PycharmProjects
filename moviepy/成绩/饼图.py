#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 18:07
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 饼图.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
plt.subplots(1,figsize=(6,6), facecolor='white')
lb = ['e', 'f', 'g']
sizes = [30,40,50]
color = ['b', 'g', 'r']
explode = [0.1,0.2,0.3]
plt.pie(sizes, explode=explode, labels=lb, autopct='%1.1f%%', colors=color, shadow=True, startangle=100)
plt.axis('equal')
plt.show()