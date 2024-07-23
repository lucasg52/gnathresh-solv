from cells.Rin_cells2 import Rin_cell_1, Rin_cell_1y, Rin_cell_3y
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
h.dt = pow(2,-7) + pow(2,-7)
diff_list2, diff_list3, diff_lst4 = [], [], []
def lengthS(start, stop, step):
     return [j / 100 for j in range(start, stop, step)]
lengths = lengthS(0, 610, 10)
m = Rin_cell_1(0)
m.stim_setup(1)
m.stim_b.L = 4 * elength(m.stim_b)
n = Rin_cell_1y(1)
n.stim_b.L = 4 * elength(n.stim_b)
n.stim_setup(1)
w = Rin_cell_3y(2)
w.stim_b.L = 4 * elength(w.stim_b)
w.stim_setup(1)
l = Rin_cell_1y(1)
l.stim_b.L = 4 * elength(l.stim_b)
l.stim_setup(1)

gcells = [m,n,w, l]

def setting_length(dau_len):
    # if dau_len == 0:
    #     m.side1.disconnect()
    #     n.side1.disconnect()
    #     l.side1.disconnect()
    #     l.dau1.disconnect()
    #     w.side1.disconnect()
    # else:
    m.side1.L = dau_len*elength(m.side1)
    n.side1.L = (dau_len/2)*elength(n.side1)
    n.dau1.L = (dau_len / 2) * elength(n.dau1)
    n.dau2.L = (dau_len / 2) * elength(n.dau2)
    w.side1.L = (dau_len / 2) * elength(w.side1)
    w.dau1.L = (dau_len / 2) * elength(w.dau1)
    w.dau2.L = (dau_len / 2) * elength(w.dau2)
    w.dau3.L = (dau_len/2)*elength(w.dau3)
    l.side1.L = (dau_len) * elength(l.side1)
    l.dau1.L = (dau_len) * elength(l.dau1)
    all()
    n._normalize()
    m._normalize()
    w._normalize()
    l._normalize()

def disconnect():
    for m in gcells:
        m.main_shaft.disconnect()
def all():
    for m in gcells:
        m.all = m.soma.wholetree()

def run(rin_solver):
    start_all = time.perf_counter()
    for i in lengths:
        setting_length(i)
        # if i==0:
        #     print("base case")
        #     m.side1.connect(m.main_shaft(0.6))
        #     n.side1.connect(n.main_shaft(0.6))
        #     l.side1.connect(l.main_shaft(0.6))
        #     l.dau1.connect(l.main_shaft(0.6))
        #     w.side1.connect(w.main_shaft(0.6))
        disconnect()
        if rin_solver == 1:
            for cell in gcells:
                    cell.rin_lst.append(cell.Rin(cell.main_shaft(0.3)))
            diff_list2.append(m.Rin(m.main_shaft(0.3))-(n.Rin(n.main_shaft(0.3))))
            diff_list3.append(m.Rin(m.main_shaft(0.3))-(w.Rin(w.main_shaft(0.3))))
            diff_lst4.append(m.Rin(m.main_shaft(0.3))-(l.Rin(l.main_shaft(0.3))))
        if rin_solver == 0:
            for cell in gcells:
                cell.rin_lst.append(cell.alt_Rin(cell.main_shaft(0.3)))
            diff_list2.append(m.alt_Rin(m.main_shaft(0.3))-n.alt_Rin(n.main_shaft(0.3)))
            diff_list3.append(m.alt_Rin(m.main_shaft(0.3))-w.alt_Rin(w.main_shaft(0.3)))
            diff_lst4.append(m.alt_Rin(m.main_shaft(0.3)) - (l.alt_Rin(l.main_shaft(0.3))*2))

        print(m.side1.L/118.84, n.side1.L/118.84, "i:", i)

        for cell in gcells:
            cell.main_shaft.connect(cell.IS(1))
        all()
        h.dt= pow(2,-6)
        # for cell in gcells:
        #     start_full = time.perf_counter()
        #     cell.gna_lst.append(cell.fullsolve(0.1490, err= 1e-4, acc=1e-6))
        #     end_full = time.perf_counter()
        #     print(f"fullsolve time = {end_full-start_full}")
    disconnect()
    end_all = time.perf_counter()
    # print(f"Control: gna base = {m.fullsolve(0.1490, err=1e-4, acc=1e-6)}")
    print(f"total time: {(end_all-start_all)/3600} hours")

def plot():
    fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(8,4))
    ax[0,0].plot(lengths,m.rin_lst, 'blue', label="Rin for base cell")
    ax[0,0].plot(lengths,n.rin_lst, 'orange', label="Rin for eqi cell")
    ax[0,0].plot(lengths, w.rin_lst, 'green', linestyle = 'dashed', label='Rin for eqi2 cell')
    ax[0,0].plot(lengths, l.rin_lst, 'red', label='Rin for eqi3 cell')
    ax[0,1].plot(lengths,m.gna_lst, 'blue',label=f"Gna for base cell; control")
    ax[0,1].plot(lengths,n.gna_lst, 'orange', label="Gna for eqi cell")
    ax[0,1].plot(lengths,w.gna_lst, 'green', linestyle = 'dashed', label="Gna for eqi2 cell")
    ax[0, 1].plot(lengths, l.gna_lst, 'red', label="Gna for eqi3 cell")
    ax[1,1].plot(m.rin_lst, m.gna_lst, 'blue', label="Rin vs Gna for base cell")
    ax[1,1].plot(n.rin_lst, n.gna_lst, 'orange', label="Rin vs Gna for equi cell")
    ax[1,1].plot(w.rin_lst, w.gna_lst, 'green', linestyle = 'dashed', label='Rin vs Gna for equiv cell 2')
    ax[1, 1].plot(l.rin_lst, l.gna_lst, 'red', label='Rin vs Gna for equiv cell 3')
    ax[1,0].plot(lengths,diff_list2, 'orange', label="base - equiv")
    ax[1,0].plot(lengths,diff_list3, 'green', linestyle = 'dashed', label="base - equiv2")
    ax[1,0].plot(lengths, diff_lst4, 'red', label='base - equiv3')
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