from ..cells.base import BaseExpCell
from neuron import h
from ..cells import kinetics as kin
import time
h.load_file("stdrun.hoc")
class StressCell(BaseExpCell):
    def __init__(self, *args, gid = 0, **kwargs):
        self.gid = 0
        self.side = h.Section(name = "side", cell = self)
        super().__init__(*args, **kwargs)

    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.IS_diam
        self.prop_site.L *= 3
        self.side.L = self.prop_site.L
        self.side.diam = self.prop_site.diam

    def _setup_bioph(self):
        for sec in [
                getattr(self,name)
                for name in [ 'IS', 'main_shaft', 'prop_site', 'side']
                ]:
            kin.insmod_Traub(sec, "axon")
            sec.gbar_nafTraub = 0.4
            sec.gbar_kdrTraub = 0.4

        kin.insmod_Traub(self.soma, "soma")
            

    def _connect(self):
        super()._connect()
        self.prop_site.connect(self.main_shaft(0.3))
        self.side.connect(self.main_shaft(0.6))

    def __repr__(self):
        return f"StressCell[{self.gid}]"


m = StressCell(pow(2,-7),3)

stims = [h.IClamp(seg) for seg in m.prop_site]
for i, s in enumerate(stims):
    s.delay = 5 + (5 * i)
    h.tstop = s.delay + 10
    s.amp = 200
    s.dur = 0.25
tstart = time.process_time()
h.dt = pow(2,-6)
h.finitialize(-69)
h.continuerun(h.tstop)
print(time.process_time() - tstart)


