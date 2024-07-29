from cells.rincell import RinCell, Rin_Ycell, Rin_Wcell, Rin_Vcell, Rin_Tcell, Rin_2bbcell
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from neuron import h
import matplotlib.pyplot as plt
import time
import pandas as pd
h.load_file("stdrun.hoc")

__MAXGBAR__ = 0.2
__tstop__ = h.tstop = 15
h.dt = pow(2,-6)

def lengthS(start, stop, step):
     return [j / 100 for j in range(start, stop, step)]

def setting_length(dau_len):
    if dau_len == 0:
        m.side1.disconnect()
        n.side1.disconnect()
        w.side1.disconnect()
        l.side1.disconnect()
        l.dau1.disconnect()
        t.side1.disconnect()
        rl.side1.disconnect()
        rl2.side1.disconnect()
        m2.side1.disconnect()
        for cell in gcells:
            cell._normalize()

    else:
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
        t.side1.L = (dau_len) * elength(t.side1)
        t.dau1.L = (dau_len/3) * elength(t.dau1)
        rl.side1.L = dau_len*elength(rl.side1)
        rl2.side1.L = dau_len*elength(rl2.side1)
        m2.side1.L = (dau_len/2)*elength(m2.side1)
        for cell in gcells:
            cell._normalize()

def gna_solve():
    gna = m.fullsolve(m.est, err=1e-4, acc=1e-6)
    for cell in gcells:
        start_full = time.perf_counter()
        if cell == m:
            m.gna_lst.append(gna)
            m.est = gna
        else:
            print(gna)
            gna2 = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
            cell.gna_lst.append(gna2)
            cell.diff_gna.append(gna-gna2)
            cell.est = gna2
        end_full = time.perf_counter()
        print(f"{cell} fullsolve time = {end_full - start_full}")
def run():
    start_all = time.perf_counter()
    for i in lengths:
        setting_length(i)
        print(m.side1.L / 118.84, n.side1.L / 118.84, "i:", i)
        if i==0:
            print("base case")
            gna_solve()
            for cell in gcells:
                # cell.rin_lst.append(cell.Rin(cell.main_shaft(0.3)))
                # if cell == rl:
                #     cell.gna_lst.append(cell.Rin(cell.main_shaft(0.15)))
                #     cell.diff_rin.append(m.Rin(m.main_shaft(0.3)) - cell.Rin(cell.main_shaft(0.15)))
                # elif cell == rl2:
                #     cell.gna_lst.append(cell.Rin(cell.main_shaft(0.9)))
                #     cell.diff_rin.append(m.Rin(m.main_shaft(0.3)) - cell.Rin(cell.main_shaft(0.9)))
                # else:
                cell.rin_lst.append(cell.getRin(cell.main_shaft(0.3)))
                cell.diff_rin.append(m.getRin(m.main_shaft(0.3)) - cell.getRin(cell.main_shaft(0.3)))
            m.side1.connect(m.main_shaft(0.6))
            n.side1.connect(n.main_shaft(0.6))
            w.side1.connect(w.main_shaft(0.6))
            l.side1.connect(l.main_shaft(0.6))
            l.dau1.connect(l.main_shaft(0.6))
            t.side1.connect(t.main_shaft(0.6))
            rl.side1.connect(rl.main_shaft(0.15))
            rl2.side1.connect(rl2.main_shaft(0.9))
            m2.side1.connect(m2.main_shaft(0.6))
        else:
            gna_solve()
            for cell in gcells:
                    # cell.rin_lst.append(cell.Rin(cell.main_shaft(0.3)))
                    # if cell == rl:
                    #     cell.rin_lst.append(cell.Rin(cell.main_shaft(0.15)))
                    #     cell.diff_rin.append(m.Rin(m.main_shaft(0.3)) - cell.Rin(cell.main_shaft(0.15)))
                    # elif cell == rl2:
                    #     cell.rin_lst.append(cell.Rin(cell.main_shaft(0.9)))
                    #     cell.diff_rin.append(m.Rin(m.main_shaft(0.3)) - cell.Rin(cell.main_shaft(0.9)))
                    # else:
                    cell.rin_lst.append(cell.getRin(cell.main_shaft(0.3)))
                    cell.diff_rin.append(m.getRin(m.main_shaft(0.3)) - cell.getRin(cell.main_shaft(0.3)))

    end_all = time.perf_counter()
    print(f"total time: {(end_all-start_all)/60} mins")

def plot(title):
    fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(8,4))
    ax[0,0].plot(lengths,m.rin_lst, 'black', label="Rin for base cell")
    ax[0,0].plot(lengths,n.rin_lst, 'orange', label="Rin for y cell")
    ax[0,0].plot(lengths, w.rin_lst, 'green', label='Rin for w cell')
    ax[0,0].plot(lengths, l.rin_lst, 'red',  label='Rin for v cell')
    ax[0,0].plot(lengths, t.rin_lst, 'blue', label="Rin for t cell")
    ax[0,0].plot(lengths, rl.rin_lst, 'c', label="Rin for top cell")
    ax[0,0].plot(lengths, rl2.rin_lst, 'm', label="Rin for bottom cell")
    ax[0,0].plot(lengths, m2.rin_lst, 'y', label="Rin for 0.4 cell")

    ax[0,1].plot(lengths,m.gna_lst, 'black',label=f"Gna for base cell; control")
    ax[0,1].plot(lengths,n.gna_lst, 'orange', label="Gna for Y cell")
    ax[0,1].plot(lengths,w.gna_lst, 'green', label="Gna for Tri cell")
    ax[0,1].plot(lengths, l.gna_lst, 'red', label="Gna for V cell")
    ax[0,1].plot(lengths, t.gna_lst, 'blue', label="Gna for T cell")
    ax[0,1].plot(lengths, rl.gna_lst, 'c', label="gna for top cell")
    ax[0,1].plot(lengths, rl2.gna_lst, 'm', label="gna for bottom cell")
    ax[0,1].plot(lengths, m2.gna_lst, 'y', label="gna for 0.4 cell")

    ax[1,1].plot(m.rin_lst, m.gna_lst, 'black', label="Rin vs Gna for base cell")
    ax[1,1].plot(n.rin_lst, n.gna_lst, 'orange', label="Rin vs Gna for Y cell")
    ax[1,1].plot(w.rin_lst, w.gna_lst, 'green', label='Rin vs Gna for Tri cell')
    ax[1, 1].plot(l.rin_lst, l.gna_lst, 'red', label='Rin vs Gna for V cell')
    ax[1, 1].plot(l.rin_lst, t.gna_lst, 'blue', label='Rin vs Gna for T cell')
    ax[1,1].plot(rl.rin_lst, rl.gna_lst, 'c', label="rin vs gna for top cell")
    ax[1,1].plot(rl2.rin_lst, rl2.gna_lst, 'm', label="rin vs gna for bottom cell")
    ax[1,1].plot(m2.rin_lst, m2.gna_lst, 'y', label="rin vs gna for 0.4 cell")

    ax[1,0].plot(lengths,n.diff_rin, 'orange', label="Rin diff Y")
    ax[1,0].plot(lengths,w.diff_rin, 'green', label="Rin diff W")
    ax[1,0].plot(lengths, l.diff_rin, 'red', label='Rin diff V')
    ax[1,0].plot(lengths, t.diff_rin, 'blue', label='Rin diff T')
    ax[1,0].plot(lengths, rl.diff_rin, 'c', label="Rin diff top")
    ax[1,0].plot(lengths, rl2.diff_rin, 'm', label="Rin diff bottom")
    ax[1,0].plot(lengths, m2.diff_rin, 'y', label="Rin diff 0.4")
    # ax[1, 0].plot(lengths, n.diff_gna, 'orange', linestyle='dashed', label="gNa equiv")
    # ax[1, 0].plot(lengths, w.diff_gna, 'green', linestyle='dashed', label="gNa equiv2")
    # ax[1, 0].plot(lengths, l.diff_gna, 'red', linestyle='dashed', label='gNa equiv3')
    # ax[1, 0].plot(lengths, t.diff_gna, 'blue', linestyle='dashed', label='gNa equiv4')
    for row in [0,1]:
        for col in [0,1]:
            ax[row,col].grid()
    fig.legend(labels=['base', 'y', 'w', 'v', 't', 'top', 'bottom', 'alt_diam'],
               loc="upper right")
    fig.title(title)
    ax[0,1].set_xlabel("length in lambda")
    ax[0,0].set_ylabel("Rin in mV/nA")
    ax[0,1].set_ylabel("Gna thresh")
    ax[1,0].set_ylabel("Difference from base")
    ax[1,0].set_xlabel("Length in Lambda")
    ax[1,1].set_xlabel("Rin")
    ax[1,1].set_ylabel("Gna")
    plt.show()

def ult_plot():
    plt.plot(m.rin_lst, m.gna_lst, 'black', label="Rin vs Gna for base cell")
    plt.plot(n.rin_lst, n.gna_lst, 'orange', label="Rin vs Gna for equi cell")
    plt.plot(w.rin_lst, w.gna_lst, 'green', linestyle = 'dashed', label='Rin vs Gna for equiv cell 2')
    plt.plot(l.rin_lst, l.gna_lst, 'red', linestyle = 'dashed', label='Rin vs Gna for equiv cell 3')
    plt.plot(l.rin_lst, t.gna_lst, 'blue', linestyle='dashed', label='Rin vs Gna for equiv cell 4')
    plt.plot(rl.rin_lst, rl.gna_lst, 'c', label="rin vs gna for top cell")
    plt.plot(rl2.rin_lst, rl2.gna_lst, 'm', label="rin vs gna for bottom cell")
    plt.plot(m2.rin_lst, m2.gna_lst, 'y', label="rin vs gna for 0.4 cell")
    plt.xlabel('Rin in megaohms')
    plt.ylabel('Sodium Conductance Threshold mS/cm^2')
    plt.title('Input Resistance versus Sodium Conductance Threshold')
    plt.grid()
    plt.legend()
    plt.show()

def save_data(len_lst, cell_lst, filename):
    df = pd.DataFrame({'lengths': len_lst})
    for i, cell in enumerate(cell_lst):
        df.insert(i+1, f'Rin_{cell}', cell.rin_lst, True)
        df.insert(i+2, f'Gna_{cell}', cell.gna_lst, True)
    return df, df.to_csv(filename)

def save_gna(len_lst, cell_lst, filename):
    df = pd.DataFrame({'lengths': len_lst})
    for i, cell in enumerate(cell_lst):
        df.insert(i+1, f'Gna_{cell}', cell.gna_lst, True)
    return df, df.to_csv(filename)

def save_rin(len_lst, cell_lst, filename):
    df = pd.DataFrame({'lengths': len_lst})
    for i, cell in enumerate(cell_lst):
        df.insert(i+1, f'Rin_{cell}', cell.rin_lst, True)
    return df, df.to_csv(filename)