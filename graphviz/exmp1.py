#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: exmp1
@time: 2018/6/24  12:58

"""
# http://www.graphviz.org/doc/info/attrs.html
#https://www.cnblogs.com/AimeeKing/p/5021675.html
# 设置文档编码
import pygraphviz as pgv
from matplotlib import mathtext



G=pgv.AGraph(directed=True,strict=True,encoding='UTF-8')
G.graph_attr['epsilon']='0.001'
# G.graph_attr['splines']='polyline'
# 设置节点标签
nodeA = u'        \n        '
nodeB = u'技术总监'
nodeC = u'销售总监'
nodeD = u'销售经理'
nodeE = u'高级工程师'
nodeF = u'你好       '
nodeG = ' 4 '
# 图形中添加节点,设置节点形状、字体、字号属性
parser = mathtext.MathTextParser("Bitmap")
# 生成公式图片再插入这个公式图片，最后删除图片
parser.to_png('test2.png',
              u'    ' + r'$\left[\left\lfloor\frac{5}{\frac{\left(3\right)}{4}}y\right)\right]$'
              , color=u'black', fontsize=20, dpi=120)
G.add_node(nodeF,fontname="SimHei",image = 'test2.png', shape="rect", fontsize=20)
# G.add_node(nodeF,image = "test2.png", shape="rect", fontsize=50)
G.add_node(nodeA,fontname="SimHei", shape="rect", style="rounded", fontsize=30)
G.add_node(nodeB,fontname="SimSun", shape="diamond", fontsize=18)
G.add_node(nodeC,fontname="FangSong",shape="rect", fontsize=18)
G.add_node(nodeD,fontname="KaiTi", fontsize=18)
G.add_node(nodeE,fontname="Microsoft YaHei", shape="parallelogram", fontsize=18)
# G.add_node(nodeG, shape="point", width=0, height=0)
# 图形中添加节点关系
G.add_edge(nodeA,nodeB)
G.add_edge(nodeA,nodeC)
# G.add_edge(nodeB,nodeG, dir='none')
# G.add_edge(nodeA,nodeG)
G.add_edge(nodeB,nodeE)
G.add_edge(nodeC,nodeD)
G.add_edge(nodeC,nodeF)
G.add_edge(nodeE,nodeF)
G.add_edge(nodeC,nodeA)
G.add_edge(nodeE,nodeA)
G.add_edge(1,12)
# G.add_edge(1,nodeA)
nA = pgv.Node(G, nodeA)
nA.attr["color"] = 'red'

nB = G.get_node(nodeB)
nB.attr["color"] = 'blue'

edge = G.get_edge(nodeC,nodeA)
edge.attr["color"] = "green"
edge.attr["label"] = "green"
# G.add_edge(nodeE,edge)
# G.write("test.dot")
# 绘制节点Optional prog=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
G.layout('dot')
# 指定生产图形格式
G.draw('1.pdf',format='pdf')
# G.draw('1.png',format='png')
# print help(pgv)
import os
# os.remove('test2.png')