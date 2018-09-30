#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: TTheta3Dsymmetrical
@time: 2018/6/28  13:50
"""
from sympy import*
import numpy as np
xhat, yhat, zhat = var("xhat,yhat,zhat")
x, y, z = var("x,y,z")
xi, eta, zeta = var("xi,eta,zeta")
var(["e_"+str(i) for i in range(5)])
var(["f_"+str(i) for i in range(5)])
var(["g_"+str(i) for i in range(5)])

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

print diff(tt,x)
print Matrix([diff(tt,x),diff(tt,y), diff(tt,z)]).det()


print "mapping $T_{\\bs \\theta}$"
print tt[0]
print tt[1]
print tt[2]
# print solve(tt, [x,y,z])
print "\nmapping one to one"
t = [0.5,0.5,0.5,1.0/3.0,1.0/3.0]
sb = {e_0:t[0], e_1:t[1], e_2:t[2], f_0:t[3], f_1:t[4], f_2:1-t[3]-t[4], g_0:1-t[0], g_1:1-t[1], g_2:1-t[2]}
print tt[0].subs(sb)
print tt[1].subs(sb)
print tt[2].subs(sb)
mp11 = tt.subs(sb)
print simplify(Matrix([diff(mp11,x),diff(mp11,y), diff(mp11,z)]).det())
# print linsolve([mp11[0], mp11[1], mp11[2]], [x,y,z])


print "\nmapping Duffy 3D case"
t = [0,0,0,0,0]
sb = {e_0:t[0], e_1:t[1], e_2:t[2], f_0:t[3], f_1:t[4], f_2:1-t[3]-t[4], g_0:1-t[0], g_1:1-t[1], g_2:1-t[2]}
print tt[0].subs(sb)
print tt[1].subs(sb)
print tt[2].subs(sb)
duffy = tt.subs(sb)
print solve([duffy[0]-xhat, duffy[1]-yhat, duffy[2]- zhat], [x,y,z])

# print solve([x+xhat-1, x+yhat], [xhat,yhat])