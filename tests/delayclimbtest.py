"""
testing delay-climbing search mechanism (see gnatsolv.solvers.delayclimb)
"""
import unittest
import numpy as np
from gnatsolv.solver.delayclimb import DelayClimb

class DelClimbTest(unittest.TestCase):
    def test_basicfit(self):
        def fun(x):
            return -0.1337*np.log(2.024-x)+4.2069
        trueparams = np.array([4.2069, -0.1337, 2.024])
        truegna = trueparams[2]
        startpts = [
                [1, fun(1)],
                [1.5, fun(1.5)],
                [2, fun(2)]
                ]
        d = DelayClimb(fun, startpts)
        d.safety_factor = 1/5000
        
        self.assertAlmostEqual(d._fit(fititers = 15), truegna, places = 4)
