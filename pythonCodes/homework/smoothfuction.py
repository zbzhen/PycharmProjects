#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: smoothfuction
@time: 2016-03-03 15:30
"""
from _1_Intergral_8 import Intergral_2
import  numpy as np
import matplotlib.pyplot as plt

def smoothfuc_1d(x):
    normx = x**2
    if normx < 1:
        return np.e**(1.0/(normx - 1))
    return 0*x
c = Intergral_2().guass_leg_1_comp(smoothfuc_1d, (-1, 1), m=20)

def b(g):
    def bb(x):
        def f(t):
            return g(x - t)*smoothfuc_1d(t)
        return Intergral_2().guass_leg_1_comp(f, (-4, 4), m=80)/c
    return bb

def g(x):
    return int(x)

x = np.linspace(-4, 4, 129)
z = np.zeros(len(x))
zture = np.zeros(len(x))
for ni, vi in enumerate(x):
     #z[ni] = b(g)(vi) #1times
     z[ni] = b(g)(vi)
     zture[ni] = g(vi)

plt.plot(x, z, label="smooth")
plt.plot(x, zture, "*", label="exact")
plt.grid(True)
plt.legend()
plt.show()