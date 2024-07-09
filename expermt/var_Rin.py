import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from expermt.Laura_27.testing_Rin import Resist_cell, resist_in
from neuron import h
h.load_file("stdrun.hoc")
from cells.adoptedeq import elength
import cells.adoptedeq as gnat

def imped(part):
	zz = h.Impedance()
	zz.loc(part)
	zz.compute(0)
	return zz.input(part)

def set_ELen(section, length, dx):
	Lambda = elength(section)
	section.L = length*Lambda
	gnat.normalize_dlambda(section, dx)
	return
	#   print(Lambda)

def collect_Rin(length, collector, m, rec_place):
	j=-1
	for seg in m.main_shaft:
		j+=1
		m.parent.connect(seg)
		for i in range(1,length*10+1,1):
			set_ELen(m.side1, i/10, 0.1)
			set_ELen(m.side2,i/10,0.1)
			m._normalize()
			#print(f"{j},{i-1}: {m.parent.nseg}")
			collector[j][i-1]*=imped(rec_place)
	print(f"successfully gotten input resistances at {rec_place}")

def isolate_bchang(rec_place, collect_list):
	for i in range(1, length * 10 + 1, 1):
		set_ELen(m.side1, i / 10, 0.1)
		set_ELen(m.side2, i / 10, 0.1)
		m._normalize()
		collect_list.append(imped(rec_place))
	print(f"collected isolated resistances at {rec_place}")

def plot(length,matx, sec):
	fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,4))
	ax = fig.add_subplot(projection='3d')
	x0 = [i for i in range(0, length*10, 1)]
	y0 = [i for i in range(0, sec.nseg, 1)]
	X0,Y0 = np.meshgrid(x0,y0)
	Z0 = matx
	ax.plot_surface(X0/10, Y0, Z0,alpha=0.5, cmap = cmap.viridis)
	ax.set_xlabel('length of side branches in lambda')
	ax.set_ylabel('node along main shaft')
	ax.set_zlabel('input resistance')
	plt.show()

def stim_func(site):
	stim = h.IClamp(site)
	stim.amp = 200 #nA
	stim.dur = 5 #ms
	stim.delay = 0.3125 #ms

def run():
	h.finitialize(-70) #mV
	h.continuerun(15)#ms


m = Resist_cell(0)
m.prop_site.connect(m.main_shaft(1))
m.parent.L = 118
length = 6
resist_collect = np.ones((m.main_shaft.nseg, length*10))
resist_list = []




