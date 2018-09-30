#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mv5
@time: 2018/4/16  23:18
"""
import moviepy.editor as mpy
import skimage.exposure as ske # rescaling, histogram eq.
import skimage.filter as skf # gaussian blur

clip = mpy.VideoFileClip("svm.gif")
gray = clip.fx(mpy.vfx.blackwhite).to_mask()

def apply_effect(effect, title, **kw):
    """ Returns a clip with the effect applied and a title"""
    filtr = lambda im: effect(im, **kw)
    new_clip = gray.fl_image(filtr).to_RGB()
    txt = (mpy.TextClip(title, font="Purisa-Bold", fontsize=15)
           .set_position(("center","top"))
           .set_duration(clip.duration))
    return mpy.CompositeVideoClip([new_clip,txt])

# Apply 4 different effects to the original animation
equalized = apply_effect(ske.equalize_hist, "Equalized")
rescaled  = apply_effect(ske.rescale_intensity, "Rescaled")
adjusted  = apply_effect(ske.adjust_log, "Adjusted")
blurred   = apply_effect(skf.gaussian_filter, "Blurred", sigma=4)

# Put the clips together on a 2x2 grid, and write to a file.
finalclip = mpy.clips_array([[ equalized, adjusted ],
                             [ blurred,   rescaled ]])
finalclip.write_gif("test2x2.gif", fps=20)