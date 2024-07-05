from neuron import h
#from gnatsolv.cells.adoptedeq import elength
h.load_file("stdrun.hoc")

class branch():
	def __init__(self,gid):
		self.gid = gid
		self.main_sec = h.Section("main_sec", self)
		self.side1 = h.Section("side1",self)
		self.side2 = h.Section("side2",self)
		self.side1.connect(self.main_sec(1))
		self.side2.connect(self.main_sec(1))
		self.all = self.main_sec.wholetree()
		self._setup_morph()
		self._setup_bioph()
		

	def _setup_morph(self):
		self.main_sec.L = 300
		self.main_sec.diam = 10
		self.side1.L = self.side2.L = 600
		self.side1.diam = self.side2.diam = 5

	def _setup_bioph(self):
		for sec in self.all:
			sec.insert("pas")	# using default pas parameters (?)

	def __repr__(self):
		return f"Branch[{self.gid}]"


def imped(part):
	zz = h.Impedance()
	zz.loc(part)
	zz.compute(0)
	return zz.input(part)
