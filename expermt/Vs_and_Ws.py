from cells.rincell import Rin_Vcell, RinCell, Rin_Wcell, Rin_W2cell
from tools.Rin_funcs import run, gna_solve
from matplotlib import pyplot as plt
from neuron import h
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

__MAXGBAR__ = 0.3
__tstop__ = h.tstop = 15
h.dt = pow(2,-6)

m = RinCell(0)
v1 = Rin_Vcell(1)
v2 = Rin_Wcell(2)
v3 = Rin_W2cell(3)
len_lst = [i/100 for i in range(0, 110,10)]

tcells = [m, v1, v2, v3]
for cell in tcells:
    cell.setup_stim(0.5)

def set_Tlens(len):
    if len == 0:
        for cell in tcells:
            cell.side1.disconnect()
            cell._normalize()

    else:
        for cell in tcells:
            if cell == m:
                cell.side1.L = len*elength(cell.side1)
            else:
                cell.side1.L = len*elength(cell.side1)
                cell.dau1.L = (len/3)*elength(cell.dau1)
            cell._normalize()

def connect():
    m.side1.connect(m.main_shaft(0.6))
    t1.side1.connect(t1.main_shaft(0.6))
    t2.side1.connect(t2.main_shaft(0.3))
    t3.side1.connect(t3.main_shaft(0.9))

def plot(title):
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,4))
    colors = ['black', 'orange', 'green', 'red']
    for i, cell in enumerate(tcells):
        ax[0].plot(len_lst, cell.rin_lst, colors[i], label=f'Rin for {cell}')
        if cell == m:
            pass
        else:
            ax[1].plot(len_lst, cell.diff_rin, colors[i], label=f'Rin diff for {cell}')
    ax[0].grid()
    ax[1].grid()
    fig.legend(labels=[f'{cell}' for cell in tcells])
    fig.title(title)
    ax[1].set_xlabel('length of side branch in lambda')
    ax[0].set_ylabel('Rin')
    ax[1].set_ylabel('Diff in Rin')
    plt.show()

def rin_solv():
    for cell in tcells:
        cell.rin_lst.append(cell.getRin(cell.main_shaft(0.3)))
        cell.diff_rin.append(m.getRin(cell.main_shaft(0.3))-cell.getRin(cell.main_shaft(0.3)))