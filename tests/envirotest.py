import unittest
import warnings
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
    def _setup_bioph(self):
        for sec in [self.IS, self.main_shaft, self.prop_site, self.side]:
            kin.insmod_Traub(sec, "axon")
        kin.insmod_Traub(self.soma, "soma")
    def _connect(self):
        super()._connect()
        self.side.connect(self.main_shaft(1/8))
    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.IS_diam
        self.side.L = self.prop_site.L * 3
        self.side.diam = self.prop_site.diam

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
        k = e.fullsolve(0.15, 0.1, 1e-6)
        self.assertAlmostEqual(k, 0.15032167434692384, places = 6)

    def test_badestimate(self):
        e = create_test_enviro()
        with warnings.catch_warnings(record=True) as wlog:
            k = e.fullsolve(0.1, 0.005, 1e-6)
            self.assertTrue(wlog)
        self.assertAlmostEqual(k, 0.15032167434692384, places = 6)

