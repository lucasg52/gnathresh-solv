#Lucas Swanson & Laura Zittlow -- Ripon College '27

import matplotlib.pyplot as plt
import numpy as np
# from visual import readsummary as rs

from matplotlib import cm
#def makeplot(cmap = cm.viridis):

plt.style.use('_mpl-gallery')

def matrixplot(matx, start1, stop1, start2, stop2):
    rows,cols = matx.shape
    X = np.linspace(start1,stop1,rows)#np.arange(cols)
    Y = np.linspace(start2,stop2,cols)#np.arange(rows)

    X, Y = np.meshgrid(X, Y)
    Z = matx

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z, vmin=Z.min(),  cmap = cm.viridis)
    plt.show()

def matrixplot_smart(matx_x, matx_z, unitsize = 4): #axisvars):
    rows,cols = matx_z.shape
    X = matx_x*unitsize
    Y = matx_x*unitsize

    X, Y = np.meshgrid(X, Y)
    Z = matx_z

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z, vmin=Z.min(),  cmap = cm.viridis)
    plt.show()
