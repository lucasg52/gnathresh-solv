import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from expermt.Laura_27.testing_Rin import Resist_cell, resist_in
from neuron import h
h.load_file("stdrun.hoc")
from cells.adoptedeq import elength

def imped(part):
	zz = h.Impedance()
	zz.loc(part)
	zz.compute(0)
	return zz.input(part)

m = Resist_cell(0)
m.prop_site.connect(m.main_shaft(1))
m.parent.L = 118

length = 59
#getting resistances
resist_collect = np.ones((m.main_shaft.nseg,length))
def collect_Rin(length, collector, m, rec_place):
	j=-1
	for seg in m.main_shaft:
		j+=1
		m.parent.connect(seg)
		for i in range(1,length+1):
			m.side1.L = m.side2.L = i
			m._normalize()
		#print(f"{j},{i-1}: {m.parent.nseg}")
			collector[j][i-1]*=imped(rec_place)
	print("successfully gotten input resistances")


# resist_collect2 = np.ones((m.main_shaft.nseg,length))
# j2=-1
# for seg in m.main_shaft:
# 	j2+=1
# 	m.parent.connect(seg)
# 	for i in range(1,length+1):
# 		m.side1.L = m.side2.L = i
# 		m._normalize()
# 		#print(f"{j2},{i-1}: {m.side1.nseg}")
# 		resist_collect2[j2][i-1]*=imped(m.parent(0))


#plot making and showing
def plot():
	fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,4))
	ax = fig.add_subplot(projection='3d')
	x0 = [i for i in range(0, length, 1)]
	y0 = [i for i in range(0, m.main_shaft.nseg, 1)]
	X0,Y0 = np.meshgrid(x0,y0)
	Z0 = resist_collect
	ax.plot_surface(X0, Y0, Z0,alpha=0.5, cmap = cmap.viridis)
	ax.set_xlabel('length of side branches in um')
	ax.set_ylabel('node along main shaft')
	ax.set_zlabel('input resistance')
	plt.show()
#ax.set_zlim3d(-50,30)                    # viewrange for z-axis should be [-4,4]
# ax.set_ylim3d(0, 32)                    # viewrange for y-axis should be [-2,2]

#subplot 2
# fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(8,4))
# ax[1] = fig.add_subplot(projection='3d')
# x1 = [i for i in range(0, length, 1)]
# y1 = [i for i in range(0, m.main_shaft.nseg, 1)]
# X1,Y1 = np.meshgrid(x1,y1)
# Z1 = resist_collect2
# ax[1].plot_surface(X1, Y1, Z1,alpha=0.5, cmap = cmap.viridis)
# ax[1].set_xlabel('length of side branches in um')
# ax[1].set_ylabel('node along main shaft')
# ax[1].set_zlabel('input resistance')
# plt.show()