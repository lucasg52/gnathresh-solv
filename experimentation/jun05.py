from neuron import h
from neuron.units import ms, mV
from neuron.units import μm as microm
import matplotlib.pyplot as plt
#import sys
from tutorialclasses import BallAndStick
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
            sec.insert ("hh")
            sec.insert ("pas")

        for seg in self.soma:
            seg.hh.gnabar = 0.12
            seg.hh.gkbar = 0.036
            seg.hh.gl = 0.0003
            seg.hh.el = -54.3 * mV
        for seg in self.dend:
            seg.pas.g = 0.001
            seg.pas.e = -65 * mV

    def __repr__(self):
        return "BallAndStick[{}]".format(self._gid)

class modBAS(BallAndStick):
    def __init__ (self,gid):
        super().__init__(gid)
        self.setup2()
    def setup2(self):
        self.axon = h.Section(cell = self, name = "3")
        self.axon.connect(self.soma(1))
        self.axon.L = 200* microm
        self.axon.nseg = 50
        self.axon.insert("hh")
        #self.axon.insert("pas")

        for seg in self.axon:
            seg.hh.gnabar = 0.12
            seg.hh.gkbar = 0.036
            seg.hh.gl = 0.0003
            seg.hh.el = -54.3 * mV
            #seg.pas.g = 0.001
            #seg.pas.e = -65 * mV

m = modBAS(1)
m.dend.nseg = 20
m.dend.L = 200 * microm


stim = h.IClamp(m.soma(0))
stim.delay = 5
stim.dur = 1
stim.amp = 0.05



somaV = h.Vector().record(m.soma(0.5)._ref_v)
axonV = h.Vector().record(m.axon(0.5)._ref_v)
dendV = h.Vector().record(m.dend(1)._ref_v)


arrV = [h.Vector().record(m.dend(d/5)._ref_v) for d in range (0,5)]

t = h.Vector().record(h._ref_t)

h.finitialize(-65 * mV)
h.continuerun(50 * ms)

ga = plt.plot(t,axonV, label = "axonV")
gs = plt.plot(t,somaV, label = "somaV")
gd = plt.plot(t,dendV,label = "dendV")

#stdout = sys.stdout
#sys.stdout = fp = open("out.txt","w")
#help(plt.Figure)
#sys.stdout = stdout
#fp.close()
#test 123
