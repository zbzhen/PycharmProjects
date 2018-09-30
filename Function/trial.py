#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: trial
@time: 2018/1/31  14:33
"""
import numpy as np
class Trial2DR(object):
    def __init__(self, xhat1d):
        self.deg = len(xhat1d) -1
        self.freetoquad = self.freedomToQuad()
        self.quadtofree = self.quadToFreedom()
        self.nodecoord = np.array(np.meshgrid(xhat1d, xhat1d))
        pass

    # 只是针对矩形
    def freedomToQuad(self):
        pd = self.deg + 1
        ed = self.deg - 1
        ct = self.deg * 4
        index = [0]*(pd*pd)
        index[1] = pd-1
        index[2] = pd*pd-1
        index[3] = pd*(pd-1)
        for i in range(1, self.deg):
            index[3     +i] = index[0]+i
            index[3  +ed+i] = index[1]+pd*i
            index[3+2*ed+i] = index[2]-i
            index[3+3*ed+i] = index[0]+pd*(ed-i+1)
        for i in range(1, self.deg):
            for j in range(1, self.deg):
                index[ct] = i*pd+j
                ct += 1
        return np.array(index)

    def quadToFreedom(self):
        index = [0]*((self.deg + 1)*(self.deg + 1))
        for i, vi in enumerate(self.freetoquad):
            index[vi] = i
        return np.array(index)


if __name__ == "__main__":
    tri2dR = Trial2DR([-1,-0.3, 0.3, 1])
    x,y = tri2dR.nodecoord
    print x*y
    print tri2dR.quadtofree
    print tri2dR.freetoquad