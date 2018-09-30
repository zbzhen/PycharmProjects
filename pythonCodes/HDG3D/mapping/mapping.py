#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/23 10:05
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : mapping.py
# @version : Python 2.7.6
def mapping1D(a, b):
    """
    line ab
     _______
    a       b
    :param a: line ab start point
    :param b: line ab end point
    :return: 1d linear transform Interval [-1,1]----> Line ab
    """
    # return lambda x: 0.5*(b-a)*x + 0.5*(b+a)
    return lambda x: 0.5*(b-a)*x + 0.5*(b+a)

def mapping2D(a, b, c, d, case=0):
    """
    Quadrilateral abcd
    d_______c
    |      |
    |      |
    |______|
    a      b
    :param a: Quadrilateral abcd start point
    :param b: Quadrilateral abcd second point
    :param c: Quadrilateral abcd third point
    :param d: Quadrilateral abcd end point
    :return: 2d transform Box [-1,1]^2----> Quadrilateral abcd
    """
    def retmap(x):
        if case == 0:
            ad = mapping1D(a, d)(x[1])  # not da
            bc = mapping1D(b, c)(x[1])
            return mapping1D(ad, bc)(x[0])
        else:
            ab = mapping1D(a, b)(x[0])
            dc = mapping1D(d, c)(x[0])  # not cd
            return mapping1D(ab, dc)(x[1])
    return retmap


def mapping3D(a, b, c, d, e, f, g, h, case=0):
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
    :param case:
    :return: 3d transform Cube [-1,1]^3----> Hexahedron abcd-efgh
    """
    def retmap(x):
        if case == 0:
            adhe = mapping2D(a, d, h, e)([x[1], x[2]])
            bcgf = mapping2D(b, c, g, f)([x[1], x[2]])
            return mapping1D(adhe, bcgf)(x[0])
        elif case == 1:
            abfe = mapping2D(a, b, f, e)([x[0], x[2]])
            dcgh = mapping2D(d, c, g, h)([x[0], x[2]])
            return mapping1D(abfe, dcgh)(x[1])
        elif case == 2:
            efgh = mapping2D(e, f, g, h)([x[0], x[1]])
            abcd = mapping2D(a, b, c, d)([x[0], x[1]])
            return mapping1D(abcd, efgh)(x[2])
        elif case == 10:
            ab = mapping1D(a, b)(x[0])
            dc = mapping1D(d, c)(x[0])
            hg = mapping1D(h, g)(x[0])
            ef = mapping1D(e, f)(x[0])
            return mapping2D(ab, dc, hg, ef)([x[1], x[2]])
        elif case == 11:
            ad = mapping1D(a, d)(x[1])
            bc = mapping1D(b, c)(x[1])
            fg = mapping1D(f, g)(x[1])
            eh = mapping1D(e, h)(x[1])
            return mapping2D(ad, bc, fg, eh)([x[0], x[2]])
        else:
            ae = mapping1D(a, e)(x[2])
            bf = mapping1D(b, f)(x[2])
            cg = mapping1D(c, g)(x[2])
            dh = mapping1D(d, h)(x[2])
            return mapping2D(ae, bf, cg, dh)([x[0], x[1]])
    return retmap




def mapping3D_interpolation(xHat, p):
    v0 = -(xHat[0]-1)*(xHat[1]-1)*(xHat[2]-1)
    v1 = (xHat[0]+1)*(xHat[1]-1)*(xHat[2]-1)
    v2 = -(xHat[0]+1)*(xHat[1]+1)*(xHat[2]-1)
    v3 = (xHat[0]-1)*(xHat[1]+1)*(xHat[2]-1)
    v4 = (xHat[0]-1)*(xHat[1]-1)*(xHat[2]+1)
    v5 = -(xHat[0]+1)*(xHat[1]-1)*(xHat[2]+1)
    v6 = (xHat[0]+1)*(xHat[1]+1)*(xHat[2]+1)
    v7 = -(xHat[0]-1)*(xHat[1]+1)*(xHat[2]+1)
    sum = v0*p[0] + v1*p[1] + v2*p[2] + v3*p[3] + \
          v4*p[4] + v5*p[5] + v6*p[6] + v7*p[7]
    return 0.125*sum




if __name__ == "__main__":
    import numpy as np
    from sympy import var, simplify, factor, expand
    for s in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x']:
        var([s+str(i) for i in range(3)])
    x = np.array([x0, x1, x2])

    print("Check that the various cases are all equivalent:")
    a = np.array([a0, a1, a2])
    b = np.array([b0, b1, b2])
    c = np.array([c0, c1, c2])
    d = np.array([d0, d1, d2])
    e = np.array([e0, e1, e2])
    f = np.array([f0, f1, f2])
    g = np.array([g0, g1, g2])
    h = np.array([h0, h1, h2])
    x = np.array([x0, x1, x2])
    print("2d case:")
    mp2dcase0 = simplify(mapping2D(a, b, c, d,0)(x))
    mp2dcase1 = simplify(mapping2D(a, b, c, d,1)(x))
    print(simplify(mp2dcase0 - mp2dcase1))
    print("3d case:")
    map3dmethod1 = simplify(mapping3D_interpolation(x, [a, b, c, d, e, f, g, h]))
    mp3dcase0 = simplify(mapping3D(a, b, c, d, e, f, g, h, 0)(x))
    mp3dcase1 = simplify(mapping3D(a, b, c, d, e, f, g, h, 1)(x))
    mp3dcase2 = simplify(mapping3D(a, b, c, d, e, f, g, h, 2)(x))
    mp3dcase10 = simplify(mapping3D(a, b, c, d, e, f, g, h, 10)(x))
    mp3dcase11 = simplify(mapping3D(a, b, c, d, e, f, g, h, 11)(x))
    mp3dcase12 = simplify(mapping3D(a, b, c, d, e, f, g, h, 12)(x))
    print(simplify(mp3dcase0 - mp3dcase1))
    print(simplify(mp3dcase0 - mp3dcase2))
    print(simplify(mp3dcase10 - mp3dcase11))
    print(simplify(mp3dcase10 - mp3dcase12))
    print(simplify(mp3dcase0 - mp3dcase10))
    print("Check the two methods are the same:")
    print(simplify(mp3dcase0 - map3dmethod1))
    print('\n')




    var(["e_"+str(i) for i in range(3)])
    var(["f_"+str(i) for i in range(3)])
    ee = [e_0, e_1, e_2]
    ff = [f_0, f_1, f_2]
    q0 = np.array([0,0,0])
    q1 = np.array([1,0,0])
    q3 = np.array([0,1,0])
    q4 = np.array([0,0,1])
    q2 = ee[0]*q1 + (1-ee[0])*q3
    q5 = ee[1]*q1 + (1-ee[1])*q4
    q7 = ee[2]*q3 + (1-ee[2])*q4
    q6 = ff[0]*q1 + ff[1]*q3 + ff[2]*q4
    method1 = mapping3D_interpolation(x, [q0, q1, q2, q3, q4, q5, q6, q7])
    method2 = mapping3D(q0, q1, q2, q3, q4, q5, q6, q7)(x)
    print('The mapping of Cube --> Tetrahedron:')
    for i in range(3):
        print(factor(method1)[i])
    print('The mapping of Cube --> Tetrahedron with \\alpha = [0,0,0,0,0,1]:')
    t = [0, 0, 0, 0, 0, 1]
    sub = {e_0:t[0], e_1:t[1], e_2:t[2], f_0:t[3], f_1:t[4], f_2:1-t[3]-t[4]}
    for i in range(3):
        tmp = factor(expand(method2[i]).subs(sub))
        print(tmp)
    t = [0.5, 0.5, 0.5, 1.0/3.0, 1.0/3.0, 1.0/3.0]
    sub = {e_0:t[0], e_1:t[1], e_2:t[2], f_0:t[3], f_1:t[4], f_2:1-t[3]-t[4]}
    print('The mapping of Cube --> Tetrahedron with \\alpha = [0.5, 0.5, 0.5, 1.0/3.0, 1.0/3.0, 1.0/3.0]:')
    for i in range(3):
        tmp = factor(expand(method2[i]).subs(sub))
        print(tmp)
    print("7.0/24.0 = ")
    print(7.0/24.0)
    print("1.0/7.0 = ")
    print(1.0/7.0)





