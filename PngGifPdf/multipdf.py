#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: multipdf
@time: 2018/6/5  23:55
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import os
import os.path
from pyPdf import PdfFileReader,PdfFileWriter
import time
time1=time.time()


# 使用os模块walk函数，搜索出某目录下的全部pdf文件
######################获取同一个文件夹下的所有PDF文件名#######################
def getFileName(filepath):
    file_list = []
    for root,dirs,files in os.walk(filepath):
        for filespath in files:
            # print(os.path.join(root,filespath))
            file_list.append(os.path.join(root,filespath))
        # print root,dirs,files,"------"

    return file_list



##########################合并同一个文件夹下所有PDF文件########################
def MergePDF(filepath,outfile):
    output=PdfFileWriter()
    outputPages=0
    pdf_fileName=getFileName(filepath)
    print pdf_fileName
    for each in pdf_fileName:
        print each
        # 读取源pdf文件
        input = PdfFileReader(file(each, "rb"))

        # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
        if input.isEncrypted == True:
            input.decrypt("map")

        # 获得源pdf文件中页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        print pageCount

        # 分别将page添加到输出output中
        for iPage in range(0, pageCount):
            output.addPage(input.getPage(iPage))


    print "All Pages Number:"+str(outputPages)
    # 最后写pdf文件

    outputStream=file(filepath+outfile,"wb")
    output.write(outputStream)
    outputStream.close()
    print "finished"



if __name__ == '__main__':
    file_dir = r'D:\pdfs'
    out="\\result1.pdf"
    pdf_fileName=getFileName(file_dir)
    print pdf_fileName
    # MergePDF(file_dir,out)
    # time2 = time.time()
    # print u'总共耗时：' + str(time2 - time1) + 's'