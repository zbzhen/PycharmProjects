#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/7 13:46
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 三维.py
# @version : Python 2.7.6
import pygame as pg
from pygame.locals import *
import ode

def coord(x,y):
    return 320 + 170*x, 400-170*y

def buildObjects():
    return world, body1, body2

def simulate(world, body1, body2):
    pg.init()
    srf = pg.display.set_mode((640, 480))
    clk = pg.time.Clock()
    fps=50
    dt=1.0/fps
    loopFlag = True
    while loopFlag:
        events = pg.event.get()
        for e in events:
            if e.type == QUIT:
                loopFlag = False
        srf.fill((255,255,255))  # 清屏
        x1,y1,z1 = body1.getPosition()
        x2,y2,z2 = body2.getPosition()
        pg.draw.line(srf, (55,0,200), coord(0,2), coord(x1,y1), 2)
        pg.draw.circle(srf, (55,0,200), coord(x1,y1), 20,0)
        pg.draw.line(srf, (55,0,200), coord(x1,y1), coord(x2,y2), 2)
        pg.display.flip()  # 显示画面
        world.step(dt)
        clk.tick(fps)
simulate(buildObjects())



