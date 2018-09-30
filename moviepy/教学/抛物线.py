#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/25 19:32
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 抛物线.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy

# DRAW A FIGURE WITH MATPLOTLIB



fig_mpl, ax = plt.subplots(1,figsize=(8,8), facecolor='white')
ax.axis('off')
ax.set_xlim(-1.5,1.5)
ax.set_ylim(-1.5,1.5)
plt.annotate("",(1.4,0),(-1.4,0), arrowprops={"arrowstyle": "->"},color="black")
plt.annotate("",(0,1.4),(0,-1.4), arrowprops={"arrowstyle": "->"},color="black")
plt.text(1.4, 0,r'$x$', color="black", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='right')
plt.text(0, 1.4,r'$y$', color="black", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')
plt.text(0, 0,r'$0$', color="black", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')


# 下面三行绘制曲线
xx = np.linspace(-1.2, 1.2, 50) # the x vector
zz = lambda t: t*xx*xx # the (changing) z vector
line, = ax.plot(xx, zz(0), lw=1, color="blue")

# 下面2行绘制点
pp = lambda t: t*0.6*0.6
points, = ax.plot(0.6, pp(0), 'ro')


# ANIMATE WITH MOVIEPY (UPDATE THE CURVE FOR EACH t). MAKE A GIF.

# plt.show()


def make_frame_mpl(t):
    # plt.text(0.6, pp(t), r'$(a, \,ax^2\!)$', color="r", fontsize=25, ha="center", verticalalignment='top', horizontalalignment='left')
    line.set_ydata(zz(t))  # <= Update the curve
    points.set_ydata(pp(t))  # <= Update the curve
    ax.plot(xx, zz(t)+1, lw=1, color="red")
    return mplfig_to_npimage(fig_mpl) # RGB image of the figure

animation =mpy.VideoClip(make_frame_mpl, duration=1)  # 参数duration越大时间越长
animation.write_gif("pwx.gif", fps=10)  # 参数fps表示每秒会放映fps帧图片