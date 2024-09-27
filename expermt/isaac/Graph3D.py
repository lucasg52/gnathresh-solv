import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LinearLocator
from gnatsolv.expermt.isaac.all_arr import B12array, X_arr, Y_arr, two_lengna_arr, len_lst,DnL_one
from gnatsolv.expermt.isaac.all_arr import pred_2d_arr,pred_2l_arr
from gnatsolv.expermt.isaac.B1_B3_arr import B1B3, pred_B1B3_arr
from matplotlib import cm
ax = plt.figure().add_subplot(projection='3d')



# Make data.
#X = [X_arr]
X = np.linspace(0, 4, 40)
xlen = len(X)
#Y = [Y_arr]
Y = np.linspace(0,4,40)
ylen = len(Y)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
arr = np.array(two_lengna_arr)
# arr = np.delete(arr, 0,1)
# arr = np.delete(arr,1,0)
Z = arr - pred_2l_arr

# Create an empty array of strings with the same shape as the meshgrid, and
# populate it with two colors in a checkerboard pattern.
# colortuple = ('y', 'b')
# colors = np.empty(X.shape, dtype=str)
# for y in range(ylen):
#     for x in range(xlen):
#         colors[y, x] = colortuple[(x + y) % len(colortuple)]

# Plot the surface with face colors taken from the array we made.
surf = ax.plot_surface(X, Y, Z, cmap = cm.cool, linewidth=0)

# Customize the z axis.
ax.set_zlim(np.min(Z), np.max(Z))
ax.zaxis.set_major_locator(LinearLocator(6))
plt.ylabel("Length B1",fontsize=15)
plt.xlabel("Length B2",fontsize=15)
ax.set_title("Difference",fontsize=15)

plt.show()
