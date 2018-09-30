#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 [MSC v.1500 32 bit (Intel)] on win32
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file: wangge1
@time: 2016-04-21 13:23
"""
from matplotlib.collections import LineCollection
for i in range(9):
    alpha = (i+1)*.1
    concave_hull, edge_points = alpha_shape(new_points,
                                            alpha=alpha)
    #print concave_hull
    lines = LineCollection(edge_points)
    pl.figure(figsize=(10,10))
    pl.title('Alpha={0} Delaunay triangulation'.format(
        alpha))
    pl.gca().add_collection(lines)
    delaunay_points = np.array([point.coords[0]for point in new_points])
    pl.plot(delaunay_points[:,0], delaunay_points[:,1],
            'o', hold=1, color='#f16824')

    _ = plot_polygon(concave_hull)
    _ = pl.plot(x,y,'o', color='#f16824')