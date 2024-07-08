from gnatsolv.cells.base import BaseExpCell
from neuron import h
from matplotlib import pyplot as plt
from gnatsolv.cells import kinetics


class resist_cell(BaseExpCell):
	def __init__(self, gid):
		self.gid = gid

		self.parent = h.Section("parent",self)
		self.side1 = h.Section("side1", self)
		self.side2 = h.Section("side2", self)

		self.parent.L = 300
		self.parent.diam = 10
		self.side1.L = self.side2.L = 600
		self.side1.diam = self.side2.diam = 5

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
	def __repr__(self):
		return f"Resist[{self.gid}]"

def resist_in(sec):
		zz = h.Impedance()
		zz.loc(sec)
		zz.compute(0)
		return zz.input(sec)