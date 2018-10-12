#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 13:32
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 立体几何.py
# @version : Python 2.7.6
import numpy as np
from mayavi import mlab


fig = mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))

linecolor = (0, 0, 0)
linesize = 0.01
mlab.clf()
x = np.array([-1,1,1,-1,-1])*1.0
y = np.array([-1,-1,1,1,-1])*1.0
z = np.array([0,0,0,0,0])-1.0
mlab.plot3d(x, y, z, line_width=0.1, transparent=True, tube_radius=linesize, color=linecolor)
z = np.array([0,0,0,0,0])+1.0
mlab.plot3d(x, y, z, line_width=0.1, transparent=True, tube_radius=linesize, color=linecolor)

z = np.array([-1,1])*1.0
x = np.array([-1,-1])*1.0
y = np.array([-1,-1])*1.0
mlab.plot3d(x, y, z, line_width=0.1, transparent=True, tube_radius=linesize, color=linecolor)
x = np.array([1, 1])*1.0
y = np.array([-1,-1])*1.0
mlab.plot3d(x, y, z, line_width=0.1, transparent=True, tube_radius=linesize, color=linecolor)
x = np.array([1,1])*1.0
y = np.array([1,1])*1.0
mlab.plot3d(x, y, z, line_width=0.1, transparent=True, tube_radius=linesize, color=linecolor)
x = np.array([-1,-1])*1.0
y = np.array([1,1])*1.0
mlab.plot3d(x, y, z, line_width=0.1, transparent=True, tube_radius=linesize, color=linecolor)

x = np.array([-1,1])*1.0
y = np.array([-1,1])*1.0
z = np.array([-1,1])*1.0
# mlab.plot3d(x,y,z, tube_radius=linesize*0.3, color=(0,1,0), representation="wireframe")  # 细线表示内部的线
num = 20
for i in range(num):
    xx = np.array([x[0]+1.0/num*i*(x[1]-x[0]), x[0]+1.0/num*(i+1)*(x[1]-x[0])])
    yy = np.array([y[0]+1.0/num*i*(y[1]-y[0]), y[0]+1.0/num*(i+1)*(y[1]-y[0])])
    zz = np.array([z[0]+1.0/num*i*(z[1]-z[0]), z[0]+1.0/num*(i+1)*(z[1]-z[0])])
    if i%2 == 0:
        mlab.plot3d(xx,yy,zz, tube_radius=linesize*0.1, color=(0.2, 0.2, 0.2), representation="wireframe")  # 细线表示内部的线


mlab.points3d(x,y,z, scale_factor=linesize*0.3)

# x, y  = np.array(np.meshgrid([-1.0,1.0], [-1.0,1.0]))
# z = 0.0*x




mlab.points3d(-1.0/3,-1.0/3,-1.0/3, scale_factor=0.08, color=(1.0, 0, 0))

x = np.array([-1,1,-1,-1]).reshape((2,2))
y = np.array([-1,-1,1,1]).reshape((2,2))
z = -1-x-y
mlab.mesh(x, y, z, transparent=True, colormap="black-white")

mlab.text(-1, -1, 'A', z=-1, width=0.03)
mlab.text(1, -1, 'B', z=-1, width=0.03)
mlab.text(1, 1, 'C', z=-1, width=0.03)
mlab.text(-1, 1, 'D', z=-1, width=0.03)

mlab.text(-1, -1, "A'", z=1, width=0.035)
mlab.text(1, -1, "B'", z=1, width=0.035)
mlab.text(1, 1, "C'", z=1, width=0.035)
t = mlab.text(-1, 1, "1", z=1, width=0.001, name="1", color=(1,0,0), figure=fig)
t.property.shadow = True
mlab.text(-1.0/3,-1.0/3, "H", z=-1.0/3, width=0.03)


a = 3
b = 3
c = 3
t = lambda x: 1.0*x/abs(x)
mlab.quiver3d(0, 0, 0, a-t(a), 0, 0, extent=[0,a-t(a),0,0,0,0], color=(1,0,0), mode='2ddash')
mlab.quiver3d(a-t(a), 0, 0, a, 0, 0, extent=[a-t(a),a,0,0,0,0], color=(1,0,0), mode='arrow')
mlab.quiver3d(0, 0, 0, 0, b-t(b), 0, extent=[0,0,0,b-t(b),0,0], color=(0,1,0), mode='2ddash')
mlab.quiver3d(0, b-t(b), 0, 0, b, 0, extent=[0,0,b-t(b),b,0,0], color=(0,1,0), mode='arrow')
mlab.quiver3d(0, 0, 0, 0, 0, c-t(c), extent=[0,0,0,0,0,c-t(c)], color=(0,0,1), mode='2ddash')
mlab.quiver3d(0, 0, c-t(c), 0, 0, c, extent=[0,0,0,0,c-t(c),c], color=(0,0,1), mode='arrow')
mlab.text(a, 0, 'X', z=0, width=0.03)
mlab.text(0, b, 'Y', z=0, width=0.03)
mlab.text(0, 0, 'Z', z=c, width=0.03)



# mlab.text(0, 0, 'A', z=0, line_width=0.05)

# mlab.outline()
# mlab.colorbar()
mlab.savefig("litijihe.png")
mlab.show()