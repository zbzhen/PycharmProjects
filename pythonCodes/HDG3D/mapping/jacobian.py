#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/24 10:55
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : jacobian.py
# @version : Python 2.7.6

import numpy as np
from sympy import var, simplify, factor, expand, diff, Matrix

var(['z'+str(i) for i in range(4)])

z = np.array([z0, z1, z2])
zz = z0*z0 + z1*z1 + z2*z2
y = z/zz




jamatrix = Matrix([[diff(y[0], z[0]),diff(y[0], z[1]),diff(y[0], z[2])],
                   [diff(y[1], z[0]),diff(y[1], z[1]),diff(y[1], z[2])],
                   [diff(y[2], z[0]),diff(y[2], z[1]),diff(y[2], z[2])]])
ja = jamatrix.det()
print(simplify(ja))
jamu = (z0**6 + 3*z0**4*z1**2 + 3*z0**4*z2**2 + 3*z0**2*z1**4 + 6*z0**2*z1**2*z2**2 + 3*z0**2*z2**4 + z1**6 + 3*z1**4*z2**2 + 3*z1**2*z2**4 + z2**6)
print factor(simplify(jamu))
print simplify(ja*zz*zz*zz)

z = np.array([z0, z1, z2, z3])
zz = z0*z0 + z1*z1 + z2*z2 + z3*z3
y = z/zz




jamatrix = Matrix([[diff(y[0], z[0]), diff(y[0], z[1]), diff(y[0], z[2]), diff(y[0], z[3])],
                   [diff(y[1], z[0]), diff(y[1], z[1]), diff(y[1], z[2]), diff(y[1], z[3])],
                   [diff(y[2], z[0]), diff(y[2], z[1]), diff(y[2], z[2]), diff(y[2], z[3])],
                   [diff(y[3], z[0]), diff(y[3], z[1]), diff(y[3], z[2]), diff(y[3], z[3])]])
ja = jamatrix.det()
print factor(1/simplify(ja))
# jamu = (z0**6 + 3*z0**4*z1**2 + 3*z0**4*z2**2 + 3*z0**2*z1**4 + 6*z0**2*z1**2*z2**2 + 3*z0**2*z2**4 + z1**6 + 3*z1**4*z2**2 + 3*z1**2*z2**4 + z2**6)
# print factor(simplify(jamu))
# print simplify(ja*zz*zz*zz)
