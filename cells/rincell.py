from neuron import h
from cells.tapertypes import BaseTaperCell
from cells import kinetics
from cells.adoptedeq import elength
from cells import adoptedeq as eq
from Tools.aprecorder import APRecorder
from solver.searchclasses import ExpandingSearch
import numpy as np
import time
h.load_file("stdrun.hoc")

__tstop__ = h.tstop = 15

class RinCell(BaseTaperCell):
	def __init__(self, gid):
		# sets up a function so each cell can have lists to store information, a set dx, a set gna estimate, a name (if you need it for how cells
		# are called, and a cstie (which is the point on a section where a branch is connected)
		self.gid = gid
		self.rin_lst = []
		self.gna_lst = []
		self.diff_gna = []
		self.diff_rin = []
		self.dx = pow(2,-6)
		self.est = 0.157
		self.name = 'base cell'
		self.csite = 0.6
		super().__init__(self.dx,3,gid)

	def _normalize(self):
		#sets up a function to normalize lengths of all branches
		for sec in self.all[1::]:
			eq.normalize_dlambda(sec, self.dx)
		self._taperIS()

	def _taperIS(self):
		#function that tapers the AIS, it is to be call once when setting up the cell
		n = self.IS.nseg
		taperarr = np.linspace(self.IS_diam, self.main_diam, n + 1)
		for seg, diam in zip(self.IS, taperarr):
			seg.diam = diam

	def _create_secs(self):
		#function that adds additional branches to the most basic cell model we have
		self.parent = h.Section("parent", self)
		self.side1 = h.Section("side1", self)
		self.prop_site2 = h.Section("prop_site2", self)

	def _connect(self):
		#function that connects branches to each other
		super()._connect()
		self.parent.connect(self.main_shaft(0.2))
		self.prop_site.connect(self.main_shaft(1))
		self.prop_site2.connect(self.prop_site(1))
		self.side1.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		#function that sets up morphology (only used for diameter and length)
		super()._setup_morph()
		self.parent.diam = self.side1.diam = 0.2
		self.prop_site.diam = self.prop_site2.diam = 0.6
		self.side1.L = 600
		self.prop_site.L = self.prop_site2.L = 2*elength(self.prop_site)
		self.main_shaft.L = 4*elength(self.main_shaft)
		self.parent.L = 4 * elength(self.parent)

	def _setup_bioph(self):
		#funciton that establishes biophysics (Traub parameters and variables)
		super()._setup_bioph()
		for sec in [self.IS, self.main_shaft, self.prop_site, self.prop_site2, self.parent, self.side1]:
			kinetics.insmod_Traub(sec, "axon")
		kinetics.insmod_Traub(self.soma, "soma")
		self._normalize()
		self._taperIS()

	def setgna(self, gna):
		#function that sets the gna for all non-soma and -AIS sections
		for sec in self.all:
			if sec is not self.soma:
				if sec is not self.IS:
					sec.gbar_nafTraub = gna
					sec.gbar_kdrTraub = gna

	def getgna(self):
		#prints out the gna for all non-soma and -AIS sections
		gna = self.main_shaft.gbar_nafTraub
		for sec in self.all:
			if sec is not self.soma:
				if sec is not self.IS:
					assert(sec.gbar_nafTraub == gna)
		return gna

	def setup_stim(self):
		#must be call in order for the cell to have a stim at 0.5 on the parent branch (all parameters are easily
		#after the funciton is called
		self.stim = h.IClamp(self.parent(0.5))
		self.stim.amp = 0.2
		self.stim.delay = 5
		self.stim.dur = 5/16
		# self.rec = APRecorder(self.prop_site, ran = 1)

	def prerun(self, gbar):
		#is necessary for the gna solver
		self.setgna(gbar)
		h.finitialize(-69)

	def getRin(self):
		#funciton that solvers for the input resistance using NEURON's solver
		imp = h.Impedance()
		imp.loc(self.main_shaft(0.2))
		imp.compute(0)
		return imp.input(self.main_shaft(0.2))

	def set_matx(self, row, col):
		#function that creates matrices to store cell specfic values
		self.gna_mtx = np.ones(shape=(row, col))
		self.rin_mtx = np.ones(shape=(row,col))
		self.mtx = np.ones(shape=(row,col))

	# def proptest(self, gbar):
	# 	self.setgna(gbar)
	# 	h.finitialize(-69)
	# 	h.continuerun(__tstop__)
	# 	return self.rec.proptest()
	#
	# def fullsolve(self, a, err=2e-3, acc=pow(2, -30), maxsteps=45, tstop_init=None):
	# 	global __ERRFLAG__
	# 	self.stim.amp = 0.2
	# 	ptstart = time.process_time()
	# 	if tstop_init is None:
	# 		__tstop__ = self.stim.delay + 10
	# 	else:
	# 		__tstop__ = tstop_init
	# 	search = ExpandingSearch(a - err, a + err, self.proptest, lim_lo=0, lim_hi=0.45)
	# 	for i in range(maxsteps):
	# 		if search.searchstep():
	# 			break
	# 		if self.rec.proptest():
	# 			if self.rec.recorded[0] > __tstop__ - 6:
	# 				__tstop__ += 3
	# 				print(__tstop__)
	# 		if search.hi - search.lo <= acc:
	# 			break
	# 	print(time.process_time() - ptstart)
	# 	if i == maxsteps - 1:
	# 		print("WARNING!!! YOU REACHED THE MAX STEPS!!")
	# 	if abs(search.a - a) > 4 * err:
	# 		__ERRFLAG__ = abs(search.a - a)
	# 	return search.a


	def __repr__(self):
		return f"Base[{self.gid}]"

#creating the Y-shaped side branch cell (aka the Y cell) class
class Rin_Ycell(RinCell):
	def __init__(self, gid):
		super().__init__(gid)

	def _create_secs(self):
		super()._create_secs()
		self.dau1 = h.Section("dau1", self)
		self.dau2 = h.Section("dau2", self)

	def _connect(self):
		super()._connect()
		self.dau1.connect(self.side1(1))
		self.dau2.connect(self.side1(1))

	def _setup_morph(self):
		super()._setup_morph()
		self.dau1.diam = self.dau2.diam = 0.125992105
		self.dau1.L = self.dau2.L = self.side1.L = 300

	def _setup_bioph(self):
		super()._setup_bioph()
		for sec in [self.dau1, self.dau2]:
			kinetics.insmod_Traub(sec, "axon")

	def __repr__(self):
		return f"Y_Cell[{self.gid}]"

#class for creating the w-shaped side branch cell (aka the W cell)
class Rin_Trident(Rin_Ycell):
	def __init__(self, gid):
		self.gid = gid
		super().__init__(gid)

	def _create_secs(self):
		super()._create_secs()
		self.dau3 = h.Section("dau3", self)

	def _connect(self):
		super()._connect()
		self.dau3.connect(self.side1(1))

	def _setup_morph(self):
		super()._setup_morph()
		self.dau1.diam = self.dau2.diam = self.dau3.diam=0.09614997135
		self.dau3.L = 300

	def _setup_bioph(self):
		super()._setup_bioph()
		kinetics.insmod_Traub(self.dau3, "axon")

	def __repr__(self):
		return f"Trident[{self.gid}]"

#class for creating the V-shaped side branch cell (aka the V cell)
class Rin_Vcell(RinCell):
	def __init__(self, gid):
		self.gid = gid
		super().__init__(gid)

	def _create_secs(self):
		super()._create_secs()
		self.dau1 = h.Section("dau1", self)

	def _connect(self):
		super()._connect()
		self.dau1.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		super()._setup_morph()
		self.side1.diam = 0.125992105
		self.dau1.diam = 0.125992105
		self.side1.L = self.dau1.L = 300

	def _setup_bioph(self):
		super()._setup_bioph()
		kinetics.insmod_Traub(self.dau1, "axon")

	def __repr__(self):
		return f"V[{self.gid}]"

class Rin_Wcell(Rin_Vcell):
	def __init__(self, gid):
		self.gid = gid
		super().__init__(gid)

	def _create_secs(self):
		super()._create_secs()
		self.dau2 = h.Section("dau2", self)

	def _connect(self):
		super()._connect()
		self.dau2.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		super()._setup_morph()
		self.side1.diam = self.dau1.diam = self.dau2.diam = 0.0961499714
		self.dau2.L = 300

	def _setup_bioph(self):
		super()._setup_bioph()
		kinetics.insmod_Traub(self.dau2, "axon")

	def __repr__(self):
		return f"W[{self.gid}]"

class Rin_W2cell(Rin_Wcell):
	def __init__(self, gid):
		self.gid = gid
		super().__init__(gid)

	def _create_secs(self):
		super()._create_secs()
		self.dau3 = h.Section("dau3", self)

	def _connect(self):
		super()._connect()
		self.dau3.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		super()._setup_morph()
		self.side1.diam = self.dau1.diam = self.dau2.diam = self.dau3.diam = 0.0793700526
		self.dau2.L = 300

	def _setup_bioph(self):
		super()._setup_bioph()
		kinetics.insmod_Traub(self.dau3, "axon")

	def __repr__(self):
		return f"4_side[{self.gid}]"

#class for creating the T-shaped side branch cell (aka the T cell)
class Rin_Tcell(RinCell):
	def __init__(self, gid):
		self.gid = gid
		super().__init__(gid)

	def _create_secs(self):
		super()._create_secs()
		self.dau1 = h.Section("dau1", self)

	def _connect(self):
		super()._connect()
		self.dau1.connect(self.side1(0.5))

	def _setup_morph(self):
		super()._setup_morph()
		self.dau1.diam = 0.05
		self.dau1.L = 100

	def _setup_bioph(self):
		super()._setup_bioph()
		kinetics.insmod_Traub(self.dau1, "axon")

	def __repr__(self):
		return f"T[{self.gid}]"

#class for creating a cell with two side branches (aka 2bb cell, which stand for the cell having 2 base branches)
class Rin_2bbcell(RinCell):
	def __init__(self, gid):
		self.gid = gid
		super().__init__(gid)

	def _create_secs(self):
		super()._create_secs()
		self.side2 = h.Section("side2", self)

	def _connect(self):
		super()._connect()
		self.side1.connect(self.main_shaft(0.5))
		self.side2.connect(self.main_shaft(0.7))

	def _setup_morph(self):
		super()._setup_morph()
		self.side2.diam = 0.2
		self.side1.L = self.side2.L = 600

	def _setup_bioph(self):
		super()._setup_bioph()
		kinetics.insmod_Traub(self.side2, "axon")

	def __repr__(self):
		return f"2bb[{self.gid}]"