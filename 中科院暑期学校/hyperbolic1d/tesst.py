#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/27 19:16
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : tesst.py
# @version : Python 2.7.6
import numpy as np
mathbbM = np.mat([[1.0,             0],
                    [0,        1.0/12.0]])
Minverse = mathbbM.I

mathbbD = np.array([[0,        0],
                    [1.0,      0]])

mathbbE = np.array([[1,      0.5],
                    [0.5,   0.25]])

mathbbF = np.array([[1,      0.5],
                    [-0.5, -0.25]])

print Minverse.dot(mathbbF)