#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/20 10:59
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 直线与平面的三种关系.py
# @version : Python 2.7.6
from pointLinePlane import spaceElement, Frame, Axis, getcubepoints, setSCALING, puttex
import numpy as np
from enthought.traits.api import HasTraits, Float, Int, Bool, Range, Str, Button, Instance
from enthought.traits.ui.api import View, HSplit, Item, VGroup, EnumEditor, RangeEditor
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi import mlab
from tvtk.api import tvtk
from tvtk.common import configure_input_data
import matplotlib.pyplot as plt


from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei', "FangSong"][-1]

# ----------------------------------------------
#   begin plot
# ----------------------------------------------
mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
mlab.clf()
v = mlab.gcf(engine=None)
y = 1.4
ps1 = np.array([[0,0,0], [1,0,0], [1,y,0], [0,y,0]])
plane1 = spaceElement(ps1).plot(colormap="Accent", scalarsfunction=puttex('$\\alpha$'), num=150)

t = 0.25
z = 0.4
a1 = spaceElement([[0.5,t,0], [0.5,y-t,0]]).plot()
a2 = spaceElement([[0.5,0.5,z], [0.5,1,-0.6*z]]).plot()
a3 = spaceElement([[0.5,t,z], [0.5,y-t,z]]).plot()
at1 = spaceElement([0.5,0.5*y,0]).plotText("a")
at2 = spaceElement([0.5,0.5,z]).plotText("a")
at3 = spaceElement([0.5,0.5*y,z]).plotText("a")

av = [[a1, at1], [a2, at2], [a3, at3]]
for a in av:
    for b in a:
        b.visible = False
# av[0][0].visible = True
# av[0][1].visible = True

class Parascalar(object):
    p = 0
ps = Parascalar()
obs = len(av)
def my_function(vtk_obj, event):
    ps.p += 1
    if vtk_obj.GetKeyCode() == 'z':
        for a in av[ps.p%obs]:
            a.visible = True
        for a in av[(ps.p-1)%obs]:
            a.visible = False

v.scene.interactor.add_observer('KeyPressEvent', my_function)

print(u'按z可以变换形态')

mlab.show()