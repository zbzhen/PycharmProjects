#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: water1
@time: 2018/5/3  0:16
"""
import numpy as np
from numpy import array, arange, random
from tvtk.api import tvtk
from mayavi.scripts import mayavi2
def single_type_ug():
    """Simple example showing how to create an unstructured grid
    consisting of cells of a single type.
    """
    points = array([[0,0,0], [1,0,0], [0,1,0], [0,0,1], # tets
                    [1,0,0], [2,0,0], [1,1,0], [1,0,1],
                    [2,0,0], [3,0,0], [2,1,0], [2,0,1],
                    ], 'f')
    tets = array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
    tet_type = tvtk.Tetra().cell_type
    ug = tvtk.UnstructuredGrid(points=points)
    ug.set_cells(tet_type, tets)
    return ug
temperature = arange(0, 120, 10, 'd')
ug = single_type_ug()
ug.point_data.scalars = temperature
ug.point_data.scalars.name = 'temperature'

from mayavi.sources.vtk_data_source import VTKDataSource
from mayavi.modules.surface import Surface

@mayavi2.standalone
def view():
    mayavi.new_scene()
    # The single type one
    src = VTKDataSource(data = ug)
    mayavi.add_source(src)
    mayavi.add_module(Surface())
if __name__ == '__main__':
    view()