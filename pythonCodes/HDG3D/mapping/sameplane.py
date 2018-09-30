#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/23 16:48
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : sameplane.py
# @version : Python 2.7.6
from mapping import mapping1D, mapping2D, mapping3D
import numpy as np
def ja3D(a, b, c, d, e, f, g, h):
    """
    Hexahedron abcd-efgh
        top efgh
       h _______g
        |      |
        |      |
        |______|
       e       f
    bottom abcd
    d_______c
    |      |
    |      |
    |______|
    a      b
    ------------------
    Faces of attached vertices
    bottom abcd, top efgh;
    left adhe, right bcgf;
    behind abfe, front dcgh.
    :return: 3d jacobian of transform Cube [-1,1]^3----> Hexahedron abcd-efgh
    """
    def retja(x):
        adhe = mapping2D(a, d, h, e)([x[1], x[2]])
        bcgf = mapping2D(b, c, g, f)([x[1], x[2]])
        abfe = mapping2D(a, b, f, e)([x[0], x[2]])
        dcgh = mapping2D(d, c, g, h)([x[0], x[2]])
        abcd = mapping2D(a, b, c, d)([x[0], x[1]])
        efgh = mapping2D(e, f, g, h)([x[0], x[1]])
        return np.cross(bcgf - adhe, dcgh - abfe).dot(efgh - abcd)
    return retja


if __name__ == "__main__":
    import numpy as np
    from sympy import var, simplify, factor, expand, diff
    for s in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x']:
        var([s+str(i) for i in range(3)])
    x = np.array([x0, x1, x2])
    # x = np.array([0, 0, 0])

    var(["ze_"+str(i) for i in range(3)])
    var(["zf_"+str(i) for i in range(3)])
    ee = [ze_0, ze_1, ze_2]
    ff = [zf_0, zf_1, zf_2]
    # ee = [0.5, 0.5, 0.5]
    # ff = [1.0/3.0, 1.0/3.0, 1.0/3.0]
    q0 = np.array([0,0,0])
    q1 = np.array([1,0,0])
    q3 = np.array([0,1,0])
    q4 = np.array([0,0,1])
    q2 = ee[0]*q1 + (1-ee[0])*q3
    q5 = ee[1]*q1 + (1-ee[1])*q4
    q7 = ee[2]*q3 + (1-ee[2])*q4
    q6 = ff[0]*q1 + ff[1]*q3 + ff[2]*q4

    ja = ja3D(q0, q1, q2, q3, q4, q5, q6, q7)(x)

    ja = expand(ja)

    jax0 = diff(ja, x0).subs({x0:1})

    print(jax0)