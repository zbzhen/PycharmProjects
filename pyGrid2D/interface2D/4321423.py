import matplotlib.pyplot as plt
from pyGrid2D.Grid2D_2 import Grid2D, plotblank
import numpy as np

def Plot_LSH_Curve(b, r, Sim_T):
    s = np.arange(0, 1, 0.01)  
    p = 1 - np.power(1 - np.power(s, r), b)  
  
    fig = plt.figure()  
    ax = plt.gca()  
    ax = fig.add_subplot(111)
    ax.plot(s, p, color='red', linewidth=2)  
    plt.vlines(Sim_T, [0], 1, color="green", linewidth=3, linestyles="dashed")  
    ax.fill_betweenx(p, Sim_T, s, facecolor="orange", color="white")  
    ax.fill_betweenx(p, Sim_T, s, where=s >= Sim_T, facecolor='blue', color="white")  
    ax.set_title('S-curve of LSH')  
    ax.annotate('T', xy=(1.03*Sim_T, 0.45))  
    plt.grid()  
    plt.savefig('LSH_Scurve.png')  
    plt.show()
