#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: exmp4
@time: 2018/6/25  7:31
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
import pydotplus
iris = load_iris()#载入数据集
clf = tree.DecisionTreeClassifier()#算法模型
clf = clf.fit(iris.data, iris.target)#模型训练
dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("iris.pdf")#写入pdf