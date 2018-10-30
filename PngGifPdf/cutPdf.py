#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 16:38
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : cutPdf.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
from wand.image import Image, Color

def convert_pdf(filename, output_path="", resolution=150):
    """ Convert a PDF into images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    all_pages = Image(filename=filename, resolution=resolution)
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}.png'.format(image_filename)
            image_filename = os.path.join(output_path, image_filename)

            img.save(filename=image_filename)

convert_pdf("sample.pdf")



from PIL import Image
im = Image.open("sample.png")
img_size = im.size
x = 100
y = 100
w = 250
h = 250
region = im.crop((x, y, x+w, y+h))
region.save("newsample.png")



plt.figure(dpi=100,facecolor="white")
axes = plt.subplot(111)
axes.set_xticks([])
axes.set_yticks([])
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['bottom'].set_color('none')
axes.spines['left'].set_color('none')
fig = mpimg.imread("newsample.png")
plt.imshow(fig)
plt.savefig("newsample.pdf")
plt.show()