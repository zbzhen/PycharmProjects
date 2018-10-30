#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/7 11:47
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 自动化分段函数.py
# @version : Python 2.7.6
import matplotlib.pyplot as plt
import numpy as np
from sympy import latex, var, pi
h = 1.2
fontsize = 30
ticksize = 20


# 绘制幂函数
# fx1 = lambda x: 3**x
# fx2 = lambda x: 2**x
# fx3 = lambda x: 0.5**x
# x1 = np.linspace(-1.3, 1.2, 120)
# x2 = np.linspace(-1.3, 1.3, 120)
# x3 = np.linspace(-1.3, 1.8, 120)
# y1 = fx1(x1)
# y2 = fx2(x2)
# y3 = fx3(x3)


# 绘制幂函数
fx1 = lambda x: np.log(x)/np.log(2)
fx2 = lambda x: np.log(x)/np.log(3)
fx3 = lambda x: np.log(x)/np.log(0.5)
x1 = np.linspace(0.3, 2.5, 120)
x2 = np.linspace(0.3, 3.5, 120)
x3 = np.linspace(0.3, 2.5, 120)
y1 = fx1(x1)
y2 = fx2(x2)
y3 = fx3(x3)


# # 绘制指数与对数函数
# fx1 = lambda x: np.exp(x)
# fx2 = lambda x: x
# fx3 = lambda x: np.log(x)
# x1 = np.linspace(-2.2, 1, 120)
# x2 = np.linspace(-2.2, 3, 120)
# x3 = np.linspace(fx1(x1[0]), fx1(x1[-1]), 120)
# y1 = fx1(x1)
# y2 = fx2(x2)
# y3 = fx3(x3)

# # 绘制一次二次反比例相关分段函数
# fx1 = lambda x: x+1.5
# fx2 = lambda x: x*x
# fx3 = lambda x: 1.0/x
# x1 = np.linspace(-3, -1, 120)
# x2 = np.linspace(-1, 1, 120)
# x3 = np.linspace(1, 3, 120)
# y1 = fx1(x1)
# y2 = fx2(x2)
# y3 = fx3(x3)

# 绘制反比例函数
# fx1 = lambda x: 1.0/x
# fx2 = fx1
# fx3 = fx1
# x1 = np.linspace(-3, -0.3, 120)
# x2 = np.linspace(0.3, 3, 120)
# x3 = x2
# y1 = fx1(x1)
# y2 = fx2(x2)
# y3 = fx3(x3)


# 绘制对勾函数
# fx1 = lambda x: x + 1.0/x
# fx2 = fx1
# fx3 = fx1
# x1 = np.linspace(-5, -0.25, 120)
# x2 = np.linspace(0.25, 5, 120)
# x3 = x2
# y1 = fx1(x1)
# y2 = fx2(x2)
# y3 = fx3(x3)

# 绘制双曲线
# fx1 = lambda x: x + 1.0/x
# fx2 = fx1
# fx3 = fx1
# t1 = np.linspace(-0.3*np.pi, 0.3*np.pi, 120)
# t2 = np.linspace(0.7*np.pi, 1.3*np.pi, 120)
# x1 = 1.0/np.cos(t1)
# x2 = 1.0/np.cos(t2)
# x3 = x2
# y1 = np.tan(t1)
# y2 = np.tan(t2)
# y3 = y2


#这个定义域和值域可以自己设置
DL = min([x1.min(), x2.min(), x3.min()])
DR = max([x1.max(), x2.max(), x3.max()])
ZL = min([y1.min(), y2.min(), y3.min()])
ZR = max([y1.max(), y2.max(), y3.max()])

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

plt.plot([0,0],[0,0.02], lw=0.1)
plt.plot([0,0.02],[0,0], lw=0.1)

plt.text(xR, 0, r'$x$', color="black", fontsize=fontsize, va='top', ha='left')
plt.text(0+0.03*lim, yR,r'$y$', color="black", fontsize=fontsize, va='center', ha='left')
# plt.text(0+0.02*lim, 0,r'$o$', color="black", fontsize=fontsize, va='top', ha='left')
# 下面一行是o在十字架中心的左下方
plt.text(0-0.02*lim, 0,r'$o$', color="black", fontsize=fontsize, va='top', ha='right')



# 绘制函数
plt.plot(x1, y1, lw=3, color="r")
plt.plot(x2, y2, lw=3, color="blue")
plt.plot(x3, y3, lw=3, color="g")
plt.plot([0,3.5],[1, 1], '--', color="black")
plt.plot(2,1,'ro')
plt.plot(3,1,'bo')
plt.plot(0.5,1,'go')
plt.plot([2,2],[0,1],'--',color="r")
plt.plot([3,3],[0,1],'--',color="b")
plt.plot([0.5,0.5],[0,1],'--',color="g")
plt.text(1,1.5,'$y = \\log _2x$',fontsize=20,color="r")
plt.text(3,1.2,'$y = \\log _3x$',fontsize=20,color="b")
plt.text(2.5,-1.5,'$y = \\log \\frac{1}{2} x$',fontsize=20,color="g")

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
print(u"您确定了没错，该代码主要针对间断函数或分段函数的绘制")
print(u"请打开zdhfenduan.png文件")
# plt.show()