#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: 22222
@time: 2016-06-01 17:05
"""
import numpy as np
def nodbd(nod):
    ans = np.zeros_like(nod)
    ansx = np.zeros_like(nod)
    (m, n) = nod.shape
    #先对每一个单元进行循环
    for h in range(m):               #主（host）单元循环
        for i in range(n):
            k = 0
            for g in range(m):       #客体（gues）匹配单元循环
                if g != h:           #主客单元不能相同
                    for j in range(n):
                        a = (j+1)%n
                        if nod[h][i] == nod[g][a] and nod[h][(i+1)%n] == nod[g][j]:
                            ans[h][i] = g
                            ansx[h][i] = j
                            k = 1
                            break
                if k == 1:
                    break
            if k == 0:
                ans[h][i] = h
                ansx[h][i] = i
    return ans, ansx


def nod(H, L):     #将D等分成H*L个矩形元，H表示横着分割，L表示竖着分割。
    n = H*L        #n为总单元数
    ans = np.zeros((n, 4))
    for i in range(n):
            ans[i][0] = i/L + i
            ans[i][1] = i/L + i + 1
            ans[i][2] = i/L + i + L + 2
            ans[i][3] = i/L + i + L + 1
    return ans

H, L = 3, 4
a = nod(H, L)
print a
print nodbd(a)