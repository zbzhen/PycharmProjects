#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 18:44
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : ex1.py
# @version : Python 2.7.6
import cv2
from PIL import Image
import numpy as np

yuantu = "test1.png"
masktu = "test1-mask.png"

#使用opencv叠加图片
img1 = cv2.imread(yuantu)
img2 = cv2.imread(masktu)

alpha = 0.5
meta = 1 - alpha
gamma = 0
#cv2.imshow(‘img1‘, img1)
#cv2.imshow(‘img2‘, img2)
#image = cv2.addWeighted(img1,alpha,img2,meta,gamma)
image = cv2.add(img1, img2)

cv2.imshow('image', image)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("./mask.png",image)