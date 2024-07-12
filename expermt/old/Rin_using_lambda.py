from neuron import h
#from gnatsolv.cells.adoptedeq import elength
h.load_file("stdrun.hoc")

class branch():
	def __init__(self,gid):
		self.gid = gid
		self.msec = h.Section("msec", self) #main section
		self.side1 = h.Section("side1",self) #a side branch
		self.side2 = h.Section("side2",self) #another side branch
		self.side1.connect(self.msec(1))
		self.side2.connect(self.msec(1))
		self.all = self.msec.wholetree()
		self._setup_morph()
		self._setup_bioph()
		

	def _setup_morph(self):
		self.msec.L = 300
		self.msec.diam = 10
		self.side1.L = self.side2.L = 600
		self.side1.diam = self.side2.diam = 5

	def _setup_bioph(self):
		for sec in self.all:
			sec.insert("pas")

	def __repr__(self):
		return f"Branch[{self.gid}]"


def imped(part): # input: at where is the input resistance suppose to be measured
	zz = h.Impedance()
	zz.loc(part)
	zz.compute(0)
	return zz.input(part)
