#!/usr/bin/env python
# encoding: utf-8
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter
import matplotlib.pyplot as plt
x = [10, 15, 20, 25]
fig = plt.figure(figsize=(9,6), dpi=72, facecolor="white")
hperro = [2.87e-4, 4.64e-7, 2.22e-10, 2.79e-13]
RTerro = [2.94e-05, 1.60e-08, 2.19e-12, 8.02e-14]
Rerro = [4.45e-05, 2.45e-08, 4.16e-12, 9.37e-15]
nohperro = [9.57e-06, 3.44e-09, 2.11e-13, 7.57e-14 ]

ax=plt.gca()
#ax.set_xticks = [5,10, 15, 20, 25,30]
ax.set_yscale("log")
#ax.set_yticks = [1e-16, 1e-13, 1e-10, 1e-7, 1e-4]
#ax.set_xticklabels(("5", "10", "15", "20", "25", "30"))
#plt.set_ylim(1e-16, 1e-4)
#plt.plot(x, hperro, label="hp-mesh")
plt.plot(x,hperro, "--*--",label="hp-mesh" )
plt.plot(x,RTerro, "--o--",label="RT-mesh" )
plt.plot(x,Rerro, "--v--",label="R-mesh" )
plt.plot(x,nohperro, "--+--",label="nohp-mesh" )
#plt.text(5,-1,r'$A$',color="blue",fontsize=20,ha="center")
plt.xlabel("$N$")
plt.ylabel("$L^2$"+"error")
#plt.ylim(1e-16, 1e-4)
plt.legend()
plt.savefig("error.pdf",dip=120)
plt.show()
