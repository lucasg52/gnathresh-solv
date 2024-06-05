import matplotlib.pyplot as plt
import numpy as np
import readsummary as rs

from matplotlib import cm
#def makeplot(cmap = cm.viridis):

plt.style.use('_mpl-gallery')
#
## Make data
#X = np.arange(-5, 5, 0.25)
#Y = np.arange(-5, 5, 0.25)
#X, Y = np.meshgrid(X, Y)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)
#
## Plot the surface
#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#ax.plot_surface(X, Y, Z, vmin=Z.min() * 2, cmap = cm.viridis)
#
#ax.set(xticklabels=[],
#       yticklabels=[],
#       zticklabels=[])
#
#plt.show()


def matrixplot(matx):
    rows,cols = matx.shape
    X = np.arange(cols)
    Y = np.arange(rows)

    X, Y = np.meshgrid(X, Y)
    Z = matx

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z, vmin=Z.min(),  cmap = cm.viridis)
    plt.show()

def matrixplot_smart(matx, axisvars):
    rows,cols = matx.shape
    X = axisvars[1]
    Y = axisvars[0]

    X, Y = np.meshgrid(X, Y)
    Z = matx

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z, vmin=Z.min(),  cmap = cm.viridis)
    plt.show()
