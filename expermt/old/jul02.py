from gnatsolv.cells.base import BaseExpCell, set_exstim_site
from gnatsolv.cells.tools import APRecorder
from gnatsolv.cells import kinetics as kin
from neuron import h
h.load_file("stdrun.hoc")
class BallAndDick(BaseExpCell):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        print(self.dx)

    def _connect(self):
        self.main_shaft.connect(self.soma(1))
        del self.IS
        del self.prop_site
        
    def _setup_morph(self):
        super()._setup_morph()
        self.main_shaft.L *= 2
        self._normalize()

    def _setup_bioph(self):
        kin.insmod_Traub(self.soma,         "soma")
        kin.insmod_Traub(self.main_shaft,   "axon") 
        for sec in [self.IS, self.prop_site]:
            sec.insert("pas")

    def __repr__(self):
        return (f"BAD[{self.gid}]")

m = BallAndDick(0.1,3)
stim = h.IClamp(m.main_shaft(0.1))
stim.delay = 5


