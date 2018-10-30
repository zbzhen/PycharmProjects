#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 22:39
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 两平面.py
# @version : Python 2.7.6
from pointLinePlane import spaceElement, Frame, Axis, getcubepoints, setSCALING
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

# set mathtext
from matplotlib import mathtext
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei', "FangSong"][-1]
def puttex(text, dpi=120, fontsize=20):
    parser = mathtext.MathTextParser("bitmap")
    te, x = parser.to_mask(text, dpi=dpi, fontsize=fontsize)
    te = np.where(te>0,2,0)
    s,t = np.shape(te)
    def cf(x):
        xs,xt = np.shape(x)
        ans = x
        ans[xs-s:, :t] += te*0.003
        return ans
    return cf

# ----------------------------------------------
#   begin plot
# ----------------------------------------------
mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))

y = 1.4; z = 0.8
ps1 = np.array([[0,0,0], [1,0,0], [1,y,0], [0,y,0]])
ps2 = np.array([[0,0,z], [1,0,z], [1,y,z], [0,y,z]])
plane1 = spaceElement(ps1).plot(colormap="Accent", scalarsfunction=puttex('$\\alpha$'), num=150)
plane2 = spaceElement(ps2).plot(colormap="Accent", scalarsfunction=puttex('$\\beta$'), num=150)

B = spaceElement([-0.2, 0.5*y, 0])
A = spaceElement([1.2, 0.5*y, 0])
AB = spaceElement(A, B)
A.plotText("A")
B.plotText("B")
AB.plot()
mlab.show()