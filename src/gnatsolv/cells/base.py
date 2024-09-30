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
    """
    (Legacy) taken from vs-expcell
    Will likely be deprecated in future versions
    """
    stim = h.IClamp(sec(0.5))
    stim.delay = 5
    stim.amp =  0.2
    stim.dur =  0.3125
    return stim

class BaseExpCell(ABC):
    """
    Abstract base class for experimental cells
        The following arguments are all attributes:
        dx          maximum segment length in terms of lambda
        ratio       (legacy) ratio between side branch and parent branch diameters
        gid = 0     gid, required for (useful (but also useless)) hoc/gui interraction
        layer = 0   (legacy) specifies main, IS, and soma diams, as well as ell_c, which is alledgedly the elctrotonic length of the main axon (?)
            see base.layerdict for more details

    Sections:
        All instances of the BaseCell have the following h.Section's:
        
        soma:       The soma should always have nseg = 1
        IS:         The axon initial segment: By default its geometry is not defined. See cells.tapertypes for predefined IS geometries
        main_shaft: The section to which side-branches should attach
        prop_site:  Extends the main_shaft; it is the section upon which an APRecorder or any other recorder should be placed
        
        additional sections should be specified by redefining self._create_secs

    Note: IS geometry must be defined for a useful experimental cell class.
    """
    def __init__(
            self,
            dx,
            ratio,
            gid = 0,
            layer = 0
            ):
        self.gid = gid

        self.dx = dx #We suggest a dx of pow(2,-6); it only affects the normalization of the cell
        self.ratio = ratio #represents ratio between the diameter of the parent branch and the main_shaft
                #it won't do anything after the cell is instantiated

        self.soma = h.Section(          name = "soma"       ,cell = self )
        self.soma.nseg = 1    # prelim. results shows that changing nseg has large effect on gna thresh
        self.IS = h.Section(            name = "IS"         ,cell = self )
        self.main_shaft = h.Section(    name = "main_shaft" ,cell = self )
        self.prop_site = h.Section(     name = "prop_site"  ,cell = self )

        self._create_secs()

        self.main_length = 8    # electrotonic length of main shaft
        self.main_diam = 1.2
        self.IS_diam = 2
        self.s_ratio = 11.4
        self.ell_c = 0.0
        for k, v in layerdict["layer" + str(layer)].items():
            setattr(self, k, v)

        self.soma_diam = self.s_ratio*self.IS_diam
        self._setup_bioph()
        self._setup_morph()

    def _create_secs(self):
        """Optionally, this method can be defined to specify additional sections. Does nothing"""
        pass

    def _setup_morph(self):
        """
        Setup morphology by initializing diameters, then connecting the segments with self._connect, then normalizing dx with self._normalize
        NOTE: Should be executed after self._setup_bioph for correct elength calculations
        Returns: None
        """
        self.soma.L = self.soma.diam = self.soma_diam
        self.IS.L = 40 # line 98
        self.main_shaft.L = self.main_length * eq.elength(self.main_shaft, d = self.main_diam)
        self.main_shaft.diam = self.main_diam
        self.prop_site.diam = self.main_diam/self.ratio
        self._connect()      
        self._normalize()   # this must be executed after bioph
    def _connect(self):
        """
        Connect all the sections
        Returns: None
        """
        self.IS.connect(self.soma(1))
        self.main_shaft.connect(self.IS(1)) # (line 107)
        self.prop_site.connect(self.main_shaft(1))      # finally where it's supposed to be 

    @abstractmethod
    def _setup_bioph(self):
        """abstract method for initializing biophysical properties. Does nothing"""

    def _normalize(self):
        """
        Call eq.normalize_dlambda for all sections, except for soma
        Returns: None
        """
        for sec in self.all[1::]:       # list slicing to avoid changing soma nseg
            normalize_dlambda(sec, self.dx)

    @abstractmethod
    def __repr__(self):
        return ""

    all = property(lambda self : self.soma.wholetree(), None)

    def clearshape(self):
        """
        Calls h.pt3dclear for all sections. Used mainly for debugging
        Returns: None
        """
        for sec in self.all:
            h.pt3dclear(sec = sec)
