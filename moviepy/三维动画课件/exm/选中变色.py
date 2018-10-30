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
ACplot = [AC.plot(linesize=0.01,color=(0,0,0), num=20), AC.plot(linesize=0.02, color=(1,0,0), num=20)]


ACm = spaceElement(A, C).getCenterPoint()
ACmplot = ACm.plot(color=(0, 0, 0))

A.plotText("A")
Aplot = [A.plot(color=(1, 0, 0), scale_factor=0.08), A.plot(color=(0, 0, 0), scale_factor=0.08)]


ABC = spaceElement(A, B, C)
ABC2 = spaceElement(A, B, C)



f = lambda x: 0*x + 1
# ABCplot = [ABC.plot(opacity=0.8, num=20), ABC2.plot(opacity=1.0, num=20, scalarsfunction=f)]

# ABCplot = [ABC.plot(opacity=0.8, num=20)]
ABCplot = []
for i in range(20):
    ABC.SCALING = 1+0.05*i
    ABCplot += [ABC.plot(opacity=0.8, num=20)]



ps = getcubepoints()
a = [spaceElement(p) for p in ps]
Frame(a[:4], a[4:]).plot()
a0264 = spaceElement(a[0],a[2],a[6],a[4])

a0264plot = [a0264.plot(colormap="Spectral", opacity=0.3, scalarsfunction=f), a0264.plot(colormap="Spectral", opacity=0.8, scalarsfunction=f)]


# from matplotlib import mathtext
# parser = mathtext.MathTextParser("bitmap")
# tmp,x = parser.to_mask(r'$\alpha$', dpi=120, fontsize=20)
# tmp = np.where(tmp>0,1,0)
# a0167 = spaceElement(a[0],a[1],a[6],a[7])
# def cf(x):
#     ans = np.zeros_like(x)
#     s,t = np.shape(tmp)
#     ans[len(x)-s:, :t] = tmp
#     return ans
# a0167.plot(colormap="Spectral", opacity=0.3, scalarsfunction=f, num=60)

# class ContralParameters(object):
#     a = 0
#     b = 0
#     c = 0
# cp = ContralParameters()



pickerplots = [Aplot, ACplot, ABCplot, a0264plot]
def init(plots):
    for pts in plots:
        pts[0].actor.visible = True
        for i in range(1, len(pts)):
            pts[i].actor.visible = False
    return
init(pickerplots)


def pickdirection(direction):

    def picker_callback(picker):
        def plot(XXplot):
            for i in range(len(XXplot)):
                if picker.actor in XXplot[i].actor.actors:
                    XXplot[i].actor.visible = False
                    XXplot[(i+1*direction)%len(XXplot)].actor.visible = True
        for pt in pickerplots:
            plot(pt)
    return picker_callback

def initialize(picker):
    mark = -1
    for i, pts in enumerate(pickerplots):
        for p in pts:
            if picker.actor in p.actor.actors:
                mark = i
    if mark == -1:
        init(pickerplots)
    else:
        init([pickerplots[mark]])
    return

picker = figure.on_mouse_pick(pickdirection(1), button="Left")
picker.tolerance = 0.01
picker = figure.on_mouse_pick(pickdirection(-1), button="Right")
picker.tolerance = 0.01
picker = figure.on_mouse_pick(initialize, button="Middle")
picker.tolerance = 0.01
mlab.show()
