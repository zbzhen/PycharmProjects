#!/usr/bin/env python  
#-*- coding: utf-8 -*-
from sympy import*
var(["x"+str(i) for i in range(5)])
var("a,b,c")

def f(x,y):
    return 7-2*x-2*y+x*y

def g(x):
    return 1+x

def h(x):
    return x-2

def ja(xi, eta, zta):
    return \
        (f(xi,eta)*f(xi,zta)*f(eta,zta) +\
        2*g(xi)*g(eta)*g(zta)*h(xi)*h(eta)*h(zta) -\
        g(zta)*g(xi)*h(eta)*h(eta)*f(xi,zta) -\
        g(zta)*g(eta)*h(xi)*h(xi)*f(eta,zta) -\
        g(eta)*g(xi)*h(zta)*h(zta)*f(xi,eta))#/24.0/24.0/24.0

coords = [[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1]]
coords +=[[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]]


# jj = collect(jj, )
# print jj
print factor(ja(a,b,c))
jj =  separatevars(ja(a,b,c))
def newja(xi,eta,zta):
    return jj.subs({a:xi,b:eta,c:zta})#/24.0/24.0/24.0


# dd = newja(a,b,1)
# print separatevars(newja(a-1,b-1,c-1))
# print separatevars(newja(a,b,c))
print separatevars(newja(-1,b,c))
print separatevars(newja(1,b,c))
print separatevars(newja(a,1,c))
print separatevars(newja(a,b,1))
print separatevars(newja(-1,b,c))
print separatevars(newja(a,-1,c))
print separatevars(newja(a,b,-1))
# print collect(a*a+a*b,a)
# print separatevars(a*a+a*b,a+b)
# print separatevars(a*a+b*b+2*a*b)


J = separatevars(newja(a+1,b+1,c+1))
J_a =  separatevars(diff(J,a))

print J
print separatevars(J_a)
print separatevars(J_a.subs({a:0}))
