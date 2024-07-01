from .base import BaseExpCell
from . import adoptedeq as eq
from . import kinetics as kin
from .taperedsection import TaperedSection
from .tools import APRecorder
class ExpCell_3dtaper(BaseExpCell):
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
    def _taperIS(self):
        self.IS.diam = self.main_diam # Confusing. This is done so that the ending diameter of the new IS TaperedSection will be consistent with main axon.
        alpha, gamma, taper = eq.alphagammataper(
            IS_diam =   self.IS_diam,
            s_ratio =   self.s_ratio,
            ell_c =     self.ell_c
            )
        taperpnts = [(taper, self.IS_diam)]
        IS = TaperedSection("IS", self, taperpnts, self.IS)
        self.IS = IS
    def _setup_morph(self):
        super()._setup_morph()
        self._taperIS()
        self.all = self.soma.wholetree()
    def _setup_bioph(self):
        kin.insmod_Traub(self.soma,         "soma")
        kin.insmod_Traub(self.main_shaft,   "axon")
        kin.insmod_Traub(self.IS,           "axon")
        kin.insmod_Traub(self.prop_site,    "axon")
    def __repr__(self):
        return(f"ExpCell3dtaper[{self.gid}]")

class ExpCell_notaper(BaseExpCell):
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
        return("ExpCell_notaper[{}]".format(self.gid) )
    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.IS_diam
        self._normalize()
    def getgnabar(self):
        gna = self.main_shaft.gbar_nafTraub
        for sec in self.all:
            if sec is not self.soma:
                assert(sec.gbar_nafTraub == gna)
        return gna
    def setgnabar(self, gna):
        for sec in self.all:
            if sec is not self.soma:
                sec.gbar_nafTraub = gna
    def setgkbar(self, gk):
        for sec in self.all:
            if sec is not self.soma:
                sec.gbar_kdrTraub = gk
    def _setup_exp(self):
        #set_exstim_site(self.prop_site)
        self.aprecord = APRecorder(self.main_shaft, ran = 1)
    def _setup_bioph(self):
        kin.insmod_Traub(self.soma,         "soma")
        kin.insmod_Traub(self.main_shaft,   "axon")
        kin.insmod_Traub(self.IS,           "axon")
        kin.insmod_Traub(self.prop_site,    "axon")


