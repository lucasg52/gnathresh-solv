from neuron import h
import numpy as np
from matplotlib import pyplot as plt
from ..cells.base import BaseExpCell
from ..tools.apdeath import DeathWatcher
from ..cells import kinetics as kin
from .. import eq
from ..tools import environment as e
from ..tools.checksum import GeomChecksum as Chksum
from ..tools.aprecorder import APRecorder
from ..visual import movie

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

e.dt = pow(2,-6)

e.m = m = NoISCell(pow(2,-5), 3)

e.stim = stim = h.IClamp(m.parent(1))
stim.amp = 100
stim.dur = 2/16
stim.delay = 1

e.aprec= aprec = APRecorder(m.main_shaft, ran = 0.5)

death = DeathWatcher(m.main_shaft(0), m.main_shaft(0.5), tstop = 1.5, recinterval = m.dx)

def proptest(gbar):
    e.prerun(gbar)
    death.run()
    return aprec.proptest()

def timetest(gbar):
    e.prerun(gbar)
    death.run()
    return death.getdeathtime()

e.proptest_basic = proptest


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

check = Chksum(m)

