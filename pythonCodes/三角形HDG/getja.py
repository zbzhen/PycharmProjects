# -*- coding: utf-8 -*-
import numpy as np
from sympy import*
x,y,z = symbols('x,y,z')
a,b,c = symbols('a,b,c')

#t = 1/24.0
t =  symbols('t')
x = t*(1+a)*(7-2*b-2*c-b*c)
y = t*(1+b)*(7-2*c-2*a-a*c)
z = t*(1+c)*(7-2*a-2*b-b*a)
#print diff(x,a,1,b,0,c,0)





a00 = diff(x,a,1,b,0,c,0)
a01 = diff(y,a,1,b,0,c,0)
a02 = diff(z,a,1,b,0,c,0)

a10 = diff(x,a,0,b,1,c,0)
a11 = diff(y,a,0,b,1,c,0)
a12 = diff(z,a,0,b,1,c,0)

a20 = diff(x,a,0,b,0,c,1)
a21 = diff(y,a,0,b,0,c,1)
a22 = diff(z,a,0,b,0,c,1)

print "a00=",a00
print "a01=",a01
print "a02=",a02

print "a10=",a10
print "a11=",a11
print "a12=",a12

print "a20=",a20
print "a21=",a21
print "a22=",a22

def computerja(a00,a01,a02,
               a10,a11,a12,
               a20,a21,a22):
    return a00*a11*a22 + a01*a12*a20 + a02*a10*a21 -\
           a02*a11*a20 - a01*a10*a22 - a00*a12*a21

J =  computerja(a00,a01,a02, a10,a11,a12, a20,a21,a22)
J = simplify(J)

print "J.subs({a:0.5, b:0.5, c:0})=",J.subs({a:0.5, b:0.5, c:0})
"""
def ff(xx, yy, zz):
    return sJ.subs({a:xx, b:yy, c:zz})
"""