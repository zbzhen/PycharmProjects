#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: flower2.py
@time: 2016-04-21 21:17
"""
#链接：http://www.zhihu.com/question/30402203/answer/94150700
import numpy as np
from numpy import cross, pi, sin ,cos
eps = 1e-8

f = open('rose.pov','w')
f.write("camera{location 0.92*<1.375,-1.625,1.5> look_at <0,0,0.25> right x*image_width/image_height up z sky z} light_source{0.92*<1.375,-1.625,1.5>,1}")

def hue(x):
    return np.array([x,sin(x*pi),abs(cos(x*pi))])

def DrawMesh(Mesh,color):

    normals = np.zeros(Mesh.shape)
    LeftTop = Mesh[0:-1,0:-1]
    RightTop = Mesh[0:-1,1:]
    LeftBot = Mesh[1:,0:-1]
    RightBot = Mesh[1:,1:]

    p0 = (LeftTop + RightTop + LeftBot + RightBot)/4
    N = cross(RightTop-p0, RightBot-p0)
    E = cross(RightBot-p0, LeftBot-p0)
    S = cross(LeftBot-p0, LeftTop-p0)
    W = cross(LeftTop-p0, RightBot-p0)

    normals[0:-1,0:-1] += (S+W)
    normals[1:,0:-1] += (N+W)
    normals[0:-1,1:] += (S+E)
    normals[1:,1:] += (N+E)

    for i in range(Mesh.shape[0]):
        for j in range(Mesh.shape[1]):
            normals[i,j] /= np.linalg.norm(normals[i,j])

    for i in range(Mesh.shape[0]-1):
        for j in range(Mesh.shape[1]-1):
            color_quad( \
                        Mesh[i,j],normals[i,j],hue(color[i,j]),\
                        Mesh[i+1,j],normals[i+1,j],hue(color[i+1,j]),\
                        Mesh[i+1,j+1],normals[i+1,j+1],hue(color[i+1,j+1]),\
                        Mesh[i,j+1],normals[i,j+1],hue(color[i,j+1]) )

def color_triangle(p1,n1,c1, p2,n2,c2, p3,n3,c3):
    nx = p2-p1
    ny = p3-p1
    nz = cross(nx,ny)
    det = np.linalg.det([nx,ny,nz])
    if abs(det) < eps:
        pigment="""pigment {{ rgb <{},{},{}> }}""".format(*c1)
    else:
        pigment="""pigment{{
        average pigment_map{{
        [1 gradient x color_map{{[0 rgbt <0,0,0,0.1>][1 rgbt <{},{},{},0.1>]}}]

        [1 gradient y color_map{{[0 rgbt <0,0,0,0.1>][1 rgbt <{},{},{},0.1>]}}]

        [1 gradient z color_map{{[0 rgbt <0,0,0,0.1>][1 rgbt <{},{},{},0.1>]}}]}}
        matrix <1.01,0,1, 0,1.01,1, 0,0,1, -0.002,-0.002,-1>
        matrix <{},{},{},{},{},{},{},{},{},{},{},{}>}}\n""".format(3*c2[0],3*c2[1],3*c2[2],3*c3[0],3*c3[1],3*c3[2],3*c1[0],3*c1[1],3*c1[2],nx[0],nx[1],nx[2],ny[0],ny[1],ny[2],nz[0],nz[1],nz[2],p1[0],p1[1],p1[2])
    finish = """finish { phong 0.4
    phong_size 0.25
    specular 0.25
    reflection 0.25}\n"""

    f.write("""smooth_triangle{{ <{},{},{}>,<{},{},{}>,<{},{},{}>,<{},{},{}>,<{},{},{}>,<{},{},{}> texture{{ {} }}}}\n""".format(p1[0],p1[1],p1[2],n1[0],n1[1],n1[2],p2[0],p2[1],p2[2],n2[0],n2[1],n2[2],p3[0],p3[1],p3[2],n3[0],n3[1],n3[2],pigment+finish))


def color_quad(p1,n1,c1, p2,n2,c2, p3,n3,c3, p4,n4,c4):
    if np.linalg.norm(p3-p1) < np.linalg.norm(p4-p2):
        color_triangle(p1,n1,c1, p2,n2,c2, p3,n3,c3)
        color_triangle(p1,n1,c1, p3,n3,c3, p4,n4,c4)
    else:
        color_triangle(p1,n1,c1, p2,n2,c2, p4,n4,c4)
        color_triangle(p2,n2,c2, p3,n3,c3, p4,n4,c4)


theta1 = -20*pi/9
theta2= 15*pi
x0 = 0.7831546645625248
def rose(x1,theta):
    phi = pi/2*np.exp(-theta/8/pi)
    new_theta = theta
    y1 = 1.9565284531299512*x1**2*((1.2768869870150188*x1-1)**2*sin(phi))
    X = 1-(1.25*(1-(3.6*theta%(2*pi)/pi))**2-0.25)**2 /2
    r = X*(x1*sin(phi)+y1*cos(phi))
    return np.array([r*sin(new_theta),r*cos(new_theta),X*(x1*cos(phi)-y1*sin(phi)),x1])

x = np.linspace(0,1,24)
y = np.linspace(theta1,theta2,575)
X,Y = np.meshgrid(x,y)
Z = rose(X,Y)
Mesh = np.dstack((Z[0,...],Z[1,...],Z[2,...]))
color = Z[3,...]
DrawMesh(Mesh,color)

f.close()