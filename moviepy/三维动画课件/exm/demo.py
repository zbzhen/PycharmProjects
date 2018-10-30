#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 21:06
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : demo.py
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



class FieldViewer(HasTraits):
    """三维标量场观察器"""

    # 三个轴的取值范围
    x0, x1 = Float(-5), Float(5)
    y0, y1 = Float(-5), Float(5)
    z0, z1 = Float(-5), Float(5)
    points = Int(50)  # 分割点数
    autocontour = Bool(True) # 是否自动计算等值面
    v0, v1 = Float(0.0), Float(1.0) # 等值面的取值范围
    contour = Range("v0", "v1", 0.5) # 等值面的值
    function = Str("x*x*0.5 + y*y + z*z*2.0") # 标量场函数
    function_list = [
        "x*x*0.5 + y*y + z*z*2.0",
        "x*y*0.5 + sin(2*x)*y +y*z*2.0",
        "x*y*z",
        "np.sin((x*x+y*y)/z)"
    ]
    plotbutton = Button(u"描画")
    scene = Instance(MlabSceneModel, ()) # mayavi场景

    view = View(
        HSplit(
            VGroup(
                "x0","x1","y0","y1","z0","z1",
                Item('points', label=u"点数"),
                Item('autocontour', label=u"自动等值"),
                Item('plotbutton', show_label=False),
            ),
            VGroup(
                Item('scene',
                    editor=SceneEditor(scene_class=MayaviScene), # 设置mayavi的编辑器
                    resizable=True,
                    height=300,
                    width=350
                ),
                Item('function',
                    editor=EnumEditor(name='function_list', evaluate=lambda x:x)),
                Item('contour',
                    editor=RangeEditor(format="%1.2f",
                        low_name="v0", high_name="v1")
                ), show_labels=False
            )
        ),
        width = 500, resizable=True, title=u"三维标量场观察器"
    )

    def _plotbutton_fired(self):
        self.plot()


    # def _autocontour_changed(self):
    #     "自动计算等值平面的设置改变事件响应"
    #     if hasattr(self, "g"):
    #         self.g.contour.auto_contours = self.autocontour
    #         if not self.autocontour:
    #             self._contour_changed()
    #
    #
    # def _contour_changed(self):
    #     "等值平面的值改变事件响应"
    #     if hasattr(self, "g"):
    #         if not self.g.contour.auto_contours:
    #             self.g.contour.contours = [self.contour]


    def plot(self):
        # mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
        # mlab.options.backend = 'envisage'
        setSCALING(4)
        mlab.clf()
        v = mlab.gcf(engine=None)
        v.scene.background = (1, 1, 1)
        v.scene.foreground = (0, 0, 1)

        Axis(1.5,1.5,1.5).plot(arraymode="2darrow")

        A = spaceElement([1,0,0])
        B = spaceElement([0,1,0])
        C = spaceElement([0,0,1])
        P = spaceElement([0,0,0])
        D = spaceElement([0.5,0.5,0])


        spaceElement(C, D).plot(linestyle="dashed", color=(0,1,0))

        # spaceElement(A, B).plot()

        D.plot()
        A.plot()
        B.plot()
        C.plot()
        aa = A.plotText("A",0.1)

        # B.plotText("B")
        # C.plotText("C")
        t = D.plotText("D")
        # spaceElement(A, B, C).plotLine()

        ps = getcubepoints()
        a = [spaceElement(p) for p in ps]
        Frame(a[:4], a[4:]).plot()
        # spaceElement(a[0],a[2],a[4],a[6]).plotLine()

        spaceElement(a[0],a[2],a[6],a[4]).plot(colormap="Spectral", opacity=self.contour)
        ABC = spaceElement(A, B, C)
        abc = ABC.plot(colormap="Accent", opacity=self.contour)
        ABC.getPerpendicularLine(a[0]).plot()
        # # print spaceElement(A, B, C).getDistanceFromPoint(a[7])
        # spaceElement(A, C).getParallelLine(D).plot()
        # spaceElement(A, C).getPerpendicularLine(D).plot()


        # And display text
        vtext = tvtk.VectorText()
        vtext.text = 'm'
        text_mapper = tvtk.PolyDataMapper()
        configure_input_data(text_mapper, vtext.get_output())
        vtext.update()
        p2 = tvtk.Property(color=(0, 0.3, 0.3))
        text_actor = tvtk.Follower(mapper=text_mapper, property=p2)
        text_actor.position = (0, 0, 0)
        v.scene.add_actor(text_actor)

        def my_function(vtk_obj, event):
            if vtk_obj.GetKeyCode() == 'z':
                # abc.actor.visible = False
                abc.mlab_source.reset(opacit=1)
                print "helloz"
            if vtk_obj.GetKeyCode() == 'x':
                abc.actor.visible = True
                print "helloa"

        v.scene.interactor.add_observer('KeyPressEvent', my_function)
        camera = v.scene.camera
        camera.parallel_scale = 90

        # camera = v.scene.camerav
        # camera.yaw(45)

app = FieldViewer()
app.configure_traits()






