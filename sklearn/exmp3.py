#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: exmp3
@time: 2018/6/25  7:28
"""
# !/usr/bin/env python3
# coding=utf-8
"""
Decision Tree on the Basis of sklearn module
Author  :Chai Zheng
Blog    :http://blog.csdn.net/chai_zheng/
Github  :https://github.com/Chai-Zheng/Machine-Learning
Email   :zchaizju@gmail.com
Date    :2017.10.13
"""

import os
import time
import pydotplus
import numpy as np
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.model_selection import train_test_split

print('Step 1.Loading data...')
data = np.loadtxt("Wine.txt",delimiter=',')
x = data[:,1:14]
y = data[:,0].reshape(178,1)
X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.4)
print('---Loading and splitting completed.')

print('Step 2.Training...')
startTime = time.time()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train,Y_train)
print('---Training Completed.Took %f s.'%(time.time()-startTime))

print('Step 3.Testing...')
Y_predict = clf.predict(X_test)
matchCount = 0
for i in range(len(Y_predict)):
    if Y_predict[i] == Y_test[i]:
        matchCount += 1
accuracy = float(matchCount/len(Y_predict))
print('---Testing completed.Accuracy: %.3f%%'%(accuracy*100))

feature_name = ['Alcohol','Malic Acid','Ash','Alcalinity of Ash','Magnesium','Total Phenols',
                'Flavanoids','Nonflavanoid Phenols','Proantocyanins','Color Intensity','Hue',
                'OD280/OD315 of Diluted Wines','Proline']
target_name = ['Class1','Class2','Class3']

dot_data = StringIO()
tree.export_graphviz(clf,out_file = dot_data,feature_names=feature_name,
                     class_names=target_name,filled=True,rounded=True,
                     special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("WineTree.pdf")
print('Visible tree plot saved as pdf.')