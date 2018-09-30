'''
Demonstration of quiver and quiverkey functions. This is using the
new version coming from the code in quiver.py.

Known problem: the plot autoscaling does not take into account
the arrows, so those on the boundaries are often out of the picture.
This is *not* an easy problem to solve in a perfectly general way.
The workaround is to manually expand the axes.
https://matplotlib.org/1.4.1/examples/pylab_examples/quiver_demo.html
'''
from pylab import quiver,figure,quiverkey,plot,show,axis
import numpy as np
import matplotlib.pyplot as plt
f = np.loadtxt("xyuv.dat")
x, y, u, v = f.T
u = (y*3)*np.sin(2*x+2*y)
v = (x*3)*np.cos(2*x+2*y)
fig = plt.figure(figsize=(10,10), dpi=72,facecolor="white")
axes = plt.subplot(111)


Q = quiver( x, y, u, v,
            pivot='mid', color='r', units='inches' )
qk = quiverkey(Q, 0.5, 0.03, 1, r'$u=1$', fontproperties={'weight': 'bold'})
# qk = quiverkey(Q)

axes.plot( x, y, 'k.')
plt.axis([-0.2, 1.2, -0.2, 1.2])


plt.show()