#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: TTheta3D
@time: 2018/6/19  18:17
"""
from sympy import*
import numpy as np
var("x,y,z")
var("xi,eta,zeta")
var(["e_"+str(i) for i in range(5)])
var(["f_"+str(i) for i in range(5)])

def cubeToT(xHat, p):
    v0=-(xHat[0]-1.0)*(xHat[1]-1.0)*(xHat[2]-1.0)
    v1=(xHat[0]+1.0)*(xHat[1]-1.0)*(xHat[2]-1.0)
    v2=-(xHat[0]+1.0)*(xHat[1]+1.0)*(xHat[2]-1.0)
    v3=(xHat[0]-1.0)*(xHat[1]+1.0)*(xHat[2]-1.0)
    v4=(xHat[0]-1.0)*(xHat[1]-1.0)*(xHat[2]+1.0)
    v5=-(xHat[0]+1.0)*(xHat[1]-1.0)*(xHat[2]+1.0)
    v6=(xHat[0]+1.0)*(xHat[1]+1.0)*(xHat[2]+1.0)
    v7=-(xHat[0]-1.0)*(xHat[1]+1.0)*(xHat[2]+1.0)

    sum = v0*p[0] + v1*p[1] + v2*p[2] + v3*p[3] + \
          v4*p[4] + v5*p[5] + v6*p[6] + v7*p[7]
    sum = factor(3.0*sum)
    return sum/24.0   # 3/24 = 1/8 for bypass the bug

e = [e_0, e_1, e_2]
f = [f_0, f_1, f_2]

q0 = np.array([0,0,0])
q1 = np.array([1,0,0])
q3 = np.array([0,1,0])
q4 = np.array([0,0,1])
q2 = e[0]*q1 + (1-e[0])*q3
q5 = e[1]*q1 + (1-e[1])*q4
q7 = e[2]*q3 + (1-e[2])*q4
q6 = f[0]*q1 + f[1]*q3 + f[2]*q4
pp = [q0, q1, q2, q3, q4, q5, q6, q7]

tt = cubeToT([x,y,z], pp)

print "mapping $T_{\\bs \\theta}$"
print tt[0]
print tt[1]
print tt[2]

print "\nmapping one to one"
sb = {e_0:0.5, e_1:0.5, e_2:0.5, f_0:1.0/3.0, f_1:1.0/3.0, f_2:1.0/3.0}
print tt[0].subs(sb)
print tt[1].subs(sb)
print tt[2].subs(sb)

print "\nmapping Duffy 3D case"
sb = {e_0:0, e_1:0, e_2:0, f_0:0, f_1:0, f_2:1}
print tt[0].subs(sb)
print tt[1].subs(sb)
print tt[2].subs(sb)
