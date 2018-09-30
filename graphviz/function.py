#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 23:33
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : function.py
# @version : Python 2.7.6

import pygraphviz as pgv
from matplotlib import mathtext

G=pgv.AGraph(directed=True,strict=True,encoding='UTF-8')
G.graph_attr['epsilon']='0.001'

node1 = u'定义域'
node2 = u'原函数'
node3 = u'导函数'
node4 = u'≥0'
node5 = u'≤0'
node6 = u'单调递增'
node7 = u'单调递减'
node8 = u'极值'
node9 = u'=0'
# G.add_node(node1,fontname="SimHei", shape="diamond", fontsize=20)
# G.add_node(node2,fontname="SimHei", shape="diamond", style="rounded", fontsize=30)
# G.add_node(node3,fontname="SimSun", shape="diamond", fontsize=18)
# G.add_node(node4,fontname="FangSong",shape="diamond", fontsize=18)
# G.add_node(node5,fontname="KaiTi", fontsize=18)
# G.add_node(node6,fontname="Microsoft YaHei", shape="diamond", fontsize=18)
# G.add_node(node7,fontname="Microsoft YaHei", shape="diamond", fontsize=18)
# G.add_node(node8,fontname="Microsoft YaHei", shape="diamond", fontsize=18)
# G.add_node(node9,fontname="Microsoft YaHei", shape="diamond", fontsize=18)

# G.add_edge(node1,node2)
# G.add_edge(node1,node3)
# G.add_edge(node2,node6)
# G.add_edge(node2,node7)
# G.add_edge(node2,node8)
# G.add_edge(node3,node4)
# G.add_edge(node3,node5)
# G.add_edge(node3,node9)
# G.add_edge(node4,node6)
# G.add_edge(node5,node7)
# G.add_edge(node8,node9)

import pygraphviz as pgv

A=pgv.AGraph()
# add some edges
A.add_edge(1,11)
A.add_edge(1,12)
A.add_edge(1,13)

# make a subgraph with rank='same'
B=A.add_subgraph([2, 21,22,23],name='s1',rank='same')
B.add_edge(2,21)
B.add_edge(2,22)
B.add_edge(2,23)
B.add_edge(21,11)
B.add_edge(22,12)
B.add_edge(23,13)
B.graph_attr['rank']='up'
# print(A.string()) # print dot file to standard output
A.layout('dot') # layout with dot
A.draw('subfoo.png') # write to file
