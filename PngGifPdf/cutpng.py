#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 16:30
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : cutpng.py
# @version : Python 2.7.6
from PIL import Image
im = Image.open("test3.png")
img_size = im.size
x = 100
y = 100
w = 250
h = 250
region = im.crop((x, y, x+w, y+h))
region.save("newtest3.png")
