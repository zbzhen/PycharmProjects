#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 9:06
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : eg.py
# @version : Python 2.7.6
import numpy as np
from mayavi import mlab
from pointLinePlane import spaceElement, Frame, Axis, getcubepoints, setSCALING
################################################################################
# Disable the rendering, to get bring up the figure quicker:
# figure = mlab.gcf()
figure =mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
mlab.clf()
figure.scene.disable_render = True

A = spaceElement([1,0,0])
B = spaceElement([0,1,0])
C = spaceElement([0,0,1])
P = spaceElement([0,0,0])
D = spaceElement([0.5,0.5,0])


points = [A,B,C,D,P]
pointsplot = [p.plot(color=(1, 0, 0)) for p in points]
# for p in points:
#     p.plotText(str(p))
A.plotText("A")
Aplot = A.plot(color=(1, 0, 0))

AC = spaceElement(A, C)
AC.plot(color=(0, 0, 0), num=2)
ACm = spaceElement(A, C).getCenterPoint()
ACmplot = ACm.plot(color=(0, 0, 0))
ABC = spaceElement(A, B, C)
ABCplot = ABC.plot(opacity=0.8)
t = 0
def picker_callback(picker):
    global t
    t += 1
    for i,pp in enumerate(pointsplot):
        if picker.actor in pp.actor.actors:
            points[i].plot(color=(t%2, 0, 0))



    if picker.actor in AC.actors:
        AC.plot(color=((t%2)*0.3, (t%2)*0.3, (t%2)*0.3))
    # if picker.actor in ACmplot.actor.actors:
    #     AC.plot(color=((t%2)*0.3, (t%2)*0.3, (t%2)*0.3))
    #     ACm.plot(color=((t%2)*0.3, (t%2)*0.3, (t%2)*0.3))
    #     if t%2 ==1:
    #         ABCplot.actor.property.delete = True
    #     # ABCplot.mlab_source.reset(opacity=(t%3)*0.4, scalars=(t%3)*0.4*np.array([[1,1],[1,1]]))
    #     # ABC.plot(opacity=(t%3)*0.4)
    #     ABC.getCenterPoint().plot(color=((t%2)*1.0, 0., 0.))

    if t>100:
        spaceElement([0,0,0]).plotText("Too many clicks, Please restart!!", 0.8)

    # picked = picker.actors
    # if ABCplot.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
    #     ABCplot.mlab_source.reset(opacity=(t%3)*0.4)
    #     # ABC.plot(opacity=(t%3)*0.4)
    #     ABC.getCenterPoint().plot(color=((t%2)*1.0, 0., 0.))



picker = figure.on_mouse_pick(picker_callback)
# Decrease the tolerance, so that we can more easily select a precise
# point.
picker.tolerance = 0.01
mlab.show()
