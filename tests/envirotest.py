import unittest
import warnings
from gnatsolv.cells.base import BaseExpCell
from gnatsolv.enviro.basic import BasicEnviro 
from gnatsolv.enviro.death import DeathEnviro 
from gnatsolv.tools.aprecorder import APRecorder
from gnatsolv.tools.apdeath import DeathRec

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
        self._normalize()

def create_test_enviro_basic():
    cell = TestCell(pow(2,-5),3)
    stim = h.IClamp(cell.side(1))
    stim.delay = 1
    stim.amp = 200
    stim.dur  = 5/16
    aprec = APRecorder(cell.prop_site)
    e = BasicEnviro(cell, aprec, stim)
    e.dt = pow(2,-6)
    return e

def create_test_enviro_death():
    e_old = create_test_enviro_basic()
    e = DeathEnviro(
            e_old.cell,
            DeathRec(*([e_old.cell.main_shaft]*2), tstart = e_old.stim.delay),
            e_old.stim)
    return e

class EnviroTest(unittest.TestCase):
    def test_basic(self):
        e = create_test_enviro_basic()
        k = e.fullsolve(0.15, 0.0125, 1e-6)
        self.assertAlmostEqual(k, 0.1518798828125, places = 5)

    def test_badestimate(self):
        e = create_test_enviro_basic()
        with warnings.catch_warnings(record=True) as wlog:
            k = e.fullsolve(0.1, 0.005, 1e-5)
            self.assertTrue(wlog)
            self.assertTrue("radius" in str(wlog[0]))
        self.assertAlmostEqual(k, 0.1518798828125, places = 5)
        e.SEARCH_RAD_WARN = 100
        with warnings.catch_warnings(record=True) as wlog:
            k = e.fullsolve(0.1, 0.005, 1e-3)
    def test_infeasable(self):
        e = create_test_enviro_basic()
        with warnings.catch_warnings(record=True) as wlog:
            e.fullsolve(0.05, 5e-9, 1e-15, maxsteps = 3)
            self.assertTrue(wlog)
            self.assertTrue("feasable" in str(wlog[0]))
    def test_abysmal(self):
        e = create_test_enviro_basic()
        with warnings.catch_warnings(record=True) as wlog:
            e.fullsolve(0.1, 5e-9, 1e-15, maxsteps = 3)
            self.assertTrue(wlog)
            self.assertTrue("steps" in str(wlog[0]))

class DeathEnviroTest(unittest.TestCase):
    def test_nostim(self):
        e = create_test_enviro_death() 
        e.stim.amp = 0
        with warnings.catch_warnings(record=True) as wlog:
            e.fullsolve(0.15, 0.0125, 1e-6)
            self.assertTrue(wlog)
            self.assertTrue("detect" in str(wlog[0]))
    # not present: test for warning about an AP that doesnt die
