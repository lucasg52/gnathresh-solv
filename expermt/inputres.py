from neuron import h
#from gnatsolv.cells.tools import APRecorder
from gnatsolv.cells.tapertypes import ExpCell_notaper
from gnatsolv.solver import searchclasses
import matplotlib.pyplot as plt
h.load_file("stdrun.hoc")
m = ExpCell_notaper(0.2,3)
m.prop_site.connect(m.main_shaft(0.3))
#aprec = APRecorder(m.main_shaft, 0.9)
mystim = h.IClamp(m.prop_site(0.9))
mystim.delay = 3
mystim.amp = 200
mystim.dur = 5/16
h.dt  =1


