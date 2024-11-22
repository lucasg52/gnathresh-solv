from neuron import h
import numpy as np
from matplotlib import pyplot as plt
from gnatsolv.cells.base import BaseExpCell
from gnatsolv.tools.apdeath import DeathRec
from gnatsolv.cells import kinetics as kin
from gnatsolv import eq
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.solver.delayclimb import DelayClimb
from gnatsolv.solver.searchclasses import ExpandingSearch
#from ..tools.aprecorder import APRecorder
from visual import movie # not sure what to do with the visual dir


h.load_file("stdrun.hoc")

class NoISCell(BaseExpCell):
    def __repr__(self):
        return f"NoISCell[{self.gid}]"

    def _create_secs(self):
        self.parent = h.Section(name = "parent", cell = self)

    def _setup_bioph(self):
        for sec in [getattr(self, n) for n in ['IS', 'main_shaft', 'prop_site', 'parent']]:
            kin.insmod_Traub(sec, "axon")
        kin.insmod_Traub(self.soma, "soma")

    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.main_diam
        self.parent.diam = self.prop_site.diam
        self.parent.L = 2*eq.elength(self.prop_site)
        self._normalize()

    def _connect(self):
        super()._connect()
        self.parent.connect(self.main_shaft(0.25))

e = DeathEnviro(None, None, None)

e.m = m = NoISCell(pow(2,-5), 3)

e.stim = stim = h.IClamp(m.parent(1))
stim.amp = 100
stim.dur = 2/16
stim.delay = 0.5

e.deathrec = e.aprec = deathrec = DeathRec(m.main_shaft, m.main_shaft, tstop = 1)

search = ExpandingSearch(
        lim_hi = 0.45, lim_lo = 0.1,
        lo = 0.14, hi = 0.15,
        propatest = e.proptest)
pnts = []
while len(pnts) < 3:
    a = search.a
    search.searchstep()
    if not e.aprec.proptest():
        pnts.append([a, e.deathrec.getdeathtime()])

def timeproptest(gbar):
    prop = e.proptest(gbar)
    delay = e.deathrec.getdeathtime()
    return prop, delay

climb = DelayClimb( timeproptest, pnts)

#def proptest_withtime(self, gbar):
#    ret = type(e).proptest(self, gbar)
#    pnts.append([gbar, self.deathrec.getdeathtime()])
#    return ret
#e.proptest = proptest_withtime



def timetest(gbar):
    e.prerun(gbar)
    deathrec.run()
    return deathrec.getdeathtime()

def timeplot(lo,hi,res = 64):
    xarr = np.linspace(lo,hi,res)
    yarr = [timetest(gbar) for gbar in xarr]
    plt.plot(xarr,yarr)
    plt.show()
    return xarr, yarr

def prerun():
    gbar = m.IS.gbar_nafTraub
    e.prerun(gbar)

movie.prerun = prerun
movie.stepsize = 0.125

