import time
from neuron import h
from .tapertypes import BaseTaperCell
from . import kinetics
from .adoptedeq import elength
from ..tools.aprecorder import APRecorder
from ..solver.searchclasses import ExpandingSearch
h.load_file("stdrun.hoc")

__tstop__ = h.tstop = 15
class RinCell(BaseTaperCell):
	def __init__(self, gid):
		self.gid = gid
		self.rin_lst = []
		self.gna_lst = []
		self.diff_gna = []
		self.diff_rin = []
		self.dx = pow(2,-6)
		self.est = 0.1497

		super().__init__(self.dx,3,gid)

	def _create_secs(self):
		self.parent = h.Section("parent", self)
		self.side1 = h.Section("side1", self)

	def _connect(self):
		super()._connect()
		self.parent.connect(self.main_shaft(0.3))
		self.prop_site.connect(self.main_shaft(1))
		self.side1.connect(self.main_shaft(0.6))

	def _setup_morph(self):
		super()._setup_morph()

		self.parent.diam = 0.2
		self.side1.diam = 0.2
		self.parent.L = 400
		self.side1.L = 600


		#self.IS.diam = self.IS_diam 
		# removed so that IS can be tapered
		self.prop_site.L = 2*elength(self.prop_site)
		self.main_shaft.L = 4*elength(self.main_shaft)
		self.parent.L = 4 * elength(self.parent)

	def _setup_bioph(self):
		super()._setup_bioph()
		self.all = [self.parent, self.side1, self.main_shaft, self.IS, self.prop_site, self.soma]
		for sec in [self.parent, self.side1, self.main_shaft, self.IS, self.prop_site]:
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
		self.stim = h.IClamp(self.parent(loc))
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

# fullsolve should be external. No reason to have it part of the class itself.
# recommend using tools.environment, but you can do whatever you want
# only reason is that it is theoretically easier for others to read, since you are not copying and pasting code
	def getRin(self, sec):  # Renamed, better to have a method start with a lowercase anyways
		imp_geter = h.Impedance()
		imp_geter.loc(sec)
		imp_geter.compute(0)
		return imp_geter.input(sec)
# I suppose this is the only "numerical" part of your class that i would keep inside, only because it fits the name



	# def alt_Rin(self, loc):
	# 	h.dt = 0.5
	# 	self.side1.gbar_nafTraub = 0
	# 	self.side1.gbar_kdrTraub = 0
	# 	stim = h.IClamp(loc)
	# 	stim.amp = 200
	# 	stim.dur = 100
	# 	stim.delay = 5
	# 	h.finitialize(-70)
	# 	h.continuerun(100)
	# 	return loc.v/stim.amp

	def __repr__(self):
		return f"RinCell[{self.gid}]"
