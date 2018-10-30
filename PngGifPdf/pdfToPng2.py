#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: pdfToPng2
@time: 2018/6/6  8:52
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
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}-{}.png'.format(image_filename, i)
            image_filename = os.path.join(output_path, image_filename)

            img.save(filename=image_filename)

convert_pdf("sample.pdf", "")
