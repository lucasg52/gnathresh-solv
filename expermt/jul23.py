from neuron import h
from ..cells.base import BaseExpCell as Base
from ..cells import kinetics as kin
from ..tools import environment as e
from matplotlib import pyplot as plt
class Cell(Base):
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
        self.prop_site.connect(self.main_shaft(1))
        self.side.connect(self.main_shaft(0.3))
    def _setup_morph(self):
        super()._setup_morph()
        self.side.L = self.prop_site.L * 3
        self.side.diam = self.prop_site.diam

e.m = Cell(0.2,3)
e.dx = pow(2,-6)

