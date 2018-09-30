#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/27 15:55
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : hyperbolic1d.py
# @version : Python 2.7.6
import numpy as np
from scipy.sparse import lil_matrix
from numpy.polynomial import legendre
from sympy import integrate, cos, pi


Nelement = 40
print Nelement
h = 1.0/Nelement
T = 3.0
deltat = h*h
deg = 1
eledof = (deg+1)
Dof = Nelement*eledof
qp, qw = legendre.leggauss(8)
def uxt(x,t):
    return np.cos(2*np.pi*(x-t))
def mapping1D(a, b):
    return lambda x: 0.5*(b-a)*x + 0.5*(b+a)

def base(x):
    return np.array([1+0*x, 0.5*x])



mathbbA = np.array([[-1.,  -0.5], [ 6.,  -3.]])/h
mathbbB = np.array([[1.,  0.5],   [ -6.,  -3.]])/h
mathbbL = lil_matrix((Dof, Dof))
# mathbbL = np.zeros((Dof, Dof))

for i in range(Nelement):
    mathbbL[i*eledof:(i+1)*eledof, i*eledof:(i+1)*eledof] = mathbbA
for i in range(1, Nelement):
    mathbbL[i*eledof:(i+1)*eledof, (i-1)*eledof:i*eledof] = mathbbB
mathbbL[:eledof, -eledof:] = mathbbB

def u0(x):
    return np.cos(2*np.pi*x)

vectorg = np.zeros(Dof)
tmp = np.zeros(deg+1)
phi = base(qp)
for ic in range(Nelement):
    mp = mapping1D(ic*h, (ic+1)*h)
    u = uxt(mp(qp), 0)
    tmp[0] = (u*qw*phi[0]).sum()*0.5
    tmp[1] = (u*qw*phi[1]).sum()*6
    vectorg[ic*eledof: (ic+1)*eledof] = tmp

print

# tmp1 = np.zeros(eledof)
# for i in range(Nelement):
#     xx = np.array([h*(i), h*(i+1)])
#     tmp = np.cos(2*np.pi*xx)
#     tmp1[0] = (tmp[0]+tmp[1])*0.5
#     tmp1[1] = tmp[1]-tmp[0]
#     vectorg[i*eledof: (i+1)*eledof] = tmp1


def ite(un):
    return un + deltat*mathbbL.dot(un)

step = 0
maxstep = int(T/deltat)
uns = np.empty((maxstep, Dof), float)
un = vectorg.copy()
while(step < maxstep):
    unplus1 = ite(un)
    un = unplus1
    step += 1





def L2error(un, t):
    sum = 0.0
    phi = base(qp)
    for ic in range(Nelement):
        mp = mapping1D(ic*h, (ic+1)*h)
        u = uxt(mp(qp), t)
        eleuh = un[ic*eledof:(ic+1)*eledof]
        tmp = u - np.dot(eleuh, phi)
        sum = (tmp*tmp*qw).sum()*h
    return np.sqrt(sum)


def L1error(un, t):
    sum = 0.0
    phi = base(qp)
    for ic in range(Nelement):
        mp = mapping1D(ic*h, (ic+1)*h)
        u = uxt(mp(qp), t)
        eleuh = un[ic*eledof:(ic+1)*eledof]
        tmp = u - np.dot(eleuh, phi)
        sum = abs(tmp*qw).sum()*h
    return sum
#
# def L1uierror(un, t):
#     sum = 0.0
#     phi = base(qp)
#     for ic in range(Nelement):
#         mp = mapping1D(ic*h, (ic+1)*h)
#         u = uxt(mp(qp), t)
#         eleuh = un[ic*eledof:(ic+1)*eledof]
#         tmp = u - np.dot(eleuh, phi)
#         sum = abs(tmp).sum()*h
#     return sum


def Looerror(un, t):
    xhat = np.linspace(-1,1)
    max = 0
    phi = base(xhat)
    for ic in range(Nelement):
        mp = mapping1D(ic*h, (ic+1)*h)
        u = uxt(mp(xhat), t)
        eleuh = un[ic*eledof:(ic+1)*eledof]
        tmp = u - np.dot(eleuh, phi)
        if(max <= abs(tmp).max()):
            max = abs(tmp).max()
    return max


print "t = ", maxstep*deltat
print "L1error"
# print L1error(vectorg, 0)
print L1error(un, maxstep*deltat)
print "Looerror"
print Looerror(un, maxstep*deltat)
# print Looerror(vectorg, 0)

import matplotlib.pyplot as plt

# for it in range(maxstep-1,maxstep):
fig = plt.figure(figsize=(8,8), dpi=72,facecolor="white")
axes = plt.subplot(111)
plt.axis([0, 1, -1.2, 1.2])
# plt.axis([0, 1, -1, 1])
for ic in range(Nelement):
    u = un[ic*eledof:(ic+1)*eledof]
    plt.plot([ic*h, (ic+1)*h], [u[0]-0.5*u[1], u[0]+0.5*u[1]])
plt.show()












# mathbbM = np.array([[1.0,             0],
#                     [0,        1.0/12.0]])
# Minverse = mathbbM
#
# mathbbD = np.array([[0,        0],
#                     [1.0,      0]])
#
# mathbbE = np.array([[1,      0.5],
#                     [0.5,   0.25]])
#
# mathbbF = np.array([[1,      0.5],
#                     [-0.5, -0.25]])


# mathbbM = np.array([[1.0,             0, 1.0/12.0],
#                     [0,        1.0/12.0, 0],
#                     [1.0/12.0,        0, 1.0/80.0]])
# Minverse = mathbbM
#
# mathbbD = np.array([[0,        0, 0],
#                     [1.0,      0, 1.0/12.0],
#                     [0,  1.0/6.0, 0]])
#
# mathbbE = np.array([[1,      0.5, 0.25],
#                     [0.5,   0.25, 0.125],
#                     [0.25, 0.125, 0.0625]])
#
# mathbbF = np.array([[1,      0.5,   0.25],
#                     [-0.5, -0.25, -0.125],
#                     [0.25, 0.125, 0.0625]])
