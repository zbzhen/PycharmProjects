#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 15:18
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : ex1.py
# @version : Python 2.7.6
# https://python-graph-gallery.com/174-change-background-colour-of-venn-diagram/
from matplotlib import pyplot as plt
from matplotlib_venn import venn2

# Basic Venn
v = venn2( (10, 20, 10), alpha = 1 )

# Change Backgroud
plt.gca().set_axis_bgcolor('skyblue')
plt.gca().set_axis_on()

# Show it
plt.show()
