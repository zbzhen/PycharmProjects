#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: figinserttxt
@time: 2018/5/16  13:38
"""
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

image = Image.open("test3.png")
# draw = ImageDraw.Draw(image)
width, height = image.size
# draw.text((width/2, height/2), r'$K_1$', fill="#ff0000")
# image.save('newtest3.png')


fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
axes = plt.subplot(111)
axes.set_xlim(-1, 1)
axes.set_ylim(-1, 1)
axes.text(0,0,r"$K_1$",fontsize=28, color="b")
axes.set_xticks([])
axes.set_yticks([])
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['bottom'].set_color('none')
axes.spines['left'].set_color('none')

plt.savefig("11.png")
# plt.show()



def blend_two_images():
    img1 = Image.open( "test3.png ")
    img1 = img1.convert('RGBA')

    img2 = Image.open( "11.png")
    img2 = img2.convert('RGBA')

    img = Image.blend(img1, img2, 0.3)
    img.show()
    img.save("blend.png")

    return

def blend_two_images2():
    img1 = Image.open( "test3.png ")
    img1 = img1.convert('RGBA')

    img2 = Image.open( "11.png")
    img2 = img2.convert('RGBA')

    r, g, b, alpha = img2.split()
    alpha = alpha.point(lambda i: i>0 and 204)

    img = Image.composite(img2, img1, alpha)

    img.show()
    img.save( "blend2.png")

    return
# blend_two_images()
blend_two_images2()