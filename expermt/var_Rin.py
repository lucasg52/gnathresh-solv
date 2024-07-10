import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from neuron import h
from expermt.Laura_27.testing_Rin import Resist_cell_2d, Resist_cell_1b
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from cells.tools import APRecorder
from solver.searchclasses import BinSearch
h.load_file("stdrun.hoc")

#functions
def set_ELen(section, length, dx):
	Lambda = elength(section)
	section.L = length*Lambda
	gnat.normalize_dlambda(section, dx)
	return

def imped(part):
	imp_geter = h.Impedance()
	imp_geter.loc(part)
	imp_geter.compute(0)
	return imp_geter.input(part)

def lam_col(start, stop, r_collector, g_collector, cell, rec_place):
	j=-1
	for seg in cell.main_shaft:
		j+=1
		cell.parent.connect(seg)
		for i in range(start*10,stop*10+1,1):
			set_ELen(cell.side1, i/10, 0.1)
			set_ELen(cell.side2,i/10,0.1)
			cell._normalize()
			r_collector[j][i-(start*10+1)]*=imped(rec_place)
			g_collector[j][i-(start*10+1)] *= fullsearch(10)
	print(f"successfully gotten input resistances at {rec_place} and g_na thresh")

def diam_col(min, max, d_dim, r_collector, g_collector, cell, rec_place):
	j=-1
	for seg in cell.main_shaft:
		j+=1
		cell.parent.connect(seg)
		for i in range(min*10,max*10,d_dim*10):
			cell.side1.diam = cell.side2.diam = i/10
			cell._normalize()
			r_collector[j][i-1]*=imped(rec_place)
			g_collector[j][i-1] *= fullsearch(10)
			print(f"{j},{i - 1}: {cell.side1.diam}")
	print(f"successfully found input resistances at {rec_place} and g_na thresh")

def lamb_col_partial(min, max, r_list, g_list, cell, rec_loc):
	for i in range(min*10, max*10+1, 1):
		set_ELen(cell.side1, i / 10, 0.1)
		set_ELen(cell.side2, i / 10, 0.1)
		cell._normalize()
		r_list.append(imped(rec_loc))
		g_list.append(fullsearch(10))
		print(cell.side1.L)
	print(f"collected isolated resistances at {rec_loc} and gna_thresh")

def plot(size_x, size_y,matx, xlabel, ylabel, zlabel, title):
	fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,4))
	ax = fig.add_subplot(projection='3d')
	x0 = [i for i in range(0, size_x, 1)]
	y0 = [i for i in range(0, size_y, 1)]
	X0,Y0 = np.meshgrid(x0,y0)
	Z0 = matx
	ax.plot_surface(X0/10, Y0, Z0,alpha=0.5, cmap = cmap.viridis)
	ax.set_xlabel(xlabel)#'length of side branches in lambda'
	ax.set_ylabel(ylabel)#'node along main shaft')
	ax.set_zlabel(zlabel)#'input resistance')
	ax.set_title(title)
	plt.show()

def test(g_na, cell):
	cell.setgna(g_na)
	h.finitialize(-70)
	h.continuerun(15)
	return rec.proptest()

def fullsearch(nsteps):
	search = BinSearch(0,1,test)
	for i in range(nsteps):
		search.searchstep()
		# print(search.a)
	return search.a

m = Resist_cell_2d(0)
m.prop_site.connect(m.main_shaft(1))
m.parent.L = 118
m.side1.L = 118
stim = h.IClamp(m.side1(0.9))
stim.amp = 200 #nA
stim.dur = 5 #ms
stim.delay = 0.3125 #ms
rec = APRecorder(m.prop_site)

# length = 3
# resist_collect = np.ones((m.main_shaft.nseg, 10))
# gna_collect = np.ones((m.main_shaft.nseg, 10))
# resist_list = []
# search_list = []