import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from neuron import h
from expermt.Laura_27.testing_Rin import Resist_cell_1b
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
	zz = h.Impedance()
	zz.loc(part)
	zz.compute(0)
	return zz.input(part)

def lambda_collect(length, start, r_collector, g_collector, m, rec_place):
	j=-1
	for seg in m.main_shaft:
		j+=1
		m.parent.connect(seg)
		for i in range(30,length*10+1,1):
			set_ELen(m.side1, i/10, 0.1)
			set_ELen(m.side2,i/10,0.1)
			m._normalize()
			#print(f"{j},{i-1}: {m.parent.nseg}")
			r_collector[j][i-start]*=imped(rec_place)
			g_collector[j][i-start] *= fullsearch(10)
	print(f"successfully gotten input resistances at {rec_place} and g_na thresh")

def diam_collect(r_collector, g_collector, m, rec_place):
	j=-1
	for seg in m.main_shaft:
		j+=1
		m.parent.connect(seg)
		for i in range(1,11,1):
			m.side1.diam = m.side2.diam = i/10
			m._normalize()
			r_collector[j][i-1]*=imped(rec_place)
			g_collector[j][i-1] *= fullsearch(10)
			print(f"{j},{i - 1}: {m.side1.diam}")
	print(f"successfully gotten input resistances at {rec_place} and g_na thresh")

def lamb_partial_collect(length,rec_place, collect_list, g_list):
	for i in range(1, length * 10 + 1, 1):
		set_ELen(m.side1, i / 10, 0.1)
		set_ELen(m.side2, i / 10, 0.1)
		m._normalize()
		collect_list.append(imped(rec_place))
		g_list.append(fullsearch(10))
		print(m.side1.L)
	print(f"collected isolated resistances at {rec_place} and gna_thresh")

def plot(length,matx):
	fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,4))
	ax = fig.add_subplot(projection='3d')
	x0 = [i for i in range(0, length*10, 1)]
	y0 = [i for i in range(0, m.main_shaft.nseg, 1)]
	X0,Y0 = np.meshgrid(x0,y0)
	Z0 = matx
	ax.plot_surface(X0/10, Y0, Z0,alpha=0.5, cmap = cmap.viridis)
	ax.set_xlabel('length of side branches in lambda')
	ax.set_ylabel('node along main shaft')
	ax.set_zlabel('input resistance')
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

m = Resist_cell_1b(0)
m.prop_site.connect(m.main_shaft(1))
m.parent.L = 118
m.side1.L = 118
stim = h.IClamp(m.parent(0.5))
stim.amp = 200 #nA
stim.dur = 5 #ms
stim.delay = 0.3125 #ms
rec = APRecorder(m.prop_site)

# length = 3
# resist_collect = np.ones((m.main_shaft.nseg, 10))
# gna_collect = np.ones((m.main_shaft.nseg, 10))
# resist_list = []
# search_list = []




