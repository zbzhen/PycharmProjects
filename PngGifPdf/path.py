#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: path
@time: 2018/6/8  0:19
"""
import os
import sys
print os.walk(r'D:\pdfs')
print 'os.getcwd()=',os.getcwd()
print 'sys.argv=',sys.argv
print 'sys.argv[0]=',sys.argv[0]
print 'os.path.realpath(sys.argv[0])=',os.path.realpath(sys.argv[0])
print 'os.path.split( os.path.realpath( sys.argv[0] ) )=',os.path.split( os.path.realpath( sys.argv[0] ) )
print 'os.path.split( os.path.realpath( sys.argv[0] ) )[0]=',os.path.split( os.path.realpath( sys.argv[0] ) )[0]
print 'os.path.split( os.path.realpath( sys.argv[0] ) )[0]=',os.path.split( os.path.realpath( sys.argv[0] ) )[-1]