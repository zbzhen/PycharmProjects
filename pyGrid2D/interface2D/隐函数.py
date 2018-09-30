import matplotlib.pyplot as plt 
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np 

fig = plt.figure(1) 
ax = fig.add_subplot(111) 

# set up axis 
ax.spines['left'].set_position('zero') 
ax.spines['right'].set_color('none') 
ax.spines['bottom'].set_position('zero') 
ax.spines['top'].set_color('none') 
ax.xaxis.set_ticks_position('bottom') 
ax.yaxis.set_ticks_position('left') 

# setup x and y ranges and precision
x = np.arange(-0.5,5.5,0.01) 
y = np.arange(-0.5,5.5,0.01)

# draw a curve 
# line, = ax.plot(x, x**2,zorder=100)

# draw a contour
X,Y=np.meshgrid(x,y)
F=X**Y
G=Y**X
ax.contour(X,Y,(F-G),[0],zorder=100)

#set bounds 
ax.set_xbound(-1,7)
ax.set_ybound(-1,7) 

#produce gridlines of different colors/widths
# ax.xaxis.set_minor_locator(MultipleLocator(0.2))
# ax.yaxis.set_minor_locator(MultipleLocator(0.2))
# ax.xaxis.grid(True,'minor',linestyle='-')
# ax.yaxis.grid(True,'minor',linestyle='-')

# minor_grid_lines = [tick.gridline for tick in ax.xaxis.get_minor_ticks()]
# for idx,loc in enumerate(ax.xaxis.get_minorticklocs()):
#     if loc % 2.0 == 0:
#         minor_grid_lines[idx].set_color('0.3')
#         minor_grid_lines[idx].set_linewidth(2)
#     elif loc % 1.0 == 0:
#         minor_grid_lines[idx].set_c('0.5')
#         minor_grid_lines[idx].set_linewidth(1)
#     else:
#         minor_grid_lines[idx].set_c('0.7')
#         minor_grid_lines[idx].set_linewidth(1)
#
# minor_grid_lines = [tick.gridline for tick in ax.yaxis.get_minor_ticks()]
# for idx,loc in enumerate(ax.yaxis.get_minorticklocs()):
#     if loc % 2.0 == 0:
#         minor_grid_lines[idx].set_color('0.3')
#         minor_grid_lines[idx].set_linewidth(2)
#     elif loc % 1.0 == 0:
#         minor_grid_lines[idx].set_c('0.5')
#         minor_grid_lines[idx].set_linewidth(1)
#     else:
#         minor_grid_lines[idx].set_c('0.7')
#         minor_grid_lines[idx].set_linewidth(1)

plt.show()