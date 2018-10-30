#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 17:53
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 全自动绘制函数.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex, var, pi
from draggable import setDrags, setPressed

fig, ax = plt.subplots(1, figsize=(8,8), facecolor='white')
fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)#取消默认快捷键的注册
ax.axis('off')
h = 1.2
fontsize = 30
ticksize = 20


# 绘制幂函数
ff = [lambda x: x,
      lambda x: x*x,
      lambda x: x*x*x,
      lambda x: np.sqrt(x),
      lambda x: 1.0/x,
      lambda x: 1.0/x]
xx = [np.linspace(-3, 3, 120),
      np.linspace(-2, 2, 120),
      np.linspace(-1.6, 1.6, 120),
      np.linspace(0, 3, 120),
      np.linspace(0.3, 3, 120),
      np.linspace(-3, -0.3, 120)]
oposition = 'r'  # 原点在右边
plotticks = True
colors = 'rgbcmmyk'
linewides=[2]*6
ftz = 30
def plotlineandtext(plt):
    # 绘制函数
    plots = []
    for i in range(len(xx)):
        p, = plt.plot(xx[i], yy[i], lw=linewides[i], color=colors[i])
        plots += [p]
    setPressed(plots, fig)
    # 绘制公式
    a1 = plt.text(1,-1,'$y=x$', fontsize=ftz, color=colors[0])
    a2 = plt.text(1,-1.5,'$y=x^2$', fontsize=ftz, color=colors[1])
    a3 = plt.text(1,-2,'$y=x^3$', fontsize=ftz, color=colors[2])
    a4 = plt.text(1,-2.5,'$y=\\sqrt{x}$', fontsize=ftz, color=colors[3])
    a5 = plt.text(1,-3,'$y=\\frac{1}{x}$', fontsize=ftz, color=colors[4])
    plots = [a1,a2,a3,a4,a5]
    setPressed(plots, fig)
    return setDrags(plots)



# 绘制对数函数
# ff = [lambda x: np.log(x)/np.log(2),
#       lambda x: np.log(x)/np.log(0.5),
#       lambda x: np.log(x)/np.log(3)]
# xx = [np.linspace(0.3, 2.5, 120),
#       np.linspace(0.3, 2.5, 120),
#       np.linspace(0.3, 3.2, 120)]
# oposition = 'r'  # 原点在右边
# plotticks = True  # 绘制刻度
# colors = 'rgbcmmyk'
# linewides=[2]*6
# ftz = 30
# def plotlineandtext(plt):
#     # 绘制函数
#     plots = []
#     for i in range(len(xx)):
#         p, = plt.plot(xx[i], yy[i], lw=linewides[i], color=colors[i])
#         plots += [p]
#     setPressed(plots, fig)
#     # 绘制公式以及线条
#     plt.plot([0,3.5],[1, 1], '--', color="black")
#     plt.plot(2,1,'ro')
#     plt.plot(3,1,'bo')
#     plt.plot(0.5,1,'go')
#     plt.plot([2,2],[0,1],'--',color="r")
#     plt.plot([3,3],[0,1],'--',color="b")
#     plt.plot([0.5,0.5],[0,1],'--',color="g")
#     plt.text(1,1.5,'$y = \\log _2x$',fontsize=20,color="r")
#     plt.text(3,1.2,'$y = \\log _3x$',fontsize=20,color="b")
#     plt.text(2.5,-1.5,'$y = \\log \\frac{1}{2} x$',fontsize=20,color="g")

#---------------------------------------------------------------------------------------------
#  下面的函数可以不需要怎么动
#---------------------------------------------------------------------------------------------


#这个定义域和值域可以自己设置
yy = [ff[i](xx[i])for i in range(len(xx))]
DL = min([i.min() for i in xx])
DR = max([i.max() for i in xx])
ZL = min([i.min() for i in yy])
ZR = max([i.max() for i in yy])



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

plt.plot([0,0],[0,0.02], lw=0.1)
plt.plot([0,0.02],[0,0], lw=0.1)

plt.text(xR, 0, r'$x$', color="black", fontsize=fontsize, va='top', ha='left')

plt.text(0+0.03*lim, yR,r'$y$', color="black", fontsize=fontsize, va='center', ha='left')
if oposition == 'r':
    plt.text(0+0.02*lim, 0,r'$o$', color="black", fontsize=fontsize, va='top', ha='left')
else:
    plt.text(0-0.02*lim, 0,r'$o$', color="black", fontsize=fontsize, va='top', ha='right')




# 这个函数在前面定义过, 设置一个输出参数才能拖动图形
tmp = plotlineandtext(plt)



# 绘制刻度
xticks = []
yticks = []
xtdocs = []
ytdocs = []
if plotticks:
    xticks = np.array(range(int(DL), 0) + range(1, int(DR)+1))  # 这个是设置x刻度线
    xtdocs = xticks.copy()  # 这个是设置x刻度值
    yticks = np.array(range(int(ZL), 0) + range(1, int(ZR)+1))  # 这个是设置x刻度值
    ytdocs = yticks.copy()   # 这个是设置y刻度值
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
plt.savefig("zdhfenduan.png")
print(u"请打开zdhfenduan.png文件")
print(u"要注意不要用中文输入法，不然按键失效")
plt.show()