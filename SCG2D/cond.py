#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: cond
@time: 2018/7/2  19:30
"""
import numpy as np
m = np.loadtxt("SMGM.dat")
print np.linalg.cond(m)