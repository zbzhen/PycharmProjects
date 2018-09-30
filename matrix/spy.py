#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 15:22
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : spy.py
# @version : Python 2.7.6
import matplotlib.pylab as plt
import scipy.sparse as sps
A = sps.rand(10000,10000, density=0.00001)
# M = sps.csr_matrix(A)
M = A.tocsr()
plt.spy(M, marker="o", markersize=1)
plt.show()