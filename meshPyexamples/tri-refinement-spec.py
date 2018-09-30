# Provided by Liu Benyuan in https://github.com/inducer/meshpy/pull/11

from __future__ import division

import meshpy.triangle as triangle
import numpy as np

import matplotlib.pyplot as plt

def main():
    innernum = 20
    outnum = 30

    points = [(2 * np.cos(angle), 1 * np.sin(angle))
              for angle in np.linspace(0, 2*np.pi, innernum, endpoint=False)]
    angle = np.linspace(0, 2*np.pi, innernum, endpoint=False)
    plt.plot(2 * np.cos(angle), np.sin(angle))
    points.extend(
            (3 * np.cos(angle), 3 * np.sin(angle))
            for angle in np.linspace(0, 2*np.pi, outnum, endpoint=False))


    facets = np.array([range(innernum+outnum), range(1,1+innernum+outnum)]).T
    facets[innernum-1][1] = 0
    facets[-1][1] = innernum

    markers = np.ones(innernum+outnum, int)
    markers[:innernum] = 2
    info = triangle.MeshInfo()
    info.set_points(points)

    info.set_facets(facets, facet_markers=markers)
    #
    info.regions.resize(1)
    # points [x,y] in region, + region number, + regional area constraints
    info.regions[0] = ([0,0] + [1,0.1])

    mesh = triangle.build(info, volume_constraints=True, max_volume=0.1, min_angle=30)

    mesh_points = np.array(mesh.points)
    mesh_tris = np.array(mesh.elements)
    mesh_attr = np.array(mesh.point_markers)
    print(mesh_attr)


    plt.triplot(mesh_points[:, 0], mesh_points[:, 1], mesh_tris)
    plt.xlabel('x')
    plt.ylabel('y')
    #
    fig = plt.gcf()
    fig.set_size_inches(4.2, 4.2)
    plt.show()
    plt.savefig('sec5-meshpy-triangle-ex4.pdf')

if __name__ == "__main__":
    main()
