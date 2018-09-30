#!/usr/bin/env python
#-*- coding: utf-8 -*-
from sympy import*
import numpy as np
var(["x"+str(i) for i in range(5)])
var("a,b,c,x,y,z")
def f(x,y):
    return 7-2*x-2*y+x*y

def g(x):
    return 1+x

def h(x):
    return x-2

def cubeToTbMapping(xhat):
    a,b,c = xhat
    # return [g(a)*f(b,c), g(b)*f(c,a), g(c)*f(a,b)]
    return [g(a)*f(b,c)*1.0/24, g(b)*f(c,a)*1.0/24, g(c)*f(a,b)*1.0/24]


y1 = g(a)*f(b,c) -24*x
y2 = g(b)*f(c,a)-24*y
y3 = g(c)*f(a,b)-24*z
# y1 = (9-b)*(a-b) - 24*(x-z)
# y2 = (9-a)*(c-b) - 24*(z-y)
# y3 = (9-c)*(b-a) - 24*(x-x)
print [y1,y2,y3]
ans3d =  solve( [y1,y2,y3],[a,b,c])
print ans3d

ans = cubeToTbMapping([a,b,c])
t1 =  expand(ans[0])
t2 =  expand(ans[1])
t3 =  expand(ans[2])

s1 =  together(t1-t2)
s2 =  together(t2-t3)
s3 =  together(t3-t1)
y1 = s1 - (x-y)
y2 = s2 - (y-z)
y3 = s3 - (z-x)

ans3d =  solve( [s1 - (x-y), s2 - (y-z), g(c)*f(a,b)-24*z],[a,b,c])

print ans3d


# t = [(1+a)*(3-b)-8*x, (3-a)*(1+b)-8*y]
# ans =  solve(t,  [a, b])
# tt0 = t[0].subs({a:ans[1][0], b:ans[1][1]})
# tt1 = t[0].subs({a:ans[1][0], b:ans[1][1]})
# print ans
# print simplify(tt0)
# print simplify(tt1)