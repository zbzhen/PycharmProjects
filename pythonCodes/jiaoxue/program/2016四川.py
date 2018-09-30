#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 2016四川
@time: 2016-09-08 17:38
"""
#输入n, v
n = 3
x = 2


v = 1
i = n - 1
while i >=  0:
    v = v*x+i
    i = i-1
    print "i=", i
    print "v=", v
    print "____________________"
print "最后的答案是",v