from neuron import h
from neuron.units import ms, mV
from neuron.units import μm as microm
import matplotlib.pyplot as plot

h.load_file('stdrun.hoc')
w  =h.Section(name="soma")
class BAS:
    def __init__ (self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()
    def _setup_morphology(self):
        self.soma = h.Section(cell=self, name = "2")
        self.dend = h.Section(cell=self, name = "1")
        self.dend.connect(self.soma)
        self.all = self.soma.wholetree()
    def _setup_biophysics(self):
        print("setting up biophys")
        for sec in self.all:
            sec.Ra = 100
            sec.cm = 1

        self.soma.insert("hh")
        for seg in self.soma:
            seg.hh.gnabar = 0.12
            seg.hh.gkbar = 0.036
            seg.hh.gl = 0.0003
            seg.hh.el = -54.3 * mV

        self.dend.insert("pas")

        for seg in self.dend:
            seg.pas.g = 0.001
            seg.pas.e = -65 * mV

    def __repr__(self):
        return "BallAndStick[{}]".format(self._gid)



m = BAS(1)


h.finitialize(-65 * mV)
stim = h.IClamp(m.dend(1))
stim.get_segment()
somaV = h.Vector().record(m.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)
