from Rin_cells2 import Rin_cell_1, Rin_cell_1y, Rin_cell_3y
from neuron import h
from matplotlib import pyplot as plt
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

__MAXGBAR__ = 0.2
__tstop__ = h.tstop = 15
h.dt = pow(2, -7)
m = Rin_cell_1(0)
m.stim_setup(1)
m.dx = 0.025
n = Rin_cell_1y(1)
n.stim_setup(1)
n.dx = 0.025
w = Rin_cell_3y(2)
w.stim_setup(1)
w.dx = 0.025
lengths = [j/100 for j in range(5, 25, 5)]
diff_list2 = []
diff_list3 = []

def setting_length(dau_len):
    m.stim_b.L = 4*elength(m.stim_b)
    n.stim_b.L = 4*elength(n.stim_b)
    w.stim_b.L = 4* elength(w.stim_b)
    m.side1.L = dau_len*elength(m.side1)
    if dau_len == 0.05 or dau_len == 0.1:
        n.side1.L = n.dau1.L = n.dau2.L = (dau_len/2)*elength(n.side1)
        w.side1.L = w.dau1.L = w.dau2.L = w.dau3.L = (dau_len/2)*elength(w.side1)
    elif dau_len>0.1 and dau_len<2.07:
        n.side1.L = n.dau1.L = n.dau2.L = (dau_len)*elength(n.side1)
        w.side1.L = w.dau1.L = w.dau2.L = w.dau3.L = (dau_len)*elength(w.side1)
    elif dau_len>2.05:
        n.side1.L = n.dau1.L = n.dau2.L =dau_len * elength(n.side1)
        w.side1.L = w.dau1.L = w.dau2.L = w.dau3.L = dau_len * elength(w.side1)
    all()
    n._normalize()
    m._normalize()
    w._normalize()

def disconnect():
    m.side1.disconnect()
    n.side1.disconnect()
    w.side1.disconnect()

def all():
    m.all = m.soma.wholetree()
    n.all = n.soma.wholetree()
    w.all = w.soma.wholetree()

def plot():
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 4))
    ax[0, 0].plot(lengths, m.rin_base, 'blue', label="Rin for base cell")
    ax[0, 0].plot(lengths, n.rin_eqi, 'orange', label="Rin for eqi cell")
    ax[0, 0].plot(lengths, w.rin_eqi2, 'green', linestyle='dashed', label='Rin for eqi2 cell')
    ax[0, 1].plot(lengths, m.gna_base, 'blue', label=f"Gna for base cell; control")
    ax[0, 1].plot(lengths, n.gna_eqi, 'orange', label="Gna for eqi cell")
    ax[0, 1].plot(lengths, w.gna_eqi2, 'green', linestyle='dashed', label="Gna for eqi2 cell")
    ax[1, 1].plot(m.rin_base, m.gna_base, 'blue', label="Rin vs Gna for base cell")
    ax[1, 1].plot(n.rin_eqi, n.gna_eqi, 'orange', label="Rin vs Gna for equi cell")
    ax[1, 1].plot(w.rin_eqi2, w.gna_eqi2, 'green', linestyle='dashed', label='Rin vs Gna for equiv cell 2')
    ax[1, 0].plot(lengths, diff_list2, 'orange', label="base - equiv")
    ax[1, 0].plot(lengths, diff_list3, 'green', linestyle='dashed', label="base - equiv2")
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

def base_exp(rin_solver):
    for i in lengths:
        m.stim_b.L = 4 * elength(m.stim_b)
        m.side1.L = i * elength(m.side1)
        print(m.side1.L/118.84)
        m.all = m.soma.wholetree()
        m._normalize()
        disconnect()
        if rin_solver==1:
            m.rin_base.append(m.Rin(m.side1(0)))
        if rin_solver == 0:
            m.rin_base.append(m.alt_Rin(m.side1(0)))
        m.side1.connect(m.main_shaft(0.6))
        h.dt = pow(2,-7)
        m.gna_base.append(m.fullsolve(0.1))
        m.side1.disconnect()
    print("ran base cell experiment")

def eqi_exp(rin_solver):
    for i in lengths:
        n.stim_b.L = 4 * elength(n.stim_b)
        n.side1.L = i * elength(n.side1)
        if i == 0.05 or i == 0.1:
            n.side1.L = (i / 2) * elength(n.side1)
            n.dau1.L =(i / 2) * elength(n.dau1)
            n.dau2.L =(i / 2) * elength(n.dau2)
        elif i > 0.1 and i < 2.07:
            n.side1.L = (i-0.08) * elength(n.side1)
            n.dau1.L = (i-0.08) * elength(n.dau1)
            n.dau2.L = (i-0.08) * elength(n.dau2)
        elif i>2.05:
            n.side1.L = i * elength(n.side1)
            n.dau1.L = i * elength(n.dau1)
            n.dau2.L = i * elength(n.dau2)
        print(n.side1.L/118.84, n.dau1.L/118.84, n.dau2.L/118.84)
        n.all = n.soma.wholetree()
        n._normalize()
        disconnect()
        if rin_solver==1:
            n.rin_eqi.append(n.Rin(n.side1(0)))
        if rin_solver == 0:
            n.rin_eqi.append(n.alt_Rin(n.side1(0)))
        n.side1.connect(n.main_shaft(0.6))
        h.dt = pow(2,-7)
        n.gna_eqi.append(n.fullsolve(0.1))
        n.side1.disconnect()
    print("ran equiv cell experiment")

def eqi2_exp(rin_solver):
    for i in lengths:
        w.stim_b.L = 4 * elength(w.stim_b)
        w.side1.L = i * elength(w.side1)
        if i == 0.05 or i == 0.1:
            w.side1.L = (i / 2) * elength(w.side1)
            w.dau1.L = (i / 2) * elength(w.dau1)
            w.dau2.L = (i / 2) * elength(w.dau2)
            w.dau3.L = (i / 2) * elength(w.dau3)
        elif i > 0.1 and i < 2.07:
            w.side1.L = (i-0.05) * elength(w.side1)
            w.dau1.L = (i-0.05) * elength(w.dau1)
            w.dau2.L = (i-0.05) * elength(w.dau2)
            w.dau3.L=(i-0.05) * elength(w.dau3)
        elif i>2.05:
            w.side1.L = i * elength(w.side1)
            w.dau1.L = i * elength(w.dau1)
            w.dau2.L = i * elength(w.dau2)
            w.dau3.L = i * elength(w.dau3)
        print(w.side1.L/118.84, w.dau1.L/118.84, w.dau2.L/118.84, w.dau3.L/118.84)
        w.all = w.soma.wholetree()
        w._normalize()
        disconnect()
        if rin_solver==1:
            w.rin_eqi2.append(w.Rin(w.side1(0)))
        if rin_solver == 0:
            w.rin_eqi2.append(w.alt_Rin(w.side1(0)))
        w.side1.connect(w.main_shaft(0.6))
        h.dt = pow(2,-7)
        w.gna_eqi2.append(w.fullsolve(0.1))
        w.side1.disconnect()
    print("ran equiv cell 2 experiment")

def run(rin_solver, cell):
    if cell == 0:
        base_exp(rin_solver)
    elif cell==1:
        eqi_exp(rin_solver)
    elif cell==2:
        eqi2_exp(rin_solver)
    m.side1.disconnect()
    print(f"Control: gna base = {m.fullsolve(0.1)}")