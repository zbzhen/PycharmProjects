#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 21:41
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : draggable.py
# @version : Python 2.7.6
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, FancyArrow

class Draggable:
    def __init__(self, rect):
        self.rect = rect
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes:
            return
        contains, attrd = self.rect.contains(event)
        if not contains:
            return
        if isinstance(self.rect, plt.Polygon):
            self.press = self.rect.get_xy(), event.xdata, event.ydata
        elif isinstance(self.rect, (plt.Circle,Ellipse)):
            self.press = self.rect.center, event.xdata, event.ydata
        elif isinstance(self.rect, plt.Text):
            self.press = self.rect.get_position(), event.xdata, event.ydata
        elif isinstance(self.rect, plt.Rectangle):
            self.press = self.rect.xy, event.xdata, event.ydata
        elif isinstance(self.rect, plt.Line2D):
            self.press = self.rect.get_xydata(), event.xdata, event.ydata


    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return
        if event.inaxes != self.rect.axes:
            return
        xydata, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        x, y = np.array(xydata).copy().T


        if isinstance(self.rect, FancyArrow):
            self.rect.set_xy(np.array([x+dx,y+dy]).T)
        elif isinstance(self.rect, plt.Polygon):
            linelen = np.sqrt((x[0]-x[1])**2+(y[0]-y[1])**2)
            t = 0
            for i in range(len(x)):
                if np.sqrt((x[i]-xpress)**2+(y[i]-ypress)**2)<0.2*linelen:
                    x[i] += dx
                    y[i] += dy
                    self.rect.set_xy(np.array([x,y]).T)
                    t = 1
            if t==0:
                self.rect.set_xy(np.array([x+dx,y+dy]).T)
        elif isinstance(self.rect, (plt.Circle,Ellipse)):
            self.rect.center = (xydata[0]+dx, xydata[1]+dy)
        elif isinstance(self.rect, plt.Rectangle):
            self.rect.set_x(xydata[0]+dx)
            self.rect.set_y(xydata[1]+dy)
        elif isinstance(self.rect, plt.Text):
            self.rect.set_x(xydata[0]+dx)
            self.rect.set_y(xydata[1]+dy)
        elif isinstance(self.rect, plt.Line2D):
            linelen = np.sqrt((x[0]-x[-1])**2+(y[0]-y[-1])**2)
            if np.sqrt((x[0]-xpress)**2+(y[0]-ypress)**2)<0.2*linelen:
                x[0] += dx
                y[0] += dy
                self.rect.set_xdata(x)
                self.rect.set_ydata(y)
            elif np.sqrt((x[-1]-xpress)**2+(y[-1]-ypress)**2)<0.2*linelen:
                x[-1] += dx
                y[-1] += dy
                self.rect.set_xdata(x)
                self.rect.set_ydata(y)
            else:
                self.rect.set_xdata(x+dx)
                self.rect.set_ydata(y+dy)
        self.rect.figure.canvas.draw()

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

def setDrags(plots):
    drs = []
    for p in plots:
        dr = Draggable(p)
        dr.connect()
        drs.append(dr)
    return drs

def Pressed(p,fig):
    def on_key_press(event):
        if event.inaxes != p.axes:
            return
        contains, attrd = p.contains(event)
        if not contains:
            return
        if event.key in 'rgbcmyk':
            p.set_color(event.key)
        if event.key in '0123456789':
            p.set_alpha(0.1*eval(event.key))
        if isinstance(p, plt.Line2D):
            if event.key in '=':
                p.set_linewidth(p.get_linewidth()*1.2)
                p.set_ms(p.get_ms()*1.2)
            if event.key in '-':
                p.set_linewidth(p.get_linewidth()*1.0/1.2)
                p.set_ms(p.get_ms()*1.0/1.2)
        elif isinstance(p, plt.Text):
            if event.key in '=':
                p.set_fontsize(p.get_fontsize()*1.2)
            if event.key in '-':
                p.set_fontsize(p.get_fontsize()*1.0/1.2)
        elif isinstance(p, plt.Circle):
            if event.key in '=':
                p.set_radius(p.get_radius()*1.2)
            if event.key in '-':
                p.set_radius(p.get_radius()*1.0/1.2)
        elif isinstance(p, Ellipse):
            if event.key in '=':
                p.width = p.width*1.2
                p.height = p.height*1.2
            if event.key in '-':
                p.width = p.width*1.0/1.2
                p.height = p.height*1.0/1.2

        elif isinstance(p, plt.Rectangle):
            if event.key in '=':
                p.set_width(p.get_width()*1.2)
                p.set_height(p.get_height()*1.2)
            if event.key in '-':
                p.set_width(p.get_width()*1.0/1.2)
                p.set_height(p.get_height()*1.0/1.2)

        elif isinstance(p, plt.Polygon):
            xy = np.array(p.get_xy())
            xyt = xy.T
            cx = xyt[0].sum()*1.0/len(xy)
            cy = xyt[1].sum()*1.0/len(xy)
            dx = xyt[0] - cx
            dy = xyt[1] - cy
            t = 1.0
            if event.key in '=':
                t = 1.2
            if event.key in '-':
                t = 1.0/1.2
            newxy = np.array([dx*t + cx, dy*t + cy]).T
            p.set_xy(newxy)
        fig.canvas.draw_idle()#重新绘制整个图表，
    return on_key_press
def setPressed(plots, fig):
    for p in plots:
        fig.canvas.mpl_connect('key_press_event', Pressed(p,fig))
    return


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = np.linspace(-1,1,50)
    A, = ax.plot(x,np.sin(x),'--')
    B, = ax.plot([0.5],[0.5],'bo')
    BB, = ax.plot([0.8],[0.8],'bo')
    AB, = ax.plot([0.5, 0.8],[0.5,0.8])
    tex = ax.text(0.5,0.5,'$(x,y)$',fontsize=30)
    tex1 = ax.text(0.2,0.2,'$e^{\\pi i}$',fontsize=30)
    rect = plt.Rectangle((0.2,0.75), width = 0.4, height = 0.15, color = 'r', alpha = 0.3)#左下起点，长，宽，颜色，α
    elli = Ellipse((0.0, 0.0), width = 0.2, height = 0.1, color = 'g')
    circ = plt.Circle((0.7,0.2), 0.15, color = 'b', alpha = 0.5)#圆心，半径，颜色，α
    pgon = plt.Polygon([[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]], color = 'g', alpha = 0.5 )#顶点坐标颜色α
    ar = plt.arrow(0,0,0.5,0.5)
    ax.add_patch(rect)
    ax.add_patch(circ)
    ax.add_patch(pgon)
    ax.add_patch(elli)
    #
    # drs = []
    plots = [A, B, rect, circ, pgon, tex, tex1, elli, AB,BB, ar]
    help(ar)
    drs = setDrags(plots)
    fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)#取消默认快捷键的注册
    setPressed(plots, fig)
    plt.show()


