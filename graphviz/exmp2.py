#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: exmp2
@time: 2018/6/24  22:50
"""
#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import pygraphviz as pgv
# strict (no parallel edges)
# digraph
# with attribute rankdir set to 'LR'
A=pgv.AGraph(directed=True,strict=True,rankdir='LR')
# add node 1 with color red
A.add_node(1,color='red')
A.add_node(5,color='blue')
# add some edges
A.add_edge(1,2,color='green')
A.add_edge(2,3)
A.add_edge(1,3)
A.add_edge(3,4)
A.add_edge(3,5)
A.add_edge(3,6)
A.add_edge(4,6)
# adjust a graph parameter
A.graph_attr['epsilon']='0.001'
print(A.string()) # print dot file to standard output
A.layout('dot') # layout with dot
A.draw('foo.png') # write to file