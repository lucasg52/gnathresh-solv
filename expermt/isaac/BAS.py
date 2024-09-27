from neuron import h, gui
from neuron.units import mV, ms, um
import math
import matplotlib.pyplot as plt

h.load_file("stdrun.hoc")


class BallAndStick:
    def __init__(self, gid):
        self.gid = gid
        # topology
        self.soma = h.Section("soma", self)
        self.axon = h.Section("axon", self)
        self.axon.connect(self.soma)
        # geometry
        self.soma.L = self.soma.diam = 10 * um
        self.axon.L = 100 * um
        self.axon.diam = 2 * um
        # biophysics
        h.hh.insert(self.soma)
        h.pas.insert(self.axon)
        for seg in self.axon:
            seg.pas.e = -65 * mV
        # synapse
        self.syn = h.ExpSyn(self.axon(1))
        self.syn.e = 0 * mV
        self.syn.tau = 2 * ms
        # spike monitoring
        self.spikes = h.Vector()
        self.nc = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.nc.record(self.spikes)

    def position(self, r, theta):
        old_soma_L = self.soma.L
        old_dend_L = self.axon.L
        self.soma.pt3dclear()
        self.soma.pt3dadd(r * math.cos(theta), r * math.sin(theta), 0, self.soma.diam)
        self.soma.pt3dadd(
            (r + old_soma_L) * math.cos(theta),
            (r + old_soma_L) * math.sin(theta),
            0,
            self.soma.diam,
        )
        self.axon.pt3dclear()
        self.axon.pt3dadd(
            (r + old_soma_L) * math.cos(theta),
            (r + old_soma_L) * math.sin(theta),
            0,
            self.axon.diam,
        )
        self.axon.pt3dadd(
            (r + old_soma_L + old_dend_L) * math.cos(theta),
            (r + old_soma_L + old_dend_L) * math.sin(theta),
            0,
            self.axon.diam,
        )

    def __repr__(self):
        return f"BallAndStick[{self.gid}]"


NUM_CELLS = 100
RADIUS = 100 * um

cells = [BallAndStick(i) for i in range(NUM_CELLS)]

for i, cell in enumerate(cells):
    cell.position(RADIUS, 2 * math.pi / NUM_CELLS * i)

# display the ring
ps = h.PlotShape()
ps.show(0)


cell = cells[0]

ns = h.NetStim()
ns.number = 1
ns.start = 10 * ms

nc = h.NetCon(ns, cell.syn)
nc.weight[0] = 0.0025
nc.delay = 0

ncs = []
for i in range(NUM_CELLS):
    my_nc = h.NetCon(
        cells[i].soma(0.5)._ref_v, cells[(i + 1) % NUM_CELLS].syn, sec=cells[i].soma
    )
    my_nc.weight[0] = 0.0025
    my_nc.delay = 1 * ms
    ncs.append(my_nc)


t = h.Vector().record(h._ref_t)

all_v = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in cells]

h.finitialize(-65 * mV)
h.continuerun(1_000 * ms)

for i, v in enumerate(all_v):
    plt.plot(t, v, label=f"cell{i}")

plt.legend()

plt.figure()
for cell in cells:
    plt.vlines(list(cell.spikes), cell.gid - 0.4, cell.gid + 0.4)

plt.xlabel("t (ms)")
plt.ylabel("Cell ID")

plt.show()
