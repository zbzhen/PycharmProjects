#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mathbbA_inverse
@time: 2018/3/3  21:56
"""
from sympy import *
var("a1,a2,b1,b2,n1,n2")
A = [[1, 0, 0, 0, 0, 0],
     [1, b1-a1, b2-a2, (b1-a1)*(b2-a2), (b1-a1)**2, (b2-a2)**2],
     [0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0],
     [0, n1, n2, n1*(b2-a2)+n2*(b1-a1), 2*n1*(b1-a1), 2*n2*(b2-a2)],
     [0, 0, 0, 0, 2, 2]]

var("x,y")
# set: n1 = (a2-b2); n2 = (b1-a1)
# set: x = (b1-a1); y = (b2-a2). Then, n1 = -y; n2 = x.
A = [[1, 0, 0, 0, 0, 0],
     [1, x, y, x*y, x**2, y**2],
     [0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0],
     [0, -y, x, -y*y+x*x, -2*y*x, 2*x*y],
     [0, 0, 0, 0, 2, 2]]

mat = Matrix(A)
AI = mat.inv()
print collect(det(mat), (x**2+y**2))
print AI[0:6]
print AI[6:12]
print simplify(AI[12:18])
print simplify(AI[18:24])
print simplify(AI[24:30])

subA = [[x*y, x**2, y**2],
        [-y*y+x*x, -2*y*x, 2*x*y],
        [0, 2, 2]]
mat = Matrix(subA)
subAI = mat.inv()
print subAI[0:3]
print subAI[3:6]
print subAI[6:9]