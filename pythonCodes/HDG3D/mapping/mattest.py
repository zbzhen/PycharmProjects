#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/23 10:52
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : mattest.py
# @version : Python 2.7.6
import numpy as np
from sympy import var,simplify
for i in range(3):
    for j in range(3):
        var(["a"+str(i)+str(j)])
        var(["b"+str(i)+str(j)])
        var(["c"+str(i)+str(j)])
A = np.array([[a00, a01], [a10, a11]])
B = np.array([[b00, b01], [b10, b11]])
C = np.array([[c00, c01], [c10, c11]])

AB_C = np.dot(np.dot(A, B), C)
A_BC = np.dot(A, np.dot(B, C))
print AB_C
print A_BC
print AB_C - AB_C