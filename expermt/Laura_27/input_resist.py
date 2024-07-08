from gnatsolv.cells.tapertypes import *
from neuron import h
import matplotlib.pyplot as plt
h.load_file("stdrun.hoc")

m = ExpCell_3dtaper(0.2,3)

stim = h.IClamp(m.prop_site(1))
stim.delay = 5
stim.dur = 0.3125
stim.amp = 200

def run():
	h.finitialize(-69)
	h.continuerun(100)

def imped(place):
	zz = h.Impedance()
	zz.loc(part)
	zz.compute(0)
	return zz.input(part)
	
def graph(x, title, xlabel, ylabel):
	plt.plot(x)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid()
	plt.show()

def find_imp(imp_list,part):
	run()
	for seg in part:
		#print(imped(seg))
		Imp_list.append(imped(seg))
	return f"Impedances found for {part}"
