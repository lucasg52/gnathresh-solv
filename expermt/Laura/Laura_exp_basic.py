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
h.dt = pow(2,-7)
diff_list2, diff_list3 = [], []
lengths = [j / 100 for j in range(5, 605, 5)]
# def lengthS():
#     return [j / 100 for j in range(5, 205, 5)]
# lengths = lengthS()
m = Rin_cell_1(0)
m.stim_setup(1)
m.dx = 0.025
n = Rin_cell_1y(1)
n.stim_setup(1)
n.dx = 0.025
w = Rin_cell_3y(2)
w.stim_setup(1)
w.dx = 0.025

gcells = [m,n,w]

def setting_length(dau_len):
    m.stim_b.L = 4*elength(m.stim_b)
    n.stim_b.L = 4*elength(n.stim_b)
    w.stim_b.L = 4* elength(w.stim_b)
    m.side1.L = dau_len*elength(m.side1)
    if dau_len <=0.15:
        n.side1.L = n.dau1.L = n.dau2.L = (dau_len/3.2)*elength(n.side1)
        w.side1.L = w.dau1.L = w.dau2.L = w.dau3.L = (dau_len/3.5)*elength(w.side1)
    elif dau_len==0.2:
        n.side1.L = (dau_len/3.25)*elength(n.side1)
        n.dau1.L =(dau_len/3.25)*elength(n.dau1)
        n.dau2.L = (dau_len/3.25)*elength(n.dau2)
        w.side1.L  = (dau_len/3.25)*elength(w.side1)
        w.dau1.L  =(dau_len/3.25)*elength(w.dau1)
        w.dau2.L  =(dau_len/3.25)*elength(w.dau2)
        w.dau3.L = (dau_len/3.25)*elength(w.dau3)
    elif dau_len>0.2 and dau_len<=2:
        n.side1.L = (dau_len/3.5)*elength(n.side1)
        n.dau1.L =(dau_len/3.5)*elength(n.dau1)
        n.dau2.L = (dau_len/3.5)*elength(n.dau2)
        w.side1.L  = (dau_len/3.5)*elength(w.side1)
        w.dau1.L  =(dau_len/3.45)*elength(w.dau1)
        w.dau2.L  =(dau_len/3.45)*elength(w.dau2)
        w.dau3.L = (dau_len/3.45)*elength(w.dau3)
    elif dau_len>2:
        n.side1.L = dau_len * elength(n.side1)
        n.dau1.L  = dau_len * elength(n.dau1)
        n.dau2.L =dau_len * elength(n.dau2)
        w.side1.L  = dau_len * elength(w.side1)
        w.dau1.L  =dau_len * elength(w.dau1)
        w.dau2.L  =dau_len * elength(w.dau2)
        w.dau3.L  =dau_len * elength(w.dau3)
    all()
    n._normalize()
    m._normalize()
    w._normalize()

def disconnect():
    for m in gcells:
        m.side1.disconnect()


def all():
    for m in gcells:
        m.all = m.soma.wholetree()

    
def run(rin_solver):
    for i in lengths:
        setting_length(i)
        disconnect()
        if rin_solver == 1:
            m.rin_base.append(m.Rin(m.side1(0)))
            n.rin_eqi.append(n.Rin(n.side1(0)))
            w.rin_eqi2.append(m.Rin(w.side1(0)))
            diff_list2.append(m.Rin(m.side1(0))-(n.Rin(n.side1(0))))
            diff_list3.append(m.Rin(m.side1(0))-(w.Rin(w.side1(0))))
        if rin_solver == 0:
            m.rin_base.append(m.alt_Rin(m.side1(0)))
            n.rin_eqi.append(n.alt_Rin(n.side1(0)))
            w.rin_eqi2.append(w.alt_Rin(w.side1(0)))
            diff_list2.append(m.alt_Rin(m.side1(0))-(n.alt_Rin(n.side1(0))))
            diff_list3.append(m.alt_Rin(m.side1(0))-(w.alt_Rin(w.side1(0))))
        print(m.side1.L/118.84, n.side1.L/118.84, "i:", i)

        m.side1.connect(m.main_shaft(0.6))
        n.side1.connect(n.main_shaft(0.6))
        w.side1.connect(w.main_shaft(0.6))
        all()
        h.dt= pow(2,-7)
        m.gna_base.append(m.fullsolve(0.1))
        n.gna_eqi.append(n.fullsolve(0.1))
        w.gna_eqi2.append(w.fullsolve(0.1))
    disconnect()
    # print(f"Control: gna base = {m.fullsolve(0.1)}")

    fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(8,4))
    ax[0,0].plot(lengths,m.rin_base, 'blue', label="Rin for base cell")
    ax[0,0].plot(lengths,n.rin_eqi, 'orange', label="Rin for eqi cell")
    ax[0,0].plot(lengths, w.rin_eqi2, 'green', linestyle = 'dashed', label='Rin for eqi2 cell')
    ax[0,1].plot(lengths,m.gna_base, 'blue',label=f"Gna for base cell; control")
    ax[0,1].plot(lengths,n.gna_eqi, 'orange', label="Gna for eqi cell")
    ax[0,1].plot(lengths,w.gna_eqi2, 'green', linestyle = 'dashed', label="Gna for eqi2 cell")
    ax[1,1].plot(m.rin_base, m.gna_base, 'blue', label="Rin vs Gna for base cell")
    ax[1,1].plot(n.rin_eqi, n.gna_eqi, 'orange', label="Rin vs Gna for equi cell")
    ax[1,1].plot(w.rin_eqi2, w.gna_eqi2, 'green', linestyle = 'dashed', label='Rin vs Gna for equiv cell 2')
    ax[1,0].plot(lengths,diff_list2, 'orange', label="base - equiv")
    ax[1,0].plot(lengths,diff_list3, 'green', linestyle = 'dashed', label="base - equiv2")
    for row in [0,1]:
        for col in [0,1]:
            ax[row,col].grid()
            ax[row,col].legend()
    ax[0,1].set_xlabel("length in lambda")
    ax[0,0].set_ylabel("Rin in mV/nA")
    ax[0,1].set_ylabel("Gna thresh")
    ax[1,0].set_ylabel("Difference from base")
    ax[1,0].set_xlabel("Length in Lambda")
    ax[1,1].set_xlabel("Rin")
    ax[1,1].set_ylabel("Gna")
    plt.show()