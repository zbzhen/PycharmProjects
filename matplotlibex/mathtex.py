#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: mathtex
@time: 2018/7/7  9:29
"""
import matplotlib.mathtext as mathtext
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('image', origin='upper')

parser = mathtext.MathTextParser("Bitmap")
# help(mathtext.MathTextParser)
# # parser = mathtext.MathTextParser("Bitmap")
parser.rcParams['axes.unicode_minus'] = False
parser.to_png('test2.png',
              r'$\left[\left\lfloor\frac{5}{\frac{\left(3\right)}{4}} '
              r'y\right)\right]$', color=u'black', fontsize=14, dpi=200)

help(parser.to_png)

# rgba1, depth1 = parser.to_rgba(
#     r'IQ: $\sigma_i=15$', color='blue', fontsize=20, dpi=200)
# rgba2, depth2 = parser.to_rgba(
#     r'some other string', color='red', fontsize=20, dpi=200)
#
# fig = plt.figure()
# fig.figimage(rgba1, 100, 100)
# fig.figimage(rgba2, 100, 300)
# plt.savefig("test2.pdf")
# plt.show()