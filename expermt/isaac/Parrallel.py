import time
start_everything = time.perf_counter()

from neuron import h
from neuron.units import mV, ms, um
import math
import matplotlib.pyplot as plt

h.nrnmpi_init()
pc = h.ParallelContext()

h.load_file("stdrun.hoc")


class BallAndStick:
    def __init__(self, gid):
        self.gid = gid
        pc.set_gid2node(gid, pc.id())
        # topology
        self.soma = h.Section("soma", self)
        self.dend = h.Section("dend", self)
        self.dend.connect(self.soma)
        # geometry
        self.soma.L = self.soma.diam = 10 * um
        self.dend.L = 100 * um
        self.dend.diam = 2 * um
        # biophysics
        h.hh.insert(self.soma)
        h.pas.insert(self.dend)
        for seg in self.dend:
            seg.pas.e = -65 * mV
        # synapse
        self.syn = h.ExpSyn(self.dend(1))
        self.syn.e = 0 * mV
        self.syn.tau = 2 * ms
        # spike monitoring
        self.spikes = h.Vector()
        self.nc = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.nc.record(self.spikes)
        pc.cell(self.gid, self.nc)

    def position(self, r, theta):
        old_soma_L = self.soma.L
        old_dend_L = self.dend.L
        self.soma.pt3dclear()
        self.soma.pt3dadd(r * math.cos(theta), r * math.sin(theta), 0, self.soma.diam)
        self.soma.pt3dadd(
            (r + old_soma_L) * math.cos(theta),
            (r + old_soma_L) * math.sin(theta),
            0,
            self.soma.diam,
        )
        self.dend.pt3dclear()
        self.dend.pt3dadd(
            (r + old_soma_L) * math.cos(theta),
            (r + old_soma_L) * math.sin(theta),
            0,
            self.dend.diam,
        )
        self.dend.pt3dadd(
            (r + old_soma_L + old_dend_L) * math.cos(theta),
            (r + old_soma_L + old_dend_L) * math.sin(theta),
            0,
            self.dend.diam,
        )

    def __repr__(self):
        return f"BallAndStick[{self.gid}]"


NUM_CELLS = 200
RADIUS = 100 * um

cells = [BallAndStick(i) for i in range(pc.id(), NUM_CELLS, pc.nhost())]

for cell in cells:
    cell.position(RADIUS, 2 * math.pi / NUM_CELLS * cell.gid)

cell = cells[0]

ns = h.NetStim()
ns.number = 1
ns.start = 10 * ms

nc = h.NetCon(ns, cell.syn)
nc.weight[0] = 0.0025
nc.delay = 0

ncs = []


'''
for i in range(NUM_CELLS):
    my_nc = h.NetCon(
        cells[i].soma(0.5)._ref_v, cells[(i + 1) % NUM_CELLS].syn, sec=cells[i].soma
    )
    my_nc.weight[0] = 0.0025
    my_nc.delay = 1 * ms
    ncs.append(my_nc)
'''


# postsyn
for cell in cells:
    my_nc = pc.gid_connect((cell.gid - 1) % NUM_CELLS, cell.syn)
    my_nc.weight[0] = 0.0025
    my_nc.delay = 1 * ms
    ncs.append(my_nc)



start_initialization = time.perf_counter()
pc.set_maxstep(10 * ms)
h.finitialize(-65 * mV)
start_simulation = time.perf_counter()
pc.psolve(2_000 * ms)
end_simulation = time.perf_counter()

my_data = {cell.gid: list(cell.spikes) for cell in cells}
all_data = pc.py_allgather(my_data)

if pc.id() == 0:
    data = {}
    for cell_data in all_data:
        data.update(cell_data)

    print(f"Total time: {end_simulation - start_everything} s")
    print(f"Initialization time: {start_simulation - start_initialization} s")
    print(f"Simulation time: {end_simulation - start_simulation} s")


    plt.figure()
    for gid, spikes in data.items():
        plt.vlines(spikes, gid - 0.4, gid + 0.4)

    plt.xlabel("t (ms)")
    plt.ylabel("Cell ID")

    plt.show()

h.quit()