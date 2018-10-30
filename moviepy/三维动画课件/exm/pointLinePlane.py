#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/9 12:46
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : pointLinePlane.py
# @version : Python 2.7.6
import numpy as np
from mayavi import mlab

SCALING = 1.0
def setSCALING(x):
    global SCALING
    SCALING = x
    return

class Point(object):
    def __init__(self, coord, pl=mlab):
        self.pl = pl
        self.coord = np.array(coord)*1.0
        self.coords = self.coord
        self.SCALING = SCALING
        self.plotCoords = []

    def plot(self, scale_factor=0.03, color=(1.0, 0.0, 0.0)):
        x, y, z = self.coord*self.SCALING
        scale_factor *= abs(self.SCALING)
        self.plotCoords = np.array([x,y,z])
        result = self.pl.points3d(x, y, z, scale_factor=scale_factor, color=color)
        return result

    def plotText(self, name, width=0.03):
        x, y, z = self.coord*self.SCALING
        # width *= np.sqrt(abs(SCALING))
        result = self.pl.text(x, y, name, z=z, width=width)
        return result

    def getLine(self, friend):
        return Line([self.coord, friend.coord], self.pl)

    def getPlane(self, friend):
        if isinstance(friend, Line):
            return Plane([self.coord, friend.coords[0], friend.coords[1]], self.pl)
        elif isinstance(friend[0], Point):
            return Plane([self.coord, friend[0].coord, friend[1].coord], self.pl)
        else:
            ValueError("friends must be Line or Points")




class Line(object):
    def __init__(self, coords, pl=mlab):
        self.pl = pl
        self.coords = np.array(coords)*1.0
        self.SCALING = SCALING
        self.plotCoords = []


    def plot(self, linesize=0.005, color=(0.2, 0.2, 0.2), linestyle="solid", num=2):
        x, y, z = self.SCALING*self.coords.copy().T
        if linestyle == "solid":
            x = np.linspace(x[0], x[1], num)
            y = np.linspace(y[0], y[1], num)
            z = np.linspace(z[0], z[1], num)
            self.plotCoords = np.array([x,y,z])
            result = self.pl.plot3d(x, y, z, tube_radius=linesize, color=color)
            return result
        else:
            num = num*3 + 5
            num = num/2*2+1
            for i in range(num):
                xx = np.array([x[0]+1.0/num*i*(x[1]-x[0]), x[0]+1.0/num*(i+1)*(x[1]-x[0])])
                yy = np.array([y[0]+1.0/num*i*(y[1]-y[0]), y[0]+1.0/num*(i+1)*(y[1]-y[0])])
                zz = np.array([z[0]+1.0/num*i*(z[1]-z[0]), z[0]+1.0/num*(i+1)*(z[1]-z[0])])
                if i%2 == 0:
                    self.pl.plot3d(xx,yy,zz, tube_radius=linesize*0.2, color=color)
        return

    def plotArrow(self, color=(1,0,0), arraymode='2darrow'):
        x1 = self.coords[0].copy()
        x2 = self.coords[1].copy()
        x, y, z = x1*self.SCALING
        u, v, w = x2*self.SCALING
        tent = [x, u, y, v, z, w]
        result = self.pl.quiver3d(x,y,z,u,v,w, extent=tent, color=color, mode=arraymode)
        return result

    def length(self):
        ab = self.coords[1] - self.coords[0]
        return np.sqrt(ab.dot(ab))

    def direction(self):
        ab = self.coords[1] - self.coords[0]
        return ab

    def getPoint(self, i):
        return Point(self.coords[i], self.pl)

    def getCenterPoint(self):
        return Point((self.coords[0]+self.coords[1])*0.5, self.pl)

    def getPlane(self, point):
        return spaceElement(self.getPoint(0), self.getPoint(1), point)

    def getParallelLine(self, point, tL=0.5, tR=0.5):
        L, R = self.coords
        p = point.coord
        pR = p+tR*self.direction()
        pL = p-tL*self.direction()
        return Line([pL, pR])

    def getPerpendicularLine(self, point):
        L, R = self.coords
        p = point.coord
        LR = self.direction()
        t = LR.dot(p-L)*1.0/LR.dot(LR)
        return Line([p, L+t*LR])


class Plane(object):
    def __init__(self, coords, pl=mlab):
        self.pl = pl
        self.coords = np.array(coords)*1.0
        self.poly = len(self.coords)
        if self.poly == 3:
            self.coords = np.vstack((self.coords, self.coords[-1]))
        self.SCALING = SCALING
        self.plotCoords = []

    def plot(self, transparent=True, colormap="black-white", opacity=0.8, scalarsfunction=lambda x: x, num=20):
        xhat = np.mgrid[-1:1:num*1j, -1:1:num*1j]
        mp = lambda a, b, x: np.array([0.5*(b[i]-a[i])*x + 0.5*(b[i]+a[i]) for i in [0,1,2]])
        a,b,c,d = self.coords.copy()*self.SCALING
        ad = mp(a, d, xhat[1])
        bc = mp(b, c,xhat[1])
        x,y,z = mp(ad, bc,xhat[0])
        self.plotCoords = np.array([x,y,z])
        result = mlab.mesh(x, y, z, transparent=transparent,
                           colormap=colormap, opacity=opacity, scalars=scalarsfunction(z))
        return result




    def plotLine(self, linesize=0.001, color=(0.2, 0.2, 0.2), linestyle="solid", num=20):
        linesize *= abs(self.SCALING)
        if self.poly==3:
            spaceElement([self.coords[0],self.coords[1]]).plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
            spaceElement([self.coords[0],self.coords[-1]]).plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
            spaceElement([self.coords[1],self.coords[-1]]).plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
        if self.poly==4:
            spaceElement([self.coords[0],self.coords[1]]).plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
            spaceElement([self.coords[0],self.coords[2]]).plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
            spaceElement([self.coords[-1],self.coords[1]]).plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
            spaceElement([self.coords[-1],self.coords[2]]).plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
        return

    def getPoint(self, i):
        return Point(self.coords[i], self.pl)

    def getCenterPoint(self):
        p = np.array([0,0,0])
        for i in range(self.poly):
            p = self.coords[i] + p
        return Point(p*(1.0/self.poly), self.pl)


    def getNorm(self):
        p0 = self.coords[0]
        p1 = self.coords[1]
        p2 = self.coords[2]
        return np.cross(p1-p0, p2-p1)

    def getDistanceFromPoint(self, point):
        p0 = self.coords[0]
        p = point.coord
        norm = self.getNorm()
        norm *= 1.0/np.sqrt(np.dot(norm, norm))   # unitization
        ans = np.dot(norm, p-p0)
        return abs(ans)


    def getPerpendicularLine(self, point):
        p0 = self.coords[0]
        p = point.coord
        norm = self.getNorm()
        norm *= 1.0/np.sqrt(np.dot(norm, norm))   # unitization
        t = np.dot(norm, p-p0)
        perpendicular = p - t*norm
        return Line([p, perpendicular])



class Frame(object):
    def __init__(self, points1, points2, pl=mlab):
        self.points1 = points1
        self.points2 = points2
        self.pl = pl
        self.SCALING = SCALING

    def plot(self, linesize=0.01, color=(0.2, 0.2, 0.2),  num=2, linestyle="solid"):
        # p = []
        # for i in self.points1:
        #     p += [i.coords.tolist()]
        # for i in self.points2:
        #     p += [i.coords.tolist()]
        # points = np.array(p)*SCALING*1.0
        # index = []
        # if len(self.points1) == 4 and len(self.points2) == 4:
        #     index = [0,1,2,3,0,4,5,6,7,4,0,1,5,6,2,3,7]
        # elif len(self.points1) == 3 and len(self.points2) == 3:
        #     index = [0,1,2,0,3,4,5,3,0,1,4,5,2]
        # elif len(self.points1) == 1 and len(self.points2) == 3:
        #     index = [0,1,2,3,1,0,2,3,0]
        # elif len(self.points1) == 1 and len(self.points2) == 4:
        #     index = [0,1,2,3,4,1,0,2,3,0,4]
        # else:
        #     ValueError("data bug")
        # x = []
        # y = []
        # z = []
        # for i in range(0,len(index)-1):
        #     Li = index[i]
        #     Ri = index[i]
        #     x += np.linspace(points[Li][0], points[Ri][0], num=num).tolist()
        #     y += np.linspace(points[Li][1], points[Ri][1], num=num).tolist()
        #     z += np.linspace(points[Li][2], points[Ri][2], num=num).tolist()
        # return self.pl.plot3d(x, y, z, tube_radius=linesize*0.5, color=color)
        linesize *= abs(self.SCALING)
        if isinstance(self.points1, (list, tuple)):
            poly1 = len(self.points1)
        else:
            poly1 = 1
            self.points1 = [self.points1]
        poly2 = len(self.points2)
        for i in range(poly2):
            line2 = spaceElement(self.points2[i], self.points2[(i+1)%poly2])
            line2.plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
            line1 = spaceElement(self.points1[i%poly1], self.points2[i])
            line1.plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
        if poly1 == poly2:
            for i in range(poly2):
                line1 = spaceElement(self.points1[i], self.points1[(i+1)%poly2])
                line1.plot(linesize=linesize, color=color, linestyle=linestyle, num=num)
        else:
            ValueError("data bug")
        return

    def plotFace(self, transparent=True, colormap="black-white", scalars=None, opacity=0.8):
        if isinstance(self.points1, (list, tuple)):
            poly1 = len(self.points1)
        else:
            poly1 = 1
            self.points1 = [self.points1]
        if poly1 < 2:
            spaceElement(self.points1[0]).plot()
        else:
            spaceElement(self.points1).plot(transparent=transparent, colormap=colormap, opacity=opacity)
        spaceElement(self.points2).plot(transparent=transparent, colormap=colormap, opacity=opacity)
        poly2 = len(self.points2)
        if poly1 == 1:
            for i in range(poly2):
                plane = spaceElement(self.points1[0], self.points2[i%poly2], self.points2[(i+1)%poly2])
                plane.plot(transparent=transparent, colormap=colormap, opacity=opacity)
        elif poly1 == poly2:
            for i in range(poly2):
                plane = spaceElement(self.points1[i%poly2], self.points2[i%poly2], self.points2[(i+1)%poly2],self.points1[(i+1)%poly2])
                plane.plot(transparent=transparent, colormap=colormap, opacity=opacity)
        else:
            ValueError("data bug")
        return


def spaceElement(*args):
    if len(args) == 0:
        ValueError("space at least one variable")
    x = args[0]
    if isinstance(x, (list, tuple, np.ndarray)):  # 第一个参数是列表
        if isinstance(x[0], (list, tuple, np.ndarray)):
            if len(x) == 1:
                return Point(x)
            elif len(x) == 2:
                return Line(x)
            else:
                return Plane(x)
        elif isinstance(x[0], (int, float)):
            return Point(x)
        else:
            if len(x) == 1:
                return Point([p.coord for p in x])
            elif len(x) == 2:
                return Line([p.coord for p in x])
            else:
                return Plane([p.coord for p in x])

    else:
        if isinstance(x, (int, float)):
            return Point(args)
        elif len(args) == 1:
            return x
        elif len(args) == 2:
            return Line([p.coord for p in args])
        elif len(args) >= 3:
            return Plane([p.coord for p in args])



class Axis(object):
    def __init__(self, x=3, y=3, z=3, center=(0.0,0.0,0.0), pl=mlab):
        self.x = x
        self.y = y
        self.z = z
        self.center = center
        self.pl = pl
        self.SCALING = SCALING

    def plot(self, linesize=0.0005, textwidth=0.03, arraymode="arrow"):
        a, b, c = self.x, self.y, self.z
        # textwidth *= (abs(SCALING))**0.1
        # textwidth *= 1
        linesize *= abs(self.SCALING)**0.5
        ct = np.array(self.center)
        t = lambda x: 1.0*x/abs(x)/abs(self.SCALING)
        o = spaceElement(ct)
        x1 = spaceElement(a-t(a)-ct[0], ct[1], ct[2])
        x2 = spaceElement(a-ct[0], ct[1], ct[2])

        y1 = spaceElement(ct[0], b-t(b)-ct[1], ct[2])
        y2 = spaceElement(ct[0], b-ct[1], ct[2])

        z1 = spaceElement(ct[0], ct[1], c-t(c)-ct[2])
        z2 = spaceElement(ct[0], ct[1], c-ct[2])

        spaceElement(o,x1).plot(color=(1,0,0), linesize=linesize)
        spaceElement(o,y1).plot(color=(0,1,0), linesize=linesize)
        spaceElement(o,z1).plot(color=(0,0,1), linesize=linesize)

        x2.plotText("X", width=textwidth)
        y2.plotText("Y", width=textwidth)
        z2.plotText("Z", width=textwidth)
        spaceElement(x1,x2).plotArrow(color=(1,0,0), arraymode=arraymode)
        spaceElement(y1,y2).plotArrow(color=(0,1,0), arraymode=arraymode)
        spaceElement(z1,z2).plotArrow(color=(0,0,1), arraymode=arraymode)
        return

def getcubepoints(L=[0,0,0], R=[1,1,1]):
    ans = np.zeros((8,3))

    for i in range(4):
        ans[i][-1] = L[-1]
        ans[i+4][-1] = R[-1]
    for i in [0,3]:
        ans[i][0] = L[0]
        ans[i+4][0] = L[0]
    for i in [1,2]:
        ans[i][0] = R[0]
        ans[i+4][0] = R[0]

    for i in [0,1]:
        ans[i][1] = L[1]
        ans[i+4][1] = L[1]
    for i in [2,3]:
        ans[i][1] = R[1]
        ans[i+4][1] = R[1]
    return ans

def puttex(text, dpi=120, fontsize=20, position='leftbottom'):
    from matplotlib import mathtext
    parser = mathtext.MathTextParser("bitmap")
    te, x = parser.to_mask(text, dpi=dpi, fontsize=fontsize)
    te = np.where(te>0,2,0)
    s,t = np.shape(te)
    def cf(x):
        xs,xt = np.shape(x)
        ans = x*0
        if position == 'leftbottom':
            ans[xs-s-10:xs-10, 5:t+5] += te*0.003
        elif position == 'lefttop':
            ans[10:10+s, 5:5+t] += te*0.003
        return ans
    return cf


if __name__ == "__main__":
    fig = mlab.figure(fgcolor=(0, 0, 1.0), bgcolor=(1.0, 1.0, 1.0), size=(700, 700))
    setSCALING(1)   # 缩放比例

    # 坐标轴， arraymode='arrow' 表示3d箭头， 默认原点是(0,0,0), 前面三个参数是各个坐标长度
    Axis(1.8, 1.8, 1.8).plot(arraymode="2darrow")

    linesize = 0.001  # 线大小

    #  spaceElement --- 该函数的作用是构造空间的点线面元素对象
    #  spaceElement 输入一个三维坐标可以得到点对象，输入两个点对象可以得到线对象，输入三个点对象得到面对象

    # 构造制点对象
    A = spaceElement([1,0,0])
    B = spaceElement([0,1,0])
    C = spaceElement([0,0,1])
    P = spaceElement([0,0,0])
    D = spaceElement([0.5,0.5,0])
    # getcubepoints是直接得到立方体（或长方体）的8个点，参数为体对角线上两个点的坐标
    ps = getcubepoints()
    a = [spaceElement(p) for p in ps]   # a是一个列表，里面有8个元素，每个元素都是一个点对象

    # 绘制点，以及点文本
    A.plot()
    B.plot()
    C.plot()
    D.plot()
    A.plotText("A")
    B.plotText("B")
    C.plotText("C")
    D.plotText("D")


    #  绘制立方体框架Frame，支持立方体Frame((A,B,C,D), (E,F,G,H))，柱体和椎体Frame(A, (B,C,D))，
    Frame(a[:4], a[4:]).plot(linesize=linesize)

    # spaceElement两点构成一条线
    spaceElement(C, D).plot(linestyle="dashed", linesize=linesize, color=(0,1,0))

    # spaceElement四点构成一平面
    spaceElement(a[0],a[2],a[6],a[4]).plot(colormap="Spectral", opacity=0.8)

    # spaceElement3点构成一平面
    ABC = spaceElement(A, B, C)
    ABC.plot(colormap="Accent", opacity=0.8)
    pABC = ABC.getPerpendicularLine(a[0])   # a[0]点到平面ABC的垂线
    pABC.plot(linestyle="dashed", linesize=linesize, color=(1,0,0))
    pABC.getPoint(1).plot(scale_factor=0.05)   # 由线得到点
    # spaceElement(A, C).getParallelLine(D).plot(linestyle="dashed", linesize=linesize, color=(0,1,0))
    pAC = spaceElement(A, C).getPerpendicularLine(D)  # a[0]点到直线AC的垂线
    pAC.plot(linestyle="dashed", linesize=linesize, color=(1,0,0))
    pAC.getPoint(1).plot(scale_factor=0.05)

    """
    总结：
    先构造所有点对象，绘制坐标轴
    然后根据这些点对象得到线，以及面，按照这样的思路就很容易绘制3d图形
    """
    mlab.show()