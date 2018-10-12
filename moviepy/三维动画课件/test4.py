#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 19:49
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : test4.py
# @version : Python 2.7.6
# -*- coding: utf-8 -*-
from enthought.traits.api import *
from enthought.traits.ui.api import *
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene

class DemoApp(HasTraits):
    plotbutton = Button(u"绘图")
    scene = Instance(MlabSceneModel, ()) # mayavi场景

    view = View(
        VGroup(
            Item(name='scene',
                editor=SceneEditor(scene_class=MayaviScene), # 设置mayavi的编辑器
                resizable=True,
                height=250,
                width=400
            ),
            'plotbutton',
            show_labels=False
        ),
        title=u"在TraitsUI中嵌入Mayavi"
    )

    def _plotbutton_fired(self):
        self.plot()

    def plot(self):
        g = self.scene.mlab.test_mesh()

app = DemoApp()
app.configure_traits()