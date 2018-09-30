#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 2016天津
@time: 2016-09-08 18:25
"""
s = 4
n = 1



while n <= 3:
    if s >= 6:
        s = s - 6
    else:
        s = 2*s
    n = n + 1
print s