#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: 3dja
@time: 2018/6/28  17:00
"""

from sympy import*
import numpy as np
xhat, yhat, zhat = var("xhat,yhat,zhat")
x, y, z = var("x,y,z")
a,b,c = var("a,b,c")
xi, eta, zeta = var("xi,eta,zeta")
var(["e_"+str(i) for i in range(5)])
var(["f_"+str(i) for i in range(5)])
var(["g_"+str(i) for i in range(5)])
var(["a_"+str(i) for i in range(5)])
var(["b_"+str(i) for i in range(5)])
var(["c_"+str(i) for i in range(5)])

def cubeToT(xHat, p):
    v0=-(xHat[0]-1)*(xHat[1]-1)*(xHat[2]-1)
    v1=(xHat[0]+1)*(xHat[1]-1)*(xHat[2]-1)
    v2=-(xHat[0]+1)*(xHat[1]+1)*(xHat[2]-1)
    v3=(xHat[0]-1)*(xHat[1]+1)*(xHat[2]-1)
    v4=(xHat[0]-1)*(xHat[1]-1)*(xHat[2]+1)
    v5=-(xHat[0]+1)*(xHat[1]-1)*(xHat[2]+1)
    v6=(xHat[0]+1)*(xHat[1]+1)*(xHat[2]+1)
    v7=-(xHat[0]-1)*(xHat[1]+1)*(xHat[2]+1)

    sum = v0*p[0] + v1*p[1] + v2*p[2] + v3*p[3] + \
          v4*p[4] + v5*p[5] + v6*p[6] + v7*p[7]
    return simplify(sum)  # 3/24 = 1/8 for bypass the bug


e = [e_0, e_1, e_2]
f = [f_0, f_1, f_2]
g = [g_0, g_1, g_2]
q0 = np.array([0,0,0])
q1 = np.array([1,0,0])
q3 = np.array([0,1,0])
q4 = np.array([0,0,1])
q2 = e[0]*q1 + g[0]*q3
q5 = e[1]*q1 + g[1]*q4
q7 = e[2]*q3 + g[2]*q4
q6 = f[0]*q1 + f[1]*q3 + f[2]*q4
pp = [q0, q1, q2, q3, q4, q5, q6, q7]

tt = cubeToT([x,y,z], pp)
t = [0.5,0.5,0.5,1.0/3.0,1.0/3.0]
sb = {e_0:t[0], e_1:t[1], e_2:t[2], f_0:t[3], f_1:t[4], f_2:1-t[3]-t[4], g_0:1-t[0], g_1:1-t[1], g_2:1-t[2]}


# fa = (1+x)*( a_0*y*z + a_1*y + a_2*z + a_3)
# fb = (1+y)*( b_0*x*z + b_1*x + b_2*z + b_3)
# fc = (1+z)*( c_0*y*x + c_1*x + c_2*y + c_3)
# print solve([fa-a,fb-b,fc-c], [x,y,z])
# #
# print solve([fa-a,fb-b,fc-c], [x,y,z])

fa = (1+x)*( y*z -2*y -2*z + 7)
fb = (1+y)*( x*z -2*x -2*z + 7)
fc = (1+z)*( y*x -2*x -2*y + 7)
print solve([fa-0,fb-0,fc-0], [x,y,z])

ja = Matrix([
    [diff(fa,x),diff(fb,x), diff(fc,x)],
    [diff(fa,y),diff(fb,y), diff(fc,y)],
    [diff(fa,z),diff(fb,z), diff(fc,z)]
])
# print ja
# J = ja.det()
# a,b,c = var("a,b,c")
#
# print simplify(J)
# print factor(J)
# jj = J.subs({x:a-1, y:b-1, z:c-1})
# print simplify(jj)


# print tt
# ja = Matrix([diff(tt,x),diff(tt,y), diff(tt,z)]).det()
# print ja
# print separatevars(ja,[x,y,z])
# print simplify(3*ja.subs(sb))




