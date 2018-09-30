#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: EX4
@time: 2018/4/26  10:08
"""
import numpy
from mayavi.mlab import *

def test_mesh():
    """A very pretty picture of spherical harmonics translated from
    the octaviz example."""
    pi = numpy.pi
    cos = numpy.cos
    sin = numpy.sin
    dphi, dtheta = pi / 250.0, pi / 250.0
    [phi, theta] = numpy.mgrid[0:pi + dphi * 1.5:dphi,
                               0:2 * pi + dtheta * 1.5:dtheta]
    m0 = 4
    m1 = 3
    m2 = 2
    m3 = 3
    m4 = 6
    m5 = 2
    m6 = 6
    m7 = 4
    r = sin(m0 * phi) ** m1 + cos(m2 * phi) ** m3 + \
        sin(m4 * theta) ** m5 + cos(m6 * theta) ** m7
    x = r * sin(phi) * cos(theta)
    y = r * cos(phi)
    z = r * sin(phi) * sin(theta)

    return mesh(x, y, z, colormap="Accent")

test_mesh()
show()