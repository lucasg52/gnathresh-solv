from  neuron import h
import gnatsolv.   adoptedeq as eq
from  gnatsolv. adoptedeq import normalize_dlambda
import gnatsolv.   kinetics_transcribe as kin
from  gnatsolv. taperedsection import TaperedSection
from  math import ulp as __ulp__, sqrt as __sqrt__
#KISS:
#Keep It Simple, Stupid.
__NORMEPSILON__ = __ulp__(5)

__layerdict__ = {
    "layer2":{ # // estimate parameters based on cell reconstructions
        "main_diam" : 0.6,
        "IS_diam" : 1.2,
        "s_ratio" : 14,
        "ell_c" : 0.015
    },
    "layer4":{
        "main_diam" : 0.6,
        "IS_diam" : 1.5,
        "s_ratio" : 11.2,
        "ell_c" : 0.01
    },
    "layer5":{
        "main_diam" : 1.2,
        "IS_diam" : 2,
        "s_ratio" : 11.4,
        "ell_c" : 0.0
    },
    "layer0":{ # "default" layer (prints a warning in O.G code when used
        "main_diam" : 0.6,
        "IS_diam" :   1.6,
        "s_ratio" :   12.5,
        "ell_c" :     0.015
    }
}
def reset3d(m): # doesnt even work
    for sec in m.all:
        if sec.n3d() < 0.5:
            print("3d info does not need to be reset, loop break at section:" + str(sec))
            return
        if sec.pt3dclear() < 0.5:
            print("failed to clear section 3d info because plotshape is open")

def autof3d(cell, ratio = 4, min = 50):
    sec = cell.main_shaft
    f = 0
    children = sec.children()
    if children:
        for sec in children:
            f += max(sec.diam * ratio, min)
            f3d(sec, f = f)
def autof3d0(tree, ratio = 4):
    f = 0
    for sec in tree:
        children = sec.children()
        if children:
            for sec in children:
                f += sec.diam * ratio
                f3d(sec, f = f)

def f3d(sec, f = 0):
    #if h.pt3dclear(sec = sec) > 0.5:
    #    print("ShapePlot must be closed to fuck 3d.")
    #else:
    if sec.n3d() < 1:
        print("how can one fuck 3d if there is no 3d?")
        return
    if f == 0:
        f = sec.L
    h.pt3dstyle(1, 0,f, 0, sec = sec)
def set_exstim_site(sec):
        stim = h.IClamp(sec(0.5))
        stim.delay = 5
        stim.amp =  0.2
        stim.dur =  0.3125

class BaseExpCell:
    def __init__(
            self,
            dx,
            ratio,
            gid = 0,
            layer = 0
            ):
        self.gid = gid
        self.dx = dx # i belive this is the only paramater that really matters (for now)
        self.ratio = ratio

        self.soma = h.Section(          name = "soma"       ,cell = self )
        self.IS = h.Section(            name = "IS"         ,cell = self )
        self.main_shaft = h.Section(    name = "main_shaft" ,cell = self )
        self.prop_site = h.Section(     name = "prop_site"  ,cell = self )

        self.main_length = 8 # // electronic length of main shaft
        for k, v in __layerdict__["layer" + str(layer)].items():
            setattr(self, k, v)

        self.soma_diam = self.s_ratio*self.IS_diam

    def _setup_morph(self):
        self.soma.L = self.soma.diam = self.soma_diam
        self.IS.L = 40 # line 98 
        self.main_shaft.L = self.main_length * eq.elength(self.main_shaft, d = self.main_diam)
        self.main_shaft.diam = self.main_diam
        self.prop_site.diam = self.main_diam/self.ratio
        self.IS.connect(self.soma(1))
        self.main_shaft.connect(self.IS(1)) # (line 107)
        self.prop_site.connect(self.main_shaft(0)) # connections must be made first for self.all to be correct

        self.all = self.soma.wholetree()
        #the following definitions for section diameter are taken from lines 89-105. 

        self._normalize() # technically this is executed at the end
    def _normalize(self): # line 166, not clear why some sections get normalized differently. so I am just assuming it is homogenous. also made my own subroutine 
        for sec in self.all:
            normalize_dlambda(sec, self.dx)




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
        self._setup_bioph()
        self._setup_morph()
    def _taperIS(self):
        self.IS.diam = self.main_diam # Confusing. This is done so that the ending diameter of the new IS TaperedSection will be consistent with main axon.
        IS_diam =   self.IS_diam
        s_ratio =   self.s_ratio
        ell_c =     self.ell_c  
        self.soma_diam = s_ratio*IS_diam
        
        # this entire section below I am considering tossing it in adoptedeq.py
        alpha=                          \
                ((
                    (__sqrt__(s_ratio)-1)
                    /
                    (s_ratio-1)
                )**4)                   \
                /                       \
                (
                    25**4
                    *
                    100 *
                    IS_diam**2
                )

        gamma=                          \
                IS_diam**2              \
                *                       \
                (s_ratio-1)**2          \
                /4

        taper =                         \
                __sqrt__(
                    -gamma/2 +
                    __sqrt__(
                        alpha**2
                        *
                        gamma**2
                        +
                        4 * alpha * ell_c**4
                        )
                    /
                    (2*alpha)
                )
        taperpnts = [(taper, IS_diam)]
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

class APRecorder():
    def __init__ (
            self,
            sec,
            ran = 0.5
            ):
        self.recorded = False
        self.nc = h.NetCon(sec(ran)._ref_v, None, sec = sec)
        self.nc.record(self._record())
    def _record(self):
        print(str(self) + "recorded an AP")
        self.recorded = True
    def proptest(self):
        ret = self.recorded
        self.recorded = False
        return ret
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
        self._setup_bioph()
        self._setup_morph()
        self._setup_exp()
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
    def _setup_exp(self):
        set_exstim_site(self.prop_site)
        self.aprecord = APRecorder(self.main_shaft, ran = 1)
    def _setup_bioph(self):
        kin.insmod_Traub(self.soma,         "soma")
        kin.insmod_Traub(self.main_shaft,   "axon")
        kin.insmod_Traub(self.IS,           "axon")
        kin.insmod_Traub(self.prop_site,    "axon")


        
