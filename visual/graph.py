#Lucas Swanson -- Ripon College '27

import matplotlib.pyplot as plt
import numpy as np
# from visual import readsummary as rs

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


def matrixplot(matx, start1, stop1, start2, stop2):
    rows,cols = matx.shape
    X = np.linspace(start1,stop1,rows)#np.arange(cols)
    Y = np.linspace(start2,stop2,cols)#np.arange(rows)

    X, Y = np.meshgrid(X, Y)
    Z = matx

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z, vmin=Z.min(),  cmap = cm.viridis)
    plt.show()

def matrixplot_smart(matx_x, matx_z): #axisvars):
    rows,cols = matx_z.shape
    X = matx_x*4 #axisvars[1]
    Y = matx_x*4#axisvars[0]

    X, Y = np.meshgrid(X, Y)
    Z = matx_z

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z, vmin=Z.min(),  cmap = cm.viridis)
    plt.show()
