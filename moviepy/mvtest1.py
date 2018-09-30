#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mvtest1
@time: 2017/12/23  22:16
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
fig = plt.figure()
axes1 = fig.add_subplot(111)
line, = axes1.plot(np.random.rand(10))
#因为update的参数是调用函数data_gen,
#所以第一个默认参数不能是framenum
def update(data):
  line.set_ydata(data)
  return line,
# 每次生成10个随机数据
def data_gen():
  while True:
    yield np.random.rand(10)
ani = animation.FuncAnimation(fig, update, data_gen, interval=2*1000)
plt.show()