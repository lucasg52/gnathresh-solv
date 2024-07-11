import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from neuron import h
from expermt.Laura_27.testing_Rin import Resist_cell_2d, Resist_cell_1b
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from tools.aprecorder import APRecorder
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

def my_imped(part):
	stim = h.IClamp(part)
	stim.amp = 200
	stim.dur = 51
	stim.delay = 5
	h.finitialize(-70)
	h.continuerun(55)
	return part.v/stim.amp
	#treturn f"input resistance at {part} = {part.v/stim.amp} mV/nA"

def lam_resist_col(stop, r_collector, cell, rec_place): #, g_collector, imp_solver):
	j=-1
	for sec in cell.all:
		if sec is not cell.soma:
			sec.gbar_nafTraub = 0
			sec.gbar_kdrTraub = 0
	for seg in cell.main_shaft:
		j+=1
		cell.parent.connect(seg)
		for i in range(1,stop*10+1,1):
			set_ELen(cell.side1, i/10, 0.1)
			set_ELen(cell.side2,i/10,0.1)
			cell._normalize()
			# if imp_solver == imped:
			# 	r_collector[j][i - 1] *= imped(rec_place)
			#if imp_solver == my_imped:
			r_collector[j][i-1]*= my_imped(rec_place)
			#g_collector[j][i-1] *= fullsearch(10)
	print(f"successfully calculated input resistances at {rec_place}")

def lam_gna_col(stop, g_collector, cell): #imp_solver): #g_collector,
	j=-1
	for seg in cell.main_shaft:
		j+=1
		cell.parent.connect(seg)
		for i in range(1,stop*10+1,1):
			set_ELen(cell.side1, i/10, 0.1)
			set_ELen(cell.side2,i/10,0.1)
			cell._normalize()
			g_collector[j][i-1] *= fullsearch(10)
	print(f"successfully retrieved gna thresh")

def diam_resist_col(min, max, d_dim, r_collector, cell, rec_place):
	j=-1
	for seg in cell.main_shaft:
		j+=1
		cell.parent.connect(seg)
		for i in range(min,max,d_dim):
			cell.side1.diam = cell.side2.diam = i/10
			cell._normalize()
			r_collector[j][i-1]*=my_imped(rec_place)
			#g_collector[j][i-1] *= fullsearch(10)
			print(f"{j},{i - 1}: {cell.side1.diam}")
	print(f"successfully found input resistances at {rec_place}")

def diam_gna_col(min, max, d_dim, g_collector, cell):
	j=-1
	for seg in cell.main_shaft:
		j+=1
		cell.parent.connect(seg)
		for i in range(min,max,d_dim):
			cell.side1.diam = cell.side2.diam = i/10
			cell._normalize()
			g_collector[j][i-1] *= fullsearch(10)
			print(f"{j},{i-1}: {cell.side1.diam}")
	print(f"successfully found gna")



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

def test(g_na):
	m.setgna(g_na)
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
resist_collect = np.ones((m.main_shaft.nseg, 30))
gna_collect = np.ones((m.main_shaft.nseg, 30))
# resist_list = []
# search_list = []