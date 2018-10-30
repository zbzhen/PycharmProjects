#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/20 13:34
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 二面角旋转图.py
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
y = 0.5
ps1 = np.array([[1,0,0], [1,y,0], [0,y,0],[0,0,0]])
plane1 = spaceElement(ps1).plot(colormap="Spectral", scalarsfunction=puttex('$\\alpha$'), num=150)


nums = 20
nums = (nums/2)*2+1
theta = np.linspace(0,np.pi,nums)
ys = y*np.cos(theta)
zs = y*np.sin(theta)




ps2 = [spaceElement([[1,ys[i],zs[i]],[1,0,0], [0,0,0], [0,ys[i],zs[i]]]) for i in range(len(theta))]
plane2 = [p.plot(colormap="Accent", scalarsfunction=puttex('$\\beta$',position='lefttop'), num=150) for p in ps2]


x = 0.35
spaceElement([1.2,0,0]).plotText('M')
spaceElement([-0.2,0,0]).plotText('N')
spaceElement([[1.2,0,0], [-0.2,0,0]]).plot()
O = spaceElement([x,0,0])
O.plotText('O')
A = spaceElement([x,0.7*y,0])
A.plotText('A')
OA = spaceElement(O, A).plot(num=2)
B = [spaceElement([x, 0.7*ys[i], 0.7*zs[i]]) for i in range(nums)]
OB = [spaceElement(O, b).plot(num=2) for b in B]


angleAOB = [mlab.plot3d(ys[:i]*0+x, 0.3*ys[:i], 0.3*zs[:i], tube_radius=0.005) for i in range(1,nums+1)]
angleAOB[nums/2].visible = False
angleAOB[nums/2] = mlab.plot3d([x,x,x], [0.3*y, 0.3*y, 0], [0,0.3*y,0.3*y], tube_radius=0.005)
Btext = [b.plotText('B') for b in B]

plots = [plane2, Btext, OB, angleAOB]
for plot in plots:
    for b in plot:
        b.visible = False
class Parascalar(object):
    p = 0
ps = Parascalar()

def my_function(vtk_obj, event):

    if vtk_obj.GetKeyCode() == 'z':
        ps.p += 1
    if vtk_obj.GetKeyCode() == 'x':
        ps.p -= 1
    for plot in plots:
        obs = len(plot)
        plot[ps.p%obs].visible = True
        plot[(ps.p-1)%obs].visible = False
        plot[(ps.p+1)%obs].visible = False


v.scene.interactor.add_observer('KeyPressEvent', my_function)

print(u'按z可以旋转')
print(u'要用英文输入法，单按一次Shfit键可以转换')

mlab.show()