"""
solve for gna_thresh using a death-environment
"""
import unittest
from neuron import h
from gnatsolv.cells.dcell import DCell
from gnatsolv.enviro.death import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
h.load_file("stdrun.hoc")
def test():
    m = DCell()
    e = DeathEnviro(
            m = m, 
            stim = h.IClamp(m.parent(1)),
            deathrec = DeathRec(
                m.main_shaft, m.main_shaft,
                tstop = 1
                )
            )
    e.stim.delay = 0.5
    e.stim.amp = 0.2
    e.stim.dur = 5/16
    e.TARGDT = pow(2,-6)
    calcthresh = e.fullsolve(0.1745, 0.001, 1e-8) 
    return (abs(calcthresh - 0.1745632667541504) < 5e-9)

