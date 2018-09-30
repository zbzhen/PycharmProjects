#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: pdfToLongPngOneStep
@time: 2018/6/7  14:20
"""




import os
from wand.image import Image, Color
from PIL import Image as PImage

def convert_pdf(filename, outputfilename, resolution=160):
    all_pages = Image(filename=filename, resolution=resolution)

    pages = len(all_pages.sequence)
    x, y = all_pages.page[:2]
    p = PImage.new('RGBA', (x, y*pages), (255,255,255))

    # image_jpeg = all_pages.convert('png')
    # for i, img in enumerate(image_jpeg.sequence):
    #     img_page = Image(image=img)
    #     ff = open('tmp.png','wb')
    #     ff.write(img_page.make_blob('png'))
    #     ff.close()
    #     im = PImage.open('tmp.png')
    #     p.paste(im, (0, i*y, x, (i+1)*y))
    #     im.close()
    #     os.remove('tmp.png')

    all_pages = all_pages.convert('png')
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            # img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'
            img.save(filename='tmp.png')
            im = PImage.open('tmp.png')
            p.paste(im, (0, i*y, x, (i+1)*y))
            im.close()
            os.remove('tmp.png')
    p.save(outputfilename)
    return

putfilename = "D:\pdfs\长郡高一测试卷选讲.pdf"
outputfilename = "tt.png"
pages = convert_pdf(putfilename, outputfilename)

