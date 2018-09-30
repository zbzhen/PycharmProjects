#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: qr1
@time: 2018/7/10  10:22
"""
import numpy as np

a = np.array([[2, 1j], [1j, 3]])
print np.linalg.eig(a)
help(np.linalg.qr)
