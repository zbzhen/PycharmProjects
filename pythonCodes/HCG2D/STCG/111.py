# -*- coding: UTF-8 -*-
import numpy as np
#初始条件
def iteration(A, b, x, e=0.00001):
    r=np.dot(A,x)+b
    while np.linalg.norm(r)>e:
        d=np.dot(np.linalg.inv(A),-1*r)
        p=np.dot(r.T,d)
        q=np.dot(d.T,A)
        h=np.dot(q,d)
        a=-float(p)/float(h)  #搜索步长
        x=x+a*d
        return x
x=np.array([[1],[1]])  #初始点
b=np.array([[-1],[0]])
A=np.array([[1,-1],[-1,2]])
x = iteration(A, b, x, e=0.00001)
print "The unknown quantity: x =", x