#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 9:06
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : eg.py
# @version : Python 2.7.6
import numpy as np
a = np.array([0,1])
b = np.array([2,2])
print np.vstack((a,b))
print a.tolist()+b.tolist()