#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mv4
@time: 2018/4/16  22:57
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm # sklearn = scikit-learn
from sklearn.datasets import make_moons
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

X, Y = make_moons(50, noise=0.1, random_state=2) # semi-random data

fig, ax = plt.subplots(1, figsize=(4, 4), facecolor=(1,1,1))
fig.subplots_adjust(left=0, right=1, bottom=0)
xx, yy = np.meshgrid(np.linspace(-2,3,500), np.linspace(-1,2,500))

def make_frame(t):
    ax.clear()
    ax.axis('off')
    ax.set_title("SVC classification", fontsize=16)

    classifier = svm.SVC(gamma=2, C=1)
    # the varying weights make the points appear one after the other
    weights = np.minimum(1, np.maximum(0, t**2+10-np.arange(50)))
    classifier.fit(X, Y, sample_weight=weights)
    Z = classifier.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, cmap=plt.cm.bone, alpha=0.8,
                vmin=-2.5, vmax=2.5, levels=np.linspace(-2,2,20))
    ax.scatter(X[:,0], X[:,1], c=Y, s=50*weights, cmap=plt.cm.bone)

    return mplfig_to_npimage(fig)

animation = VideoClip(make_frame, duration = 7)
animation.write_gif("svm.gif", fps=15)