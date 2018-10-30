#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/20 10:26
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 直线与直线1.py
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
def puttex(text, dpi=120, fontsize=20, position='leftbottom'):
    parser = mathtext.MathTextParser("bitmap")
    te, x = parser.to_mask(text, dpi=dpi, fontsize=fontsize)
    te = np.where(te>0,2,0)
    s,t = np.shape(te)
    def cf(x):
        xs,xt = np.shape(x)
        ans = x*0
        if position == 'leftbottom':
            ans[xs-s:, :t] += te*0.003
        elif position == 'lefttop':
            ans[0:s, :t] += te*0.003
        return ans
    return cf

# ----------------------------------------------
#   begin plot
# ----------------------------------------------
mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))

y = 1.4
ps1 = np.array([[0,0,0], [1,0,0], [1,y,0], [0,y,0]])
plane1 = spaceElement(ps1).plot(colormap="Accent", scalarsfunction=puttex('$\\alpha$'), num=150)

t = 0.25
z = 0.8
spaceElement([[0.8,t,0], [0.8,y-t,0]]).plot()
spaceElement([0.8,0.5*y,0]).plotText('a')
spaceElement([[0.2,0.5,z], [0.2,1,-0.6*z]]).plot()
spaceElement([0.2,0.5,z]).plotText('b')

mlab.show()