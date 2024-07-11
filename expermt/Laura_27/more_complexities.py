# from cells.base import BaseExpCell
# from neuron import h
# from matplotlib import pyplot as plt
# from cells import kinetics
# import numpy as np
# h.load_file("stdrun.hoc")
#
# class Resist_comx_cell(BaseExpCell):
# 	def __init__(self, gid):
# 		self.gid = gid
#
# 		self.parent = h.Section("parent",self)
# 		for i in range(ncells):
#             self.side{i} = h.Section(f"side{i}", self)
#
# 		self.parent.L = 300
# 		self.parent.diam = 0.2
# 		self.side1.L = self.side2.L = 600
# 		self.side1.diam = self.side2.diam = 0.1
#
# 		super().__init__(0.2,3,gid)
# 	def _connect(self):
# 		super()._connect()
# 		self.parent.connect(self.main_shaft(0.012))
# 		self.side1.connect(self.parent(1))
# 		self.side2.connect(self.parent(1))
#
# 	def _setup_bioph(self):
# 		super()._setup_bioph()
# 		self.all = self.soma.wholetree()
# 		for sec in [self.parent, self.side1, self.side2, self.main_shaft, self.IS, self.prop_site]:
# 			kinetics.insmod_Traub(sec, "axon")
# 		kinetics.insmod_Traub(self.soma, "soma")
#
# 	def setgna(self, gna):
# 		for sec in self.all:
# 			if sec is not self.soma:
# 				if sec is not self.IS:
# 					sec.gbar_nafTraub = gna
# 					sec.gbar_kdrTraub = gna
#
# 	def getgna(self):
# 		gna = self.main_shaft.gbar_nafTraub
# 		for sec in self.all:
# 			if sec is not self.soma:
# 				if sec is not self.IS:
# 					assert(sec.gbar_nafTraub == gna)
# 		return gna
# 	def __repr__(self):
# 		return f"Resist[{self.gid}]"

from neuron import h
h.load_file("stdrun.hoc")
def my_imped(loc):
	stim = h.IClamp(loc)
	stim.amp = 200
	stim.dur = 51
	stim.delay = 5
	h.finitialize(-70)
	h.continuerun(55)
	return loc.v/stim.amp