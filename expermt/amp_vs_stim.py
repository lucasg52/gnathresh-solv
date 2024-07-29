import numpy as np
from neuron import h
from cells.base import BaseExpCell
from cells import kinetics as kin
from matplotlib import pyplot as plt
from visual import movie
h.load_file("stdrun.hoc")

h.dt = 0.125

class ex_cell(BaseExpCell):
    def __init__(self, gid):
        self.gid = gid
        self.dx = pow(2,-6)
        super().__init__(self.dx, 3, gid)

    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.main_diam

    def _connect(self):
        super()._connect()
        self.prop_site.disconnect()

    def _setup_bioph(self):
        for sec in [self.main_shaft, self.IS]:
            kin.insmod_Traub(sec, "axon")
        kin.insmod_Traub(self.soma, "soma")

    def setGna(self, gna):
        for sec in [self.main_shaft, self.IS]:
            sec.gbar_nafTraub = gna
            sec.gbar_kdrTraub = gna
    def __repr__(self):
        return f"ex_cell({self.gid})"

m = ex_cell(0)
m.setGna(0.15)
stim = h.IClamp(m.main_shaft(0.5))
stim.delay = 5
stim.dur = 1e99
stim.amp = 0.1

x_lst =[]

der = []
xs = np.linspace(0,0.1, 50)
gna = np.linspace(0,0.15,16)
# movie.setup(start=m.soma(0), end=m.main_shaft(1))


def getRin(sec):
    imp_geter = h.Impedance()
    imp_geter.loc(sec)
    imp_geter.compute(0)
    return imp_geter.input(sec)

def get_data(title):
    y_lst = []
    for g in gna:
        m.setGna(g)
        stim.amp = 0
        h.finitialize(-69)
        h.continuerun(30)
        v_rest = m.main_shaft(0.5).v
        for x in xs:
            stim.amp = x
            h.finitialize(-69)
            h.continuerun(30)
            x_lst.append(x)
            y_lst.append((m.main_shaft(0.5).v - v_rest) / x) #getRin(m.main_shaft(0.5)))
    # for x in range(len(xs)):
    #     stim.amp=0
    #     y_lst.append(getRin(m.main_shaft(0.5)))
        plt.plot(xs,y_lst, marker = 'x', markersize=5,
                    markeredgecolor="tab:red", label=f"gna = {g}")
        y_lst = []
    plt.xlabel('amp')
    plt.ylabel('Rin')
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()


