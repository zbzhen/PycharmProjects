#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 16:09
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 选中变色.py
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
Axis(2,2,2).plot(arraymode="2darrow")
A = spaceElement([1,0,0])
B = spaceElement([0,1,0])
C = spaceElement([0,0,1])
P = spaceElement([0,0,0])
D = spaceElement([0.5,0.5,0])


points = [A,B,C,D,P]
pointsplot = [p.plot(color=(1, 0, 0)) for p in points]
# for p in points:
#     p.plotText(str(p))


AC = spaceElement(A, C)
ACplot = [AC.plot(color=(0,0,0), num=20), AC.plot(color=(1,0,0), num=20)]
ACplot[1].actor.visible = False

ACm = spaceElement(A, C).getCenterPoint()
ACmplot = ACm.plot(color=(0, 0, 0))

A.plotText("A")
Aplot = [A.plot(color=(1, 0, 0), scale_factor=0.08), A.plot(color=(0, 0, 0), scale_factor=0.08)]


ABC = spaceElement(A, B, C)
f = lambda x: 0*x + 1
ABCplot = [ABC.plot(opacity=0.8, num=20), ABC.plot(opacity=1.0, num=20, scalarsfunction=f)]


ps = getcubepoints()
a = [spaceElement(p) for p in ps]
Frame(a[:4], a[4:]).plot()
spaceElement(a[0],a[2],a[6],a[4]).plot(colormap="Spectral")


def picker_callback(picker):
    def plot(XXplot):
        for i in range(len(XXplot)):
            if picker.actor in XXplot[i].actor.actors:
                XXplot[i].actor.visible = False
                XXplot[(i+1)%len(XXplot)].actor.visible = True

    plot(ABCplot)
    plot(ACplot)
    plot(Aplot)


picker = figure.on_mouse_pick(picker_callback)
# Decrease the tolerance, so that we can more easily select a precise
# point.
picker.tolerance = 0.01
mlab.show()
