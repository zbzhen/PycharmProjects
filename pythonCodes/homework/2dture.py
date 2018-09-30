# -*- coding: utf-8 -*-
import numpy as np
from enthought.mayavi import mlab
n = 20
x, y = np.mgrid[0:1:n+0j, 0:1:n+0j]
#z = 10*x*np.exp( - x**2 - y**2)
z = 10*x*y*(x-1)*(y-1)
#transparent=True
pl=mlab.mesh(x,y,z)
#mlab.axes(xlabel='x', ylabel='y', zlabel='z')
#mlab.title( "Graph of z=10xy(x-1)(y-1)")
#mlab.outline(pl)
mlab.show()
