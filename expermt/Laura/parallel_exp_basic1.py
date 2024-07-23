from expermt.Laura.Rin_cells2 import Rin_cell_1, Rin_cell_1y, Rin_cell_3y
from solver.searchclasses import BinSearch, ExpandingSearch
from tools.aprecorder import APRecorder
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from neuron import h
import matplotlib.pyplot as plt
import time

h.load_file("stdrun.hoc")

__MAXGBAR__ = 0.2
__tstop__ = h.tstop = 15
h.dt = pow(2, -7)
diff_list2, diff_list3 = [], []
lengths = [j / 100 for j in range(5, 605, 5)]
m = Rin_cell_1(0)
m.stim_setup(1)
m.dx = 0.025

def setting_length(dau_len):
    m.stim_b.L = 4 * elength(m.stim_b)
    m.side1.L = dau_len * elength(m.side1)
    m._normalize()
def run(rin_solver):
    for i in lengths, cells:
        setting_length(i)
        m.side1.disconnect()
        if rin_solver == 1:
            m.rin_base.append(m.Rin(m.side1(0)))
        if rin_solver == 0:
            m.rin_base.append(m.alt_Rin(m.side1(0)))
        print(m.side1.L / 118.84, "i:", i)

        m.side1.connect(m.main_shaft(0.6))
        m._normalize()
        h.dt = pow(2, -7)
        m.gna_base.append(m.fullsolve(0.1))
    m.side1.disconnect()

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 4))
    ax[0, 0].plot(lengths, m.rin_base, 'blue', label="Rin for base cell")
    ax[0, 1].plot(lengths, m.gna_base, 'blue', label=f"Gna for base cell; control")
    ax[1, 1].plot(m.rin_base, m.gna_base, 'blue', label="Rin vs Gna for base cell")
    for row in [0, 1]:
        for col in [0, 1]:
            ax[row, col].grid()
            ax[row, col].legend()
    ax[0, 1].set_xlabel("length in lambda")
    ax[0, 0].set_ylabel("Rin in mV/nA")
    ax[0, 1].set_ylabel("Gna thresh")
    ax[1, 0].set_ylabel("Difference from base")
    ax[1, 0].set_xlabel("Length in Lambda")
    ax[1, 1].set_xlabel("Rin")
    ax[1, 1].set_ylabel("Gna")
    plt.show()