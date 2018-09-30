import matplotlib.pyplot as plt

plt.axvspan(76, 76, facecolor='g', alpha=1)
# plt.annotate('This is awesome!',
#              xy=(76, 0.75),
#              xycoords='data',
#              textcoords='offset points',
#              arrowprops=dict(arrowstyle="->", shrink=0.05))

plt.annotate('local max', xy=(76, 0.75), xytext=(77, 0.75),
            arrowprops=dict(facecolor='black', shrink=0.3),wideth=0.4
            )
plt.show()