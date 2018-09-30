import numpy as np
import re
from numpy import array, arange, random
from tvtk.api import tvtk
from mayavi.scripts import mayavi2
from mayavi.sources.vtk_data_source import VTKDataSource
from mayavi.modules.surface import Surface

def from_plotdat_get_pte(datafile):
    ugs = []
    with open(datafile) as f:
        lines = f.readlines()
        index = 2
        while index < len(lines):
            tmp = re.findall(r"\d+\d*", str(lines[index: index+1]))
            npoints, nelements = map(int, tmp)
            index += 1
            points = np.loadtxt(lines[index:index+npoints], float)
            index += npoints
            elements = np.loadtxt(lines[index:index+nelements], int)
            index += nelements

            ug = tvtk.UnstructuredGrid(points=points[:,:3])
            ug.set_cells(12, elements-1)
            ug.point_data.scalars = points.T[-1]
            ugs += [ug]
    return ugs

@mayavi2.standalone
def view(ugs):
    mayavi.new_scene()
    for ug in ugs:
        mayavi.add_source(VTKDataSource(data=ug))
        mayavi.add_module(Surface())

if __name__ == '__main__':
    ugs = from_plotdat_get_pte("uplot6.dat")
    view(ugs)
