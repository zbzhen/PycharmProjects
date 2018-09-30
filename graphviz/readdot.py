#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: readdot
@time: 2018/6/25  8:39
"""

# http://blog.jobbole.com/94472/

import pygraphviz as pgv
G=pgv.AGraph(directed=True,strict=True,encoding='UTF-8')
G.graph_attr['epsilon']='0.001'
G.read("test1.dot")
# 绘制节点
G.layout('dot')
# 指定生产图形格式
G.draw('2.pdf',format='pdf')