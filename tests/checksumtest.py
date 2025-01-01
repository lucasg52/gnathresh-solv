import unittest
from gnatsolv.tools import checksum
from gnatsolv.cells.base import BaseExpCell
from gnatsolv.cells.kinetics import insmod_Traub
from neuron import h

def TestSec():
    s = h.Section()
    s.nseg = 9
    s.diam = 1
    return s
class TestCell(BaseExpCell):
    def _setup_bioph(self):
        for sec in [self.main_shaft, self.soma, self.prop_site, self.IS]:
            insmod_Traub(sec, forsec = "axon")

    def _setup_morph(self):
        self.IS.diam = self.main_diam
        super()._setup_morph()

    def __repr__(self):
        return "TestCell"

class CheckSumTest(unittest.TestCase):
    def test_sec_basic(self):
        mysec = TestSec()
        mysec(0.1).diam = 2
        sum1 = checksum.secchecksum(mysec)
        mysec(0.5).diam = 2
        sum2 = checksum.secchecksum(mysec)
        mysec(0.5).diam = 1
        sum3 = checksum.secchecksum(mysec)
        self.assertEqual(sum1, sum3)
        self.assertNotEqual(sum1, sum2)
    def test_cell_basic(self):
        cell = TestCell(dx = pow(2,-3), ratio = 3)
        geom_cs1 = checksum.GeomChecksum(cell)
        cell.main_shaft(0.5).diam *= 2
        geom_cs2 = checksum.GeomChecksum(cell)
        arr = geom_cs1.compare(geom_cs2)
        self.assertEqual(len(arr), 1)
        self.assertEqual(len(arr[0]), 3)
        name, selfh, otherh = arr[0]
        self.assertEqual(name, "TestCell.main_shaft")

