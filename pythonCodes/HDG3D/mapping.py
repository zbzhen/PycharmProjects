#!/usr/bin/env python
#-*- coding: utf-8 -*-
from sympy import*
import numpy as np
var(["x"+str(i) for i in range(8)])
var(["y"+str(i) for i in range(8)])
var(["z"+str(i) for i in range(8)])
var("a,b,c,x,y,z")

def cubeToTbMapping(xhat):
    def f(x,y):
        return 7-2*x-2*y+x*y
    def g(x):
        return 1+x
    # y1 = separatevars(g(a)*f(b,c)*1.0/24)
    # y2 = separatevars(g(b)*f(c,a)*1.0/24)
    # y3 = separatevars(g(c)*f(a,b)*1.0/24)
    # y1 = y1.subs({a:xhat[0], b:xhat[1], c:xhat[2]})
    # y2 = y2.subs({a:xhat[0], b:xhat[1], c:xhat[2]})
    # y3 = y3.subs({a:xhat[0], b:xhat[1], c:xhat[2]})
    a,b,c = xhat
    return [g(a)*f(b,c)*1.0/24, g(b)*f(c,a)*1.0/24, g(c)*f(a,b)*1.0/24]


def cubeToT(xHat, p):
    v = [0]*8
    v[0]=-(xHat[0]-1.0)*(xHat[1]-1.0)*(xHat[2]-1.0)/8.0;
    v[1]=(xHat[0]+1.0)*(xHat[1]-1.0)*(xHat[2]-1.0)/8.0;
    v[2]=-(xHat[0]+1.0)*(xHat[1]+1.0)*(xHat[2]-1.0)/8.0;
    v[3]=(xHat[0]-1.0)*(xHat[1]+1.0)*(xHat[2]-1.0)/8.0;
    v[4]=(xHat[0]-1.0)*(xHat[1]-1.0)*(xHat[2]+1.0)/8.0;
    v[5]=-(xHat[0]+1.0)*(xHat[1]-1.0)*(xHat[2]+1.0)/8.0;
    v[6]=(xHat[0]+1.0)*(xHat[1]+1.0)*(xHat[2]+1.0)/8.0;
    v[7]=-(xHat[0]-1.0)*(xHat[1]+1.0)*(xHat[2]+1.0)/8.0;
    return np.dot(p,v)

def tbToT(xThat, p):
    x = [0]*3
    for i in [0,1,2]:
	    x[i] = p[0][i]*xThat[0] + p[1][i]*xThat[1] + p[2][i]*xThat[2]+p[3][i]*(1.0-xThat[0]-xThat[1]-xThat[2])
    return x


tmp = [[x0,y0,z0],[x1,y1,z1],[x2,y2,z2],[x3,y3,z3],[x4,y4,z4]]
pp = [
    [x3,y3,z3],
    [x0,y0,z0],
    [0.5*(x1+x0),0.5*(y1+y0),0.5*(z1+z0) ],
    [x1,y1,z1],
    [x2,y2,z2],
    [0.5*(x2+x0),0.5*(y2+y0),0.5*(z2+z0) ],
    [1.0/3.0*(x0+x1+x2), 1.0/3.0*(y0+y1+y2), 1.0/3.0*(z0+z1+z2)],
    [0.5*(x2+x1),0.5*(y2+y1),0.5*(z2+z1) ]
]

tt =  cubeToT([x,y,z], np.array(pp).T)
print "下面这个是一步到位的变换--------------------------------------"
print expand(simplify(tt[0]))
print expand(simplify(tt[1]))
print expand(simplify(tt[2]))
print "下面这个是分两步的变换--------------------------------------"
xThat = cubeToTbMapping([x,y,z]); ans = tbToT(xThat, tmp)
print expand(ans[0])
print expand(ans[1])
print expand(ans[2])
print "做差之后的结果如下--------------------------------------"
print expand(ans[0]) - expand(simplify(tt[0]))
print expand(ans[1]) - expand(simplify(tt[1]))
print expand(ans[2]) - expand(simplify(tt[2]))
print "上面的结果说明变换的一致性"









# ans = cubeToTbMapping([a,b,c])
# print expand(ans[0])
# print expand(ans[1])
# print expand(ans[2])
#
# # p = [[x0,x1,x2,x3,x4,x5,x6,x7],[y0,y1,y2,y3,y4,y5,y6,y7],[z0,z1,z2,z3,z4,z5,z6,z7]]
# bp = [[0,1,0.5,0, 0,0.5,1.0/3.0,0], [0,0,0.5,1, 0,0,1.0/3.0,0.5], [0,0,0,0, 1,0.5,1.0/3.0,0.5]]
# xHat = [a,b,c]
# tt =  cubeToT(xHat, bp)
# print "--------------------------------------"
# print expand(simplify(tt[0]))
# print expand(simplify(tt[1]))
# print expand(simplify(tt[2]))
# print "做差之后的结果如下--------------------------------------"
# print expand(ans[0]) - expand(simplify(tt[0]))
# print expand(ans[1]) - expand(simplify(tt[1]))
# print expand(ans[2]) - expand(simplify(tt[2]))
# print "上面的结果说明变换的一致性"
# print


