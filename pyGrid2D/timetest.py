#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: timetest
@time: 2018/2/21  19:53
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# list comprehension and map

import time
def test(i):
    return 1+i

st = time.time()
l = [test(i) for i in xrange(10000000)]

print time.time() - st



st = time.time()
l = map(test, xrange(10000000))

print time.time() - st


# def test(f, name):
# 	st = time.time()
# 	f()
# 	print '%s %ss'%(name, time.time()-st)
#
#
# TIMES = 1000
# ARR = range(10000)
#
#
# def tmap():
# 	i = 0
# 	while (i<TIMES):
# 		map(lambda x:x, ARR)
# 		i = i+1
#
# def tlst():
# 	i = 0
# 	while (i<TIMES):
# 		[x for x in ARR]
# 		i = i+1
#
#
# test(tmap, "map")
# test(tlst, "lst")
