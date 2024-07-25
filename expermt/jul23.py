from neuron import h
from ..cells.base import BaseExpCell as Base
from ..cells import kinetics as kin
from ..tools import environment as e
from matplotlib import pyplot as plt

def ngui():
    from neuron import gui
    print(gui)


class Cell(Base):
    def __repr__(self):
        return(f"pycell[{self.gid}]")
    def _create_secs(self):
        self.side = h.Section(name = "side", cell = self)
        self.main2 = h.Section(name = "main2", cell = self)
    def _setup_bioph(self):
        for sec in [self.IS, self.main_shaft, self.prop_site, self.side, self.main2]:
            kin.insmod_Traub(sec, "axon")
        kin.insmod_Traub(self.soma, "soma")
    def _connect(self):
        super()._connect()
        self.main2.connect(self.IS(1))
        self.main_shaft.connect(self.main2(1))
        self.prop_site.connect(self.main_shaft(1))
        self.side.connect(self.main2(1))
    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.IS_diam
        self.side.L = self.prop_site.L * 3
        self.side.diam = self.prop_site.diam
        self.main2.diam = self.main_diam
        self.main2.L = self.main_shaft.L / 8
        self.main_shaft.L -= self.main_shaft.L / 8
        h.define_shape()
    def _disconnect(self):
        while(len(self.all) > 1):
            self.all[-1].disconnect()

    def _reconnect(self):
        self._disconnect()
        self._connect()

e.PRINTTIME = True
m = e.m = Cell(0.2,3)
m.dx = pow(2,-6)
e.dt = pow(2,-7)
m._normalize()

h.load_file("stdrun.hoc")
e.aprec = e.APRecorder(m.prop_site)
e.stim = h.IClamp(m.side(1))
e.stim.delay = 1
e.stim.amp = 200
e.stim.dur  = 5/16
print(e.fullsolve(0.15111,0.001,1e-9))
print(m.main2.L)
#e.SHAPECONFIG = h.define_shape
#print(e.fullsolve(0.15111,0.001,1e-9))
#print(m.main2.L)




