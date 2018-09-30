#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: pngTogif
@time: 2018/5/4  19:41
"""

import imageio, os
images = []
# filenames=sorted((fn for fn in os.listdir('.') if fn.endswith('.png')))
filenames = []
for i in range(20):
    filenames += ["sinc"+str(i)+".png"]

for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('gif.gif', images,duration=0.2)