from  neuron import h
from . import adoptedeq as eq
from .adoptedeq import normalize_dlambda
from abc import ABC, abstractmethod

layerdict = {
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
def set_exstim_site(sec):
    """(Legacy) taken from vs-expcell"""
    stim = h.IClamp(sec(0.5))
    stim.delay = 5
    stim.amp =  200
    stim.dur =  0.3125
    return stim

class BaseExpCell(ABC):
    """Abstract base class for experimental cells
        dx          maximum segment length in terms of lambda
        ratio       (legacy) ratio between side branch and parent branch diams
        gid = 0     gid, required for (useful) hoc/gui interraction
        layer = 0   (legacy) specifies main, IS, and soma diams, as well as ell_c, which is alledgedly the elctrotonic length of the main axon (?)
            see base.layerdict for more details
    """
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
        self.main_diam = 1.2,
        self.IS_diam = 2,
        self.s_ratio = 11.4,
        self.ell_c = 0.0
        for k, v in layerdict["layer" + str(layer)].items():
            setattr(self, k, v)

        self.soma_diam = self.s_ratio*self.IS_diam
        self._setup_bioph()
        self._setup_morph()

    def _setup_morph(self):
        """setup morphology by initializing diameters, then connecting the segments (see _connect), then normalizing dx"""
        self.soma.L = self.soma.diam = self.soma_diam
        self.IS.L = 40 # line 98 
        self.main_shaft.L = self.main_length * eq.elength(self.main_shaft, d = self.main_diam)
        self.main_shaft.diam = self.main_diam
        self.prop_site.diam = self.main_diam/self.ratio
        self._connect()     # connections must be made first for self.all to be correct
        
        self.all = self.soma.wholetree()
        #the following definitions for section diameter are taken from lines 89-105. 
        self._normalize()   # this must be executed after bioph 


    def _connect(self):
        """Connect all the sections
        Returns: None"""
        self.IS.connect(self.soma(1))
        self.main_shaft.connect(self.IS(1)) # (line 107)
        self.prop_site.connect(self.main_shaft(0)) 

    @abstractmethod
    def _setup_bioph(self):
        """abstract method for initializing biophysical properties. Does nothing"""
        pass

    def _normalize(self): # line 166, not clear why some sections get normalized differently. so I am just assuming it is homogenous. also made my own subroutine 
        """calls normalize_dlambda for all sections"""
        for sec in self.all:
            normalize_dlambda(sec, self.dx)

    @abstractmethod
    def __repr__(self):
        return("")

