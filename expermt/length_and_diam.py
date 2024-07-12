import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from neuron import h
from expermt.Laura_27.testing_Rin import Resist_cell_2d #, Resist_cell_1b
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from tools.aprecorder import APRecorder
from solver.searchclasses import BinSearch
from expermt.var_Rin import fullsearch
h.load_file("stdrun.hoc")

def my_imped(part):
	stim = h.IClamp(part)
	stim.amp = 200
	stim.dur = 51
	stim.delay = 5
	h.finitialize(-70)
	h.continuerun(55)
	return part.v/stim.amp
	#treturn f"input resistance at {part} = {part.v/stim.amp} mV/nA"

def diam_lam_resist_col(min, max, d_dim, r_collector,g_collector, cell, rec_place):
    j=0
    k=0
    l = 0
	for seg in cell.main_shaft:
		cell.parent.connect(seg)
		for i in range(min,max,d_dim):
			cell.side1.diam = cell.side2.diam = i/10
			cell._normalize()
			r_collector[j][i-1]*=my_imped(rec_place)
			#g_collector[j][i-1] *= fullsearch(10)
			print(f"{j},{i - 1}: {cell.side1.diam}")
			for i in range(min, max, d_dim):
				cell.side1.diam = cell.side2.diam = i / 10
				cell._normalize()

				g_collector[j][i - 1] *= fullsearch(10)
				print(f"{j},{i - 1}: {cell.side1.diam}")
                j += 1
            l += 1
        k += 1
	print(f"successfully found input resistances at {rec_place}")