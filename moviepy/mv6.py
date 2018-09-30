#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mv6
@time: 2018/4/16  23:19
"""
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
import moviepy.editor as mpy
import skimage.exposure as ske
import skimage.filter as skf

clip = mpy.VideoFileClip("svm.gif")
gray = clip.fx(mpy.vfx.blackwhite).to_mask()

def apply_effect(effect, label, **kw):
    """ Returns a clip with the effect applied and a top label"""
    filtr = lambda im: effect(im, **kw)
    new_clip = gray.fl_image(filtr).to_RGB()
    txt = (mpy.TextClip(label, font="Amiri-Bold", fontsize=25,
                        bg_color='white', size=new_clip.size)
           .set_position(("center"))
           .set_duration(1))
    return mpy.concatenate_videoclips([txt, new_clip])

equalized = apply_effect(ske.equalize_hist, "Equalized")
rescaled  = apply_effect(ske.rescale_intensity, "Rescaled")
adjusted  = apply_effect(ske.adjust_log, "Adjusted")
blurred   = apply_effect(skf.gaussian_filter, "Blurred", sigma=4)

clips = [equalized, adjusted, blurred, rescaled]
animation = mpy.concatenate_videoclips(clips)
animation.write_gif("sinc_cat.gif", fps=15)