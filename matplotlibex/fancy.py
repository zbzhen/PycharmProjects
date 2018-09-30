#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: fancy
@time: 2018/6/26  19:48
"""
import matplotlib.patches as mpatch
import matplotlib.pyplot as plt

figheight = 8
fig = plt.figure(1, figsize=(9, figheight), dpi=80, facecolor="white")
fontsize = 0.4 * fig.dpi

def make_boxstyles(ax):
    styles = mpatch.BoxStyle.get_styles()
    # print styles
    # stylename = "square"
    # ax.text(0.8, 0.5, stylename+"$\sum_{k=0}^n$" ,ha="center",
    #               size=fontsize,
    #               transform=ax.transAxes,
    #               bbox=dict(boxstyle=stylename, fc="w", ec="k"))
    #
    # stylename = "round4"
    # ax.text(0.8, 1, stylename ,ha="center",
    #               size=fontsize,
    #               transform=ax.transAxes,
    #               bbox=dict(boxstyle=stylename, fc="w", ec="k"))
    #
    # stylename = "circle"
    # ax.text(0.8, 0.8, stylename ,ha="center",
    #               size=fontsize,
    #               transform=ax.transAxes,
    #               bbox=dict(boxstyle=stylename, fc="w", ec="k"))

    for i, (stylename, styleclass) in enumerate(sorted(styles.items())):
        ax.text(0.5, (float(len(styles)) - 0.5 - i)/len(styles), stylename,
                  ha="center",
                  size=fontsize,
                  transform=ax.transAxes,
                  bbox=dict(boxstyle=stylename, fc="w", ec="k"))

def make_arrowstyles(ax):
    styles = mpatch.ArrowStyle.get_styles()

    ax.set_xlim(0, 4)
    ax.set_ylim(0, figheight)

    for i, (stylename, styleclass) in enumerate(sorted(styles.items())):
        y = (float(len(styles)) -0.25 - i) # /figheight
        p = mpatch.Circle((3.2, y), 0.2, fc="w")
        ax.add_patch(p)

        ax.annotate(stylename, (3.2, y),
                    (2., y),
                    #xycoords="figure fraction", textcoords="figure fraction",
                    ha="right", va="center",
                    size=fontsize,
                    arrowprops=dict(arrowstyle=stylename,
                                    patchB=p,
                                    shrinkA=5,
                                    shrinkB=5,
                                    fc="w", ec="k",
                                    connectionstyle="arc3,rad=-0.05",
                                    ),
                    bbox=dict(boxstyle="square", fc="w"))

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)


ax1 = fig.add_subplot(121, frameon=False, xticks=[], yticks=[])
make_boxstyles(ax1)

# ax2 = fig.add_subplot(122, frameon=False, xticks=[], yticks=[])
# make_arrowstyles(ax2)
plt.savefig("fanc.pdf")

plt.show()