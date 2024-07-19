from cells.base import BaseExpCell
from neuron import h
from matplotlib import pyplot as plt
from cells import kinetics
import numpy as np
h.load_file("stdrun.hoc")


class Resist_cell_2d(BaseExpCell):
	def __init__(self, gid):
		self.gid = gid

		self.parent = h.Section("parent",self)
		self.side1 = h.Section("side1", self)
		self.side2 = h.Section("side2", self)

		self.parent.L = 300
		self.parent.diam = 0.2
		self.side1.L = self.side2.L = 600
		self.side1.diam = self.side2.diam = 0.1

		super().__init__(0.2,3,gid)
	def _connect(self):
		super()._connect()
		self.parent.connect(self.main_shaft(0.012))
		self.side1.connect(self.parent(1))
		self.side2.connect(self.parent(1))

	def _setup_bioph(self):
		super()._setup_bioph()
		self.all = self.soma.wholetree()
		for sec in [self.parent, self.side1, self.side2, self.main_shaft, self.IS, self.prop_site]:
			kinetics.insmod_Traub(sec, "axon")
		kinetics.insmod_Traub(self.soma, "soma")

	def setgna(self, gna):
		for sec in self.all:
			if sec is not self.soma:
				if sec is not self.IS:
					sec.gbar_nafTraub = gna
					sec.gbar_kdrTraub = gna

	def getgna(self):
		gna = self.main_shaft.gbar_nafTraub
		for sec in self.all:
			if sec is not self.soma:
				if sec is not self.IS:
					assert(sec.gbar_nafTraub == gna)
		return gna
	def __repr__(self):
		return f"Resist[{self.gid}]"




class Resist_cell_1b(BaseExpCell):
	def __init__(self, gid):
		self.gid = gid

		self.parent = h.Section("parent",self)
		self.side1 = h.Section("side1", self)

		self.parent.L = 300
		self.parent.diam = 0.2
		self.side1.L = 600
		self.side1.diam = 0.1

		super().__init__(0.2,3,gid)
	def _connect(self):
		super()._connect()
		self.parent.connect(self.main_shaft(0))
		self.side1.connect(self.parent(0.45))

	def _setup_bioph(self):
		super()._setup_bioph()
		self.all = self.soma.wholetree()
		for sec in [self.parent, self.side1, self.main_shaft, self.IS, self.prop_site]:
			kinetics.insmod_Traub(sec, "axon")
		kinetics.insmod_Traub(self.soma, "soma")

	def setgna(self, gna):
		for sec in self.all:
			if sec is not self.soma:
				if sec is not self.IS:
					sec.gbar_nafTraub = gna
					sec.gbar_kdrTraub = gna

	def getgna(self):
		gna = self.main_shaft.gbar_nafTraub
		for sec in self.all:
			if sec is not self.soma:
				if sec is not self.IS:
					assert(sec.gbar_nafTraub == gna)
		return gna
	def __repr__(self):
		return f"Resist[{self.gid}]"




def resist_in(sec):
		zz = h.Impedance()
		zz.loc(sec)
		zz.compute(0)
		return zz.input(sec)

# m = Resist_cell(0)
def stim_ste(loc):
	stim = h.IClamp(loc)
	stim.delay = 5
	stim.dur = 0.3125
	stim.amp = 200

def run():
	h.finitialize(-69)
	h.continuerun(100)