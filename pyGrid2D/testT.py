#!/usr/bin/env python
# encoding: utf-8
from pyGrid2D.Grid2D import Grid2D, plotblank
import matplotlib.pyplot as plt
import numpy as np
from Function.functionQuad import Quadrature

# Directoryname = ".//testmesh//"
# # Directoryname = "..//testmesh//RTdumbbell//"
# # datafile = "newRT_dumbbell_mesh1.dat"
# datafile = "4times4_rect.dat"

# datafile = "mesh2x2.dat"
# Directoryname = "..//testmesh//triangle11//"

datafile = "AddDensity_2_4times4_rectTrembled.dat"
datafile = "4times4_rectTrembled.dat"
Directoryname = "..//testmesh//rectTrembled//"


# datafile = "sixbianxing.dat"
# outputdatafile = "new"+datafile
grid = Grid2D()
grid.from_meshdat_get_pte(Directoryname+datafile)
p, t, e = grid.points, grid.elements, grid.bounds
grid.readGrid()


fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
axes = plt.subplot(111)

#
quad = Quadrature(1)
quad.getLobattoPiontsWeights()
grid.plotmesh2d(axes)
# grid.plotNodeDistribution(axes, quad.points, plotnodenum=False, pointsize=6, ftz=12, linewidth=5)
# print grid.poly
# print grid.elements
plotblank(axes)
plt.show()
plt.close(0)

plt.show()