#!/usr/bin/env python
# encoding: utf-8
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter
import matplotlib.pyplot as plt
#x = [10, 15, 20, 25,30,35,40,50]
x = [10, 15, 20, 25,30,35,40]
fig = plt.figure(figsize=(9,6), dpi=72, facecolor="white")
#hperro = [2.09e-07, 3.36e-08, 8.90e-09 , 3.12e-09, 1.31e-09, 6.31e-10, 3.32e-10, 1.13e-10 ]
hperro = [2.09e-07, 3.36e-08, 8.90e-09 , 3.12e-09, 1.31e-09, 6.31e-10, 3.32e-10]
RTerro = [9.32e-07, 1.34e-07, 3.36e-08, 1.13e-08,  4.69e-09,  2.24e-09, 1.78e-09]
Rerro = [9.32e-07, 1.34e-07, 3.36e-08, 1.13e-08,  4.69e-09,  2.24e-09, 1.78e-09]
#nohperro = [7.88e-07, 1.13e-07, 8.79e-10, 8.00e-09, 3.36e-09, 1.60e-09, 8.46e-10]
nohperro = [7.88e-07, 1.13e-07, 2.28e-08, 8.00e-09, 3.36e-09, 1.60e-09, 8.46e-10]

ax=plt.gca()
ax.set_xticks = [5,10, 15, 20, 25,30]
ax.set_yscale("log")
#ax.set_yticks = [1e-16, 1e-13, 1e-10, 1e-7, 1e-4]
#ax.set_xticklabels(("5", "10", "15", "20", "25", "30"))
#plt.set_ylim(1e-16, 1e-4)
#plt.plot(x, hperro, label="hp-mesh")
plt.plot(x,hperro, "--*--",label="hp-mesh" )
plt.plot(x,RTerro, "--o--",label="RT-mesh" )
plt.plot(x,Rerro, "--v--",label="R-mesh" )
plt.plot(x,nohperro, "--+--",label="nohp-mesh" )

plt.xlabel("$N$")
plt.ylabel("$L^2$"+"error")
#plt.ylim(1e-16, 1e-4)
plt.legend()
plt.savefig("errornew.pdf",dip=120)
plt.show()
