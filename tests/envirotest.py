import unittest
from gnatsolv.cells.base import BaseExpCell
from gnatsolv.enviro.basic import BasicEnviro 
from gnatsolv.tools.aprecorder import APRecorder

import gnatsolv.cells.kinetics as kin
from neuron import h

h.load_file("stdrun.hoc")

class TestCell(BaseExpCell):
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
        # this is a lot of lines
        # might b more easy to maintain if its just a dcell? maybe not?
        super()._setup_morph()
        self.IS.diam = self.IS_diam
        self.side.L = self.prop_site.L * 3
        self.side.diam = self.prop_site.diam
        self.main2.diam = self.main_diam
        self.main2.L = self.main_shaft.L / 8
        self.main_shaft.L -= self.main_shaft.L / 8

def create_test_enviro():
    cell = TestCell(0.1,3)
    cell.dx = pow(2,-6)
    cell._normalize()
    stim = h.IClamp(cell.side(1))
    stim.delay = 1
    stim.amp = 200
    stim.dur  = 5/16
    aprec = APRecorder(cell.prop_site)
    e = BasicEnviro(cell, aprec, stim)
    e.dt = pow(2,-8)
    return e

class EnviroTest(unittest.TestCase):
    def test_basic(self):
        e = create_test_enviro()
        e.fullsolve()

