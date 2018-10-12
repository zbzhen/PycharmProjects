#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/6 16:37
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 自动化坐标.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex, var, pi
h = 1.2
fontsize = 30
ticksize = 20
# 这个例子是实际坐标





# # 函数和定义域
# # 下面的3行代码是一次函数
# fx = lambda x: x
# x = np.linspace(-2, 2, 120)
# y = fx(x)

# # 下面的3行代码是二次函数
# fx = lambda x: x*x
# x = np.linspace(-2, 2, 120)
# y = fx(x)

# 下面的3行代码是绝对值函数
fx = lambda x: abs(x)
x = np.linspace(-2, 2, 120)
y = fx(x)

# # 下面的3行代码是对数函数
# fx = lambda x: np.log(x)
# x = np.linspace(0.3, 3, 120)
# y = fx(x)

# # 下面的3行代码是指数
# fx = lambda x: np.exp(x)
# x = np.linspace(-2, 1, 120)
# y = fx(x)

# 下面三行代码是绘制椭圆的例子
# theta = np.linspace(-np.pi, np.pi, 120)
# x = 4*np.cos(theta)
# y = 3*np.sin(theta)


# 下面三行代码是绘制抛物线的例子
# t = np.linspace(-1, 1, 120)
# x = 4*t*t
# y = 4*t

#这个定义域和值域可以自己设置
DL = x.min()
DR = x.max()
ZL = y.min()
ZR = y.max()

fig_mpl, ax = plt.subplots(1, figsize=(8,8), facecolor='white')
ax.axis('off')

# 坐标轴范围
xL, xR = DL*h, DR*h
yL, yR = ZL*h, ZR*h
lim = abs(np.array([xL, xR, yL, yR])).max()

# 坐标轴范围自动补充长度
xyLR = [xL, xR, yL, yR]
for i in range(4):
    if abs(xyLR[i]) < 0.2*lim or (-1)**(i+1)*xyLR[i] < 0:
        xyLR[i] = 0.2*lim
    xyLR[i] = abs(xyLR[i])*(-1)**(i+1)
xL, xR, yL, yR = xyLR



# 设置图形范围
ax.set_xlim(-1.0*h*lim, h*lim)
ax.set_ylim(-1.0*h*lim, h*lim)

# 绘制xoy直角坐标系
ax.arrow(xL, 0, xR-xL, 0, head_width=lim*0.06, head_length=lim*0.1, fc='k', ec='k', overhang=0.8, lw=2)
ax.arrow(0, yL, 0, yR-yL, head_width=lim*0.06, head_length=lim*0.1, fc='k', ec='k', overhang=0.8, lw=2)
plt.text(xR, 0, r'$x$', color="black", fontsize=fontsize, va='top', ha='left')
plt.text(0+0.03*lim, yR,r'$y$', color="black", fontsize=fontsize, va='center', ha='left')
plt.text(0+0.02*lim, 0,r'$o$', color="black", fontsize=fontsize, va='top', ha='left')
# 下面一行是o在十字架中心的左下方
# plt.text(0-0.02*lim, 0,r'$o$', color="black", fontsize=fontsize, va='top', ha='right')







# 绘制函数
plt.plot(x, y, lw=3, color="b")


# 绘制函数上的点
# x0 = 1.5
# y0 = fx1(x0)
# plt.plot([x0, x0], [0, y0], "--", lw = 1, color='k')   # 绘制虚线
# plt.plot([0, x0], [y0, y0], "--", lw = 1, color='k')   # 绘制虚线
# plt.plot(x0, y0, "ro", ms=10)   # 绘制函数上的点
# tex = "$("+str(x0) + ",\," + str(y0) + ")$"
# plt.text(x0, y0, tex, color="black", fontsize=25, ha='left', va='top')   # 绘制坐标,点在文本左上方


# 绘制刻度
xticks = []
yticks = []
xtdocs = []
ytdocs = []
# xticks = np.array(range(int(DL), 0) + range(1, int(DR)+1))  # 这个是设置x刻度线
# xtdocs = xticks.copy()  # 这个是设置x刻度值
# yticks = np.array(range(int(ZL), 0) + range(1, int(ZR)+1))  # 这个是设置x刻度值
# ytdocs = yticks.copy()   # 这个是设置y刻度值
ht = 0.03*lim
# 下面的两个for循环不要动
for i in range(len(xticks)):
    plt.plot([xticks[i],xticks[i]], [0,ht],"k")
    tex = '$'+latex(xtdocs[i])+'$'
    plt.text(xticks[i], 0-ht, tex, color="black", fontsize=ticksize, ha="center", va='top')
for i in range(len(yticks)):
    plt.plot([0,ht], [yticks[i],yticks[i]],"k")
    tex = '$'+latex(ytdocs[i])+'$'
    plt.text(0-ht, yticks[i], tex, color="black", fontsize=ticksize, va='center', ha='right')
plt.savefig("sample.png")

# plt.show()