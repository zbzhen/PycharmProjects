#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 2016北京
@time: 2016-09-08 19:03
"""
a = 1
k = 0
b = a

a = -1.0/(1+a)
print "第一次计算出a的值,a=",a

print "开始进入循环"
print "_____________________"
while b != a:
        k = k+1
        a = -1.0/(1+a)
        print "k=",k
        print "a=",a
        print "_____________________"
print "循环结束，输出k="
print k