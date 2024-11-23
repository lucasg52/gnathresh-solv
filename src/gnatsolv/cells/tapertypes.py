import numpy as np
from .base import BaseExpCell
from . import adoptedeq as eq
from . import kinetics as kin
from ..tools.aprecorder import APRecorder
"""
This file specifies two cell types with differing AIS: the 3dtaper (which uses TaperedSec to 
get a precise representation, and a cell with an IS that is just a uniform cylinder
"""

class ExpCell_notaper(BaseExpCell):
    """
    Basic cell with a cylindrical IS with a diameter based on that of legacy code
    """
    __doc__ = BaseExpCell.__doc__ + __doc__
    def __init__(
            self,
            dx,
            ratio,
            gid = 0,
            layer = 0
            ):
        super().__init__(
                 dx,
                 ratio,
                 gid = gid,
                 layer = layer)
        #self.IS_1 = h.Section(name = "IS[1]", cell = self)
    def __repr__(self):
        return(f"ExpCell_notaper[{self.gid}]")
    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.IS_diam # ?
        self._normalize()
    def getgnabar(self):
        """
        get sodium channel density of all sections except for self.soma
        Returns gna (float)
        Throws AssertionError if gbar_nafTraub is not uniform throughout cell
        """
        gna = self.main_shaft.gbar_nafTraub
        for sec in self.all:
            if sec is not self.soma:
                assert(sec.gbar_nafTraub == gna)
        return gna
    def setgnabar(self, gna):
        """set gbar_nafTraub for all sections except for self.soma"""
        for sec in self.all:
            if sec is not self.soma:
                sec.gbar_nafTraub = gna
    def setgkbar(self, gk):
        """set gbar_kdrTraub for all sections except for self.soma"""
        for sec in self.all:
            if sec is not self.soma:
                sec.gbar_kdrTraub = gk
    def _setup_exp(self):
        """creates self.aprecord located on self.main_shaft(1)"""
        #set_exstim_site(self.prop_site)
        self.aprecord = APRecorder(self.main_shaft, ran = 1)
    def _setup_bioph(self):
        """Inserts standard modTraub parameters (see /cells/kinetics.py)"""
        kin.insmod_Traub(self.soma,         "soma")
        kin.insmod_Traub(self.main_shaft,   "axon")
        kin.insmod_Traub(self.IS,           "axon")
        kin.insmod_Traub(self.prop_site,    "axon")


class BaseTaperCell(BaseExpCell):
    def _normalize(self):
        for sec in self.all[1::]:
            eq.normalize_dlambda(sec, self.dx)
        self._taperIS()
    def _taperIS(self):
        n = self.IS.nseg
        taperarr = np.linspace(self.IS_diam, self.main_diam, n+1)
        for seg, diam in zip(self.IS, taperarr):
            seg.diam = diam
