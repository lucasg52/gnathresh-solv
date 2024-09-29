from neuron import h
from gnatsolv.cells.base import BaseExpCell as Base
from gnatsolv.cells import kinetics as kin
from gnatsolv.tools import environment as e
from matplotlib import pyplot as plt
import numpy as np
import time
from gnatsolv.visual import movie

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
        #h.define_shape()
    def _disconnect(self):
        while(len(self.all) > 1):
            self.all[-1].disconnect()

    def _reconnect(self):
        self._disconnect()
        self._connect()
def printproctime():
    print(time.process_time())

#prerunold = e.prerun
#def prerun(gna):
    #printproctime()
    #prerunold(gna)
#e.prerun = prerun
e.PRINTTIME = True
m = e.m = Cell(0.2,3)
m.dx = pow(2,-6)
e.dt = pow(2,-8)
m._normalize()
h.load_file("stdrun.hoc")
e.aprec = e.APRecorder(m.prop_site)
e.stim = h.IClamp(m.side(1))
e.stim.delay = 1
e.stim.amp = 200
e.stim.dur  = 5/16

results  = []
xarr = list(range(-8,-6))
res = 0.15075
err = pow(2,-10)

GNA = None

def prerun():
    e.prerun(GNA)


movie.prerun = prerun

print(h.topology)
#for x in xarr:
#    m.dx = pow(2,x)
#    m._normalize()
#    resnew = e.fullsolve(res,err, pow(2,-23))
#    if abs(res - resnew) > err:
#        print(res-resnew)
#        err += 1.5* abs(res-resnew)
#    results.append(resnew)
#    res = resnew

