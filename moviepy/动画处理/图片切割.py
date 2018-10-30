#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 16:23
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 图片切割.py
# @version : Python 2.7.6
# -*-coding:utf-8-*-
from PIL import Image
im = Image.open("sample.pdf")
# 图片的宽度和高度
img_size = im.size
print("图片宽度和高度分别是{}".format(img_size))
'''
裁剪：传入一个元组作为参数
元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
'''
# 截取图片中一块宽和高都是250的
x = 100
y = 100
w = 250
h = 250
region = im.crop((x, y, x+w, y+h))
region.save("crop_test1.gif")

