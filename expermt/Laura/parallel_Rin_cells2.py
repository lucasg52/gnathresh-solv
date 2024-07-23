import time
start_everything = time.perf_counter()

from cells.tapertypes import BaseExpCell
from neuron import h
from cells import kinetics
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from tools.aprecorder import APRecorder
from solver.searchclasses import ExpandingSearch
import math

h.nrnmpi_init()
pc = h.ParallelContext()

h.load_file("stdrun.hoc")

__tstop__ = h.tstop = 15
class Rin_cell_1(BaseExpCell):
	def __init__(self, gid):
		self.gid = gid
		pc.set_gid2node(gid, pc.id())

		self.stim_b = h.Section("stim_b", self)
		sb = self.stim_b
		self.side1 = h.Section("side1", self)
		s1 = self.side1

		self.stim_b.diam = 0.2
		self.side1.diam = 0.2
		self.stim_b.L = 400
		self.side1.L = 600

		self.rin_base = []
		self.gna_base = []

		super().__init__(0.025,3,gid)

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

	def stim_setup(self, loc):
		self.stim = h.IClamp(self.stim_b(loc))
		self.stim.amp = 200
		self.stim.delay = 5
		self.stim.dur = 5/16
		self.rec = APRecorder(self.prop_site)
		pc.cell(self.gid, self.rec)

	def proptest(self, gbar):
		self.setgna(gbar)
		h.finitialize(-69)
		h.continuerun(__tstop__)
		return self.rec.proptest()

	def fullsolve(self, a, err=2e-3, acc=pow(2, -30), maxsteps=45, tstop_init=None):
		global __ERRFLAG__
		ptstart = time.process_time()
		if tstop_init is None:
			__tstop__ = self.stim.delay + 10
		else:
			__tstop__ = tstop_init
		search = ExpandingSearch(a - err, a + err, self.proptest, lim_lo=0, lim_hi=0.45)
		for i in range(maxsteps):
			if search.searchstep():
				break
			if self.rec.proptest():
				if self.rec.recorded[0] > __tstop__ - 6:
					__tstop__ += 3
					print(__tstop__)
			if search.hi - search.lo <= acc:
				break
		print(time.process_time() - ptstart)
		if i == maxsteps - 1:
			print("WARNING!!! U REACHED THE MAX STEPS!!")
		if abs(search.a - a) > 4 * err:
			__ERRFLAG__ = abs(search.a - a)
		return search.a

	def Rin(self, sec):
		imp_geter = h.Impedance()
		imp_geter.loc(sec)
		imp_geter.compute(0)
		return imp_geter.input(sec)

	def alt_Rin(self, loc):
		h.dt = 0.5
		self.side1.gbar_nafTraub = 0
		self.side1.gbar_kdrTraub = 0
		stim = h.IClamp(loc)
		stim.amp = 200
		stim.dur = 100
		stim.delay = 5
		h.finitialize(-70)
		h.continuerun(100)
		return loc.v/stim.amp

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

		self.rin_eqi = []
		self.gna_eqi = []

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

	def stim_setup(self, loc):
		self.stim = h.IClamp(self.stim_b(loc))
		self.stim.amp = 200
		self.stim.delay = 5
		self.stim.dur = 5/16
		self.rec = APRecorder(self.prop_site)

	def proptest(self, gbar):
		self.setgna(gbar)
		h.finitialize(-69)
		h.continuerun(__tstop__)
		return self.rec.proptest()

	def fullsolve(self, a, err=2e-3, acc=pow(2, -30), maxsteps=45, tstop_init=None):
		global __ERRFLAG__
		ptstart = time.process_time()
		if tstop_init is None:
			__tstop__ = self.stim.delay + 10
		else:
			__tstop__ = tstop_init
		search = ExpandingSearch(a - err, a + err, self.proptest, lim_lo=0, lim_hi=0.45)
		for i in range(maxsteps):
			if search.searchstep():
				break
			if self.rec.proptest():
				if self.rec.recorded[0] > __tstop__ - 6:
					__tstop__ += 3
					print(__tstop__)
			if search.hi - search.lo <= acc:
				break
		print(time.process_time() - ptstart)
		if i == maxsteps - 1:
			print("WARNING!!! U REACHED THE MAX STEPS!!")
		if abs(search.a - a) > 4 * err:
			__ERRFLAG__ = abs(search.a - a)
		return search.a

	def Rin(self, sec):
		imp_geter = h.Impedance()
		imp_geter.loc(sec)
		imp_geter.compute(0)
		return imp_geter.input(sec)

	def alt_Rin(self, loc):
		h.dt = 0.5
		side = self.side1.wholetree()
		for sec in [self.side1, self.dau1, self.dau2]:
			sec.gbar_nafTraub = 0
			sec.gbar_kdrTraub = 0
		stim = h.IClamp(loc)
		stim.amp = 200
		stim.dur = 100
		stim.delay = 5
		h.finitialize(-70)
		h.continuerun(100)
		return loc.v/stim.amp

	def __repr__(self):
		return f"Cell_2y[{self.gid}]"

class Rin_cell_3y(BaseExpCell):
	def __init__(self, gid):
		self.gid = gid

		self.stim_b = h.Section("stim_b", self)
		self.side1 = h.Section("side1", self)
		self.dau1 = h.Section("dau1", self)
		self.dau2 = h.Section("dau2", self)
		self.dau3 = h.Section("dau3", self)

		self.stim_b.diam = 0.2
		self.side1.diam = 0.2
		self.dau1.diam = self.dau2.diam = self.dau3.diam=0.164414383
		self.stim_b.L = 400
		self.side1.L = self.dau1.L=self.dau2.L = self.dau3.L = 300

		super().__init__(0.2,3,gid)

		self.rin_eqi2 = []
		self.gna_eqi2 = []

	def _connect(self):
		super()._connect()
		self.stim_b.connect(self.main_shaft(0.3))
		self.dau1.connect(self.side1(1))
		self.dau2.connect(self.side1(1))
		self.dau3.connect(self.side1(1))
		self.prop_site.connect(self.main_shaft(1))
		self.side1.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		super()._setup_morph()
		self.IS.diam = self.IS_diam
		self.prop_site.L = 2*elength(self.prop_site)
		self.main_shaft.L = 4*elength(self.main_shaft)

	def _setup_bioph(self):
		super()._setup_bioph()
		self.all = self.soma.wholetree()
		for sec in [self.stim_b, self.side1, self.dau1, self.dau2, self.dau3, self.main_shaft, self.IS, self.prop_site]:
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

	def stim_setup(self, loc):
		self.stim = h.IClamp(self.stim_b(loc))
		self.stim.amp = 200
		self.stim.delay = 5
		self.stim.dur = 5/16
		self.rec = APRecorder(self.prop_site)

	def proptest(self, gbar):
		self.setgna(gbar)
		h.finitialize(-69)
		h.continuerun(__tstop__)
		return self.rec.proptest()

	def fullsolve(self, a, err=2e-3, acc=pow(2, -30), maxsteps=45, tstop_init=None):
		global __ERRFLAG__
		ptstart = time.process_time()
		if tstop_init is None:
			__tstop__ = self.stim.delay + 10
		else:
			__tstop__ = tstop_init
		search = ExpandingSearch(a - err, a + err, self.proptest, lim_lo=0, lim_hi=0.45)
		for i in range(maxsteps):
			if search.searchstep():
				break
			if self.rec.proptest():
				if self.rec.recorded[0] > __tstop__ - 6:
					__tstop__ += 3
					print(__tstop__)
			if search.hi - search.lo <= acc:
				break
		print(time.process_time() - ptstart)
		if i == maxsteps - 1:
			print("WARNING!!! U REACHED THE MAX STEPS!!")
		if abs(search.a - a) > 4 * err:
			__ERRFLAG__ = abs(search.a - a)
		return search.a

	def Rin(self, sec):
		getter = h.Impedance()
		getter.loc(sec)
		getter.compute(0)
		return getter.input(sec)

	def alt_Rin(self, loc):
		h.dt = 0.5
		side = self.side1.wholetree()
		for sec in [self.side1, self.dau1, self.dau2, self.dau3]:
			sec.gbar_nafTraub = 0
			sec.gbar_kdrTraub = 0
		stim = h.IClamp(loc)
		stim.amp = 200
		stim.dur = 100
		stim.delay = 5
		h.finitialize(-70)
		h.continuerun(100)
		return loc.v/stim.amp

	def __repr__(self):
		return f"Cell_3y[{self.gid}]"


class AdjSearch(): # should change name to BinSearch ?
    """
    Sets up a binary search
        lo, hi,           the assumed window (lower and upper bounds) in which the solution lies
        propatest,        the function that will return True if propagation succeeds, False otherwise
        a = math.nan,     optionally, a first guess can be provided (otherwise is the median between lo and hi)
        stopcond = None   for use of fullsearch() . if left as None, will throw warning, and not iterate

    """
    def __init__(
                 self,
                 lo, hi,
                 propatest,
                 a = math.nan,
                ):
        self.lo = lo
        self.hi = hi
        self.term = False
        self.propatest = propatest
        if math.isnan(a):
            self.a = (lo + hi) / 2

    def searchstep(self):
        """ Iterate the search
        pass approximation (a) to propatest, if true is returned, assume approximation too high, if false, vise-versa.
        Returns: None
        """
        if self.propatest(self.a):
            self.hi = self.a
        else:
            self.lo = self.a
        self.a = (self.lo + self.hi) / 2
