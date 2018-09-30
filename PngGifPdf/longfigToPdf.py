#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: longfigToPdf
@time: 2018/6/6  0:54
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from PIL import Image

from pyPdf import PdfFileReader,PdfFileWriter
from reportlab.pdfgen import canvas
import gc


# 先分解图片，再把每张图片变成pdf，最后合成pdf
def splitimage(src, rownum=1, colnum=1):
    img = Image.open(src)
    w, h = img.size
    wx, hx = 1323, 1871
    s = os.path.split(src)
    fn = s[1].split('.')
    basename = fn[0]
    ext = fn[-1]

    rowheight = h // rownum
    colwidth = w // colnum
    output=PdfFileWriter()
    num = 0
    for r in range(rownum):
        for c in range(colnum):
            box = (c * colwidth, r * rowheight, (c + 1) * colwidth, (r + 1) * rowheight)
            img.crop(box).save('tmp.png', ext)
            cc = canvas.Canvas("tmp_"+str(num)+".pdf", pagesize=(wx, hx))
            cc.drawImage("tmp.png", 0, 0, wx, hx)
            cc.save()
            input = PdfFileReader(file("tmp_"+str(num)+".pdf", "rb"))
            output.addPage(input.getPage(0))
            num += 1
    outputStream=file(basename+".pdf","wb")
    output.write(outputStream)
    outputStream.close()
    return num

num = splitimage("tt.png", 16)


gc.collect()
if os.path.exists("tmp.png"):
    os.remove("tmp.png")
for i in range(num):
    filename = "tmp_"+str(i)+".pdf"
    if os.path.exists(filename):
        os.remove(filename)









# import os
# from reportlab.pdfgen import canvas
#
# f_jpg = 'tt_0.png'
# print f_jpg
# def conpdf(f_jpg):
#     f_pdf = f_jpg+'.pdf'
#     (w, h) = 1323, 1871
#     c = canvas.Canvas(f_pdf, pagesize=(w, h))
#     c.drawImage(f_jpg, 0, 0, w, h)
#     c.save()
#     print "okkkkkkkk."
#     return
#
# conpdf(f_jpg)