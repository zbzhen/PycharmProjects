#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: readfile
@time: 2018/6/19  16:14
"""
import numpy as np
f = np.loadtxt("11.dat", int, skiprows=4, comments="#", usecols=range(3))
print f