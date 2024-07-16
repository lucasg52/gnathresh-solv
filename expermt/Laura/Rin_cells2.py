from cells.tapertypes import BaseExpCell
from neuron import h
from cells import kinetics
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
h.load_file("stdrun.hoc")


class Rin_cell_1(BaseExpCell):
	def __init__(self, gid):
		self.gid = gid

		self.stim_b = h.Section("stim_b", self)
		sb = self.stim_b
		self.side1 = h.Section("side1", self)
		s1 = self.side1

		self.stim_b.diam = 0.2
		self.side1.diam = 0.2
		self.stim_b.L = 400
		self.side1.L = 600


		super().__init__(0.2,3,gid)

	def _connect(self):
		super()._connect()
		self.stim_b.connect(self.main_shaft(0.3))
		self.prop_site.connect(self.main_shaft(1))
		self.side1.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		super()._setup_morph()
		self.IS.diam = self.IS_diam
		self.prop_site.L = 2*elength(self.prop_site)
		self.main_shaft.L = 4*elength(self.main_shaft)

	def _setup_bioph(self):
		super()._setup_bioph()
		self.all = [self.stim_b, self.side1, self.main_shaft, self.IS, self.prop_site, self.soma]
		for sec in [self.stim_b, self.side1, self.main_shaft, self.IS, self.prop_site]:
			kinetics.insmod_Traub(sec, "axon")
		kinetics.insmod_Traub(self.soma, "soma")

	def setgna(self, gna):
		for sec in self.soma.wholetree():
			if sec is not self.soma:
				if sec is not self.IS:
					sec.gbar_nafTraub = gna
					sec.gbar_kdrTraub = gna

	def getgna(self):
		gna = self.main_shaft.gbar_nafTraub
		for sec in self.soma.wholetree():
			if sec is not self.soma:
				if sec is not self.IS:
					assert(sec.gbar_nafTraub == gna)
		return gna

	def __repr__(self):
		return f"Resist[{self.gid}]"




class Rin_cell_1y(BaseExpCell):
	def __init__(self, gid):
		self.gid = gid

		self.stim_b = h.Section("stim_b", self)
		self.side1 = h.Section("side1", self)
		self.dau1 = h.Section("dau1", self)
		self.dau2 = h.Section("dau2", self)

		self.stim_b.diam = 0.2
		self.side1.diam = 0.2
		self.dau1.diam = self.dau2.diam = 0.215443469
		self.stim_b.L = 400
		self.side1.L = 300
		self.dau1.L = 300
		self.dau2.L = 300

		super().__init__(0.2,3,gid)

	def _connect(self):
		super()._connect()
		self.stim_b.connect(self.main_shaft(0.3))
		self.dau1.connect(self.side1(1))
		self.dau2.connect(self.side1(1))
		self.prop_site.connect(self.main_shaft(1))
		self.side1.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		super()._setup_morph()
		self.IS.diam = self.IS_diam
		self.prop_site.L = 2*elength(self.prop_site)
		self.main_shaft.L = 4*elength(self.main_shaft)

	def _setup_bioph(self):
		super()._setup_bioph()
		self.all = [self.stim_b, self.side1, self.dau1, self.dau2, self.main_shaft, self.IS, self.prop_site, self.soma]
		for sec in [self.stim_b, self.side1, self.dau1, self.dau2, self.main_shaft, self.IS, self.prop_site]:
			kinetics.insmod_Traub(sec, "axon")
		kinetics.insmod_Traub(self.soma, "soma")

	def setgna(self, gna):
		for sec in self.soma.wholetree():
			if sec is not self.soma:
				if sec is not self.IS:
					sec.gbar_nafTraub = gna
					sec.gbar_kdrTraub = gna

	def getgna(self):
		gna = self.main_shaft.gbar_nafTraub
		for sec in self.soma.wholetree():
			if sec is not self.soma:
				if sec is not self.IS:
					assert(sec.gbar_nafTraub == gna)
		return gna

	def __repr__(self):
		return f"Resist[{self.gid}]"


def set_ELen(section, length, dx):
	Lambda = elength(section)
	section.L = length * Lambda
	gnat.normalize_dlambda(section, dx)
	return

def setting_lengths(m, n):
	m.stim_b.L = set_ELen(m.stim_b, 4, 0.1)
	n.stim_b.L = set_ELen(n.stim_b, 4, 0.1)

	m.side1.L = set_ELen(m.side1, 6, 0.1)
	n.side1.L = set_ELen(n.side1, 3, 0.1)

	n.dau1.L = set_ELen(n.dau1, 3, 0.1)
	m.dau1.L = set_ELen(n.dau2, 3, 0.1)

def imped(part):
	imp_geter = h.Impedance()
	imp_geter.loc(part)
	imp_geter.compute(0)
	return imp_geter.input(part)

# def my_imped(part, m=m, n=n):
# 	for seg in part.wholetree():
# 		if part == m.side1:
# 			m.setgna(0)
# 		if part == n.side1:
# 			n.setgna(0)
# 	stim = h.IClamp(part(0))
# 	stim.amp = 200
# 	stim.dur = 51
# 	stim.delay = 5
# 	h.finitialize(-70)
# 	h.continuerun(55)
# 	return part.v / stim.amp


# def resist_in(sec):
# 		zz = h.Impedance()
# 		zz.loc(sec)
# 		zz.compute(0)
# 		return zz.input(sec)
#
# # m = Resist_cell(0)
# def stim_ste(loc):
# 	stim = h.IClamp(loc)
# 	stim.delay = 5
# 	stim.dur = 0.3125
# 	stim.amp = 200
#
# def run():
# 	h.finitialize(-69)
# 	h.continuerun(100)