#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 2015新课标2
@time: 2016-09-08 19:15
"""
#这个其实就是求两个数的最大公约数
a = 14
b = 18

while a != b:
    if a > b:
        a = a - b
    else:
        b = b - a
print a