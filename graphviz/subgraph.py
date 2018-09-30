#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: subgraph
@time: 2018/6/24  22:56
"""
#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import pygraphviz as pgv

A=pgv.AGraph()
# add some edges
A.add_edge(1,2)
A.add_edge(2,3)
A.add_edge(1,3)
A.add_edge(3,4)
A.add_edge(3,5)
A.add_edge(3,6)
A.add_edge(4,6)
# make a subgraph with rank='same'
B=A.add_subgraph([4,5,6],name='s1',rank='same')
# B.graph_attr['rank']='left'
# print(A.string()) # print dot file to standard output
A.layout('dot') # layout with dot
A.draw('subfoo.png') # write to file