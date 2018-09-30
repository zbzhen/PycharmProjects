# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 12:48:10 2016

@author: Administrator
"""

from _1_Intergral_8 import Intergral_2
import  numpy as np
import matplotlib.pyplot as plt


def f1(x):
    return x**2
    
def f2(x):
    return x**(0.5)

def f3(x):
    return x**(-1)
    
def f4(x):
    return x**(-0.5)
    
def f5(x):
    return 2**x

def f6(x):
    return np.log(x)/np.log(2)

def f7(x):
    return np.log(x)/np.log(0.5)




x = np.linspace(0, 1.5, 129)
plt.plot(x, f1(x), label="x^2")
plt.plot(x, f2(x), label="x^0.5")
#plt.plot(x, f3(x), label="x^(-1)")
#plt.plot(x, f4(x), label="x^(-0.5)")
#plt.plot(x, f5(x), label="2^x")
#plt.plot(x, f6(x), label="log2 x")
#plt.plot(x, f7(x), label="log0.5 x")
y1 = np.linspace(-0.5, 3, 129)
y2 = np.linspace(-0.5, 3, 129)
plt.plot(0*x, y2)
plt.plot(y1, 0*y1)
#plt.grid(True)
plt.legend()
plt.show()
plt.legend()