#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: pdfToLongPng
@time: 2018/6/6  14:36
"""

import os
from wand.image import Image, Color


def convert_pdf(filename, output_path, resolution=150):
    """ Convert a PDF into images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    all_pages = Image(filename=filename, resolution=resolution)
    print all_pages.page
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'
            image_filename = '{}-{}.png'.format("tmp", i)
            img.save(filename=image_filename)

    return len(all_pages.sequence)




def pngsToLongPng(imfiles, outputfilename):
    from PIL import Image
    num = len(imfiles)
    im = Image.open(imfiles[0])
    x, y = im.size
    print x,y
    p = Image.new('RGBA', (x, y*num), (255,255,255))
    for i in range(num):
        im = Image.open(imfiles[i])
        p.paste(im, (0, i*y, x, (i+1)*y))
    p.save(outputfilename)
    return



name = "长郡高一测试卷选讲"
pages = convert_pdf("D:\pdfs\\"+name+".pdf", "")
imfiles = ['{}-{}.png'.format("tmp", i) for i in range(pages)]

outputfilename = "yy.png"
pngsToLongPng(imfiles, outputfilename)
for file in imfiles:
    os.remove(file)

