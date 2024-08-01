from visual.readsummary import toarr_axis
from visual.graph import matrixplot_smart
from neuron import h
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
h.load_file("stdrun.hoc")

__MAXGBAR__ = 0.2
__tstop__ = h.tstop = 15
h.dt = pow(2,-6)

def creat_len_lst(start, stop, step):
     return [j / 100 for j in range(start, stop, step)]

def new_run(cell, branch, branch2, len_lst, loc_lst, set_len, connect, title, solver='both', csite = None):
    start_all = time.perf_counter()
    OUTFILE = open(title, "a")
    for i, l in enumerate(loc_lst):
        cell.name = f'T{l}'
        if csite == None:
            pass
        else:
            cell.csite = csite[i]
        print(f"{cell.name}:")
        if l == 1:
            branch.disconnect()
        else:
            branch.connect(branch2(l))
        # cell.side1.connect(cell.main_shaft(l))
        for i in len_lst:
            set_len(i)
            print(f"i:{i}")
            if i == 0:
                print("base case")
                if solver == 'gna':
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
                    OUTFILE.write(f"{cell.name}, {i},{gna},/n")
                    cell.gna_lst.append(gna)
                elif solver == 'rin':
                    cell.set_resting(cell.csite)
                    rin = cell.getRin(cell.csite)
                    OUTFILE.write(f"{cell.name}, {i},{rin},/n")
                    cell.rin_lst.append(rin)
                    cell.stim2.amp = 0
                else:
                    cell.set_resting(cell.csite)
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
                    rin = cell.getRin(cell.csite)
                    OUTFILE.write(f"{cell.name}, {i},{gna}, {rin}/n")
                    cell.gna_lst.append(gna)
                    cell.rin_lst.append(rin)
                    cell.stim2.amp = 0
                connect()
            else:
                if solver == 'gna':
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
                    OUTFILE.write(f"{cell.name}, {i},{gna},/n")
                    cell.gna_lst.append(gna)
                elif solver == 'rin':
                    cell.set_resting(cell.csite)
                    rin = cell.getRin(cell.csite)
                    OUTFILE.write(f"{cell.name}, {i},{rin},/n")
                    cell.rin_lst.append(rin)
                    cell.stim2.amp = 0
                else:
                    cell.set_resting(cell.csite)
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
                    rin = cell.getRin(cell.csite)
                    OUTFILE.write(f"{cell.name}, {i},{gna}, {rin}/n")
                    cell.gna_lst.append(gna)
                    cell.rin_lst.append(rin)
                    cell.stim2.amp = 0
    end_all = time.perf_counter()
    print(f"total time: {(end_all - start_all) / 60} mins")


def save_data(len_lst, cell_lst, filename, type='both', name_lst = None):
    df = pd.DataFrame({'lengths': len_lst})
    if name_lst == None:
        if type == 'rin':
            for i, cell in enumerate(cell_lst):
                df.insert(i + 1, f'Rin_{cell}', cell.rin_lst, True)
        elif type == 'gna':
            for i, cell in enumerate(cell_lst):
                df.insert(i + 1, f'Gna_{cell}', cell.gna_lst, True)
        else:
            for i, cell in enumerate(cell_lst):
                df.insert(i+1, f'Rin_{cell}', cell.rin_lst, True)
                df.insert(i+2, f'Gna_{cell}', cell.gna_lst, True)
    else:
        if type == 'rin':
            for i, cell in enumerate(cell_lst):
                df.insert(i + 1, f'Rin_{name_lst[i]}', cell.rin_lst, True)
        elif type == 'gna':
            for i, cell in enumerate(cell_lst):
                df.insert(i + 1, f'Gna_{name_lst[i]}', cell.gna_lst, True)
        else:
            for i, cell in enumerate(cell_lst):
                df.insert(i+1, f'Rin_{name_lst[i]}', cell.rin_lst, True)
                df.insert(i+2, f'Gna_{name_lst[i]}', cell.gna_lst, True)
    return df, df.to_csv(filename)

def plot_2d(cell_lst, file):
    fig, ax = plt.subplots(figsize=(4,2), num=1)
    ax.set_title('Rin vs Gna')
    colors = ['black', 'orange', 'green', 'red', 'blue', 'purple', 'brown', 'pink', 'cyan', 'olive', 'gray']
    # for i, cell in enumerate(cell_lst):
    #     ax[0].plot(x, cell.rin_lst, colors[i])
    #     ax[1].plot(x, cell.gna_lst, colors[i])
    #     ax[2].plot(cell.rin_lst, cell.gna_lst, colors[i])
    # for j in [0,1,2]:
    #    ax[j].grid()
    # fig.legend(labels=[f'{name_lst[i]}' for i,cell  in enumerate(cell_lst)])
    # fig.suptitle(f'Rin and Gna for {title}')
    # ax[1].set_xlabel('length of side branch in lambda')
    # ax[0].set_ylabel('Rin')
    # ax[1].set_ylabel('Gna')
    # ax[2].set_xlabel('Rin')
    # ax[2].set_ylabel('Gna')
    # plt.show()
    Rinmx, axis = toarr_axis(file, 3, 0, 1, wordsep=',')
    Gnamx, axis = toarr_axis(file, 2, 0, 1, wordsep=',')
    for i, cell in enumerate(cell_lst):
        mx = make_parametic(cell, Rinmx, Gnamx, axis)
        ax.plot(*zip(*mx), label=f'{cell}', color = colors[i])
        print(mx)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    fig.legend(labels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
               loc="upper right")
    plt.show()


def make_parametic(celltype, rinmx, gnamx, axis):
    idx = axis[0].index(celltype)
    return [ringna for ringna in zip(rinmx[idx], gnamx[idx])]
def plot_3d(title, dep, ind1, ind2):
    mat, axisvars = toarr_axis(f"../expermt/{title}", dep, ind1, ind2, wordsep = ',')
    matrixplot_smart(mat, axisvars)

def graph(cell_lst, file_lst, label_lst):
    fig, ax = plt.subplot_mosaic([['a)', 'b)'], ['c)', 'c)']],
                       layout='constrained')
    colors = ['black', 'orange', 'green', 'red', 'blue', 'purple', 'brown', 'pink', 'cyan', 'olive', 'gray']
    for i, cell in enumerate(cell_lst):
        cell.mtx = np.load(file_lst[i])
        ax['a)'].plot(cell.mtx[:,0], cell.mtx[:, 2], color= colors[i])
        ax['b)'].plot(cell.mtx[:,0], cell.mtx[:,1], color= colors[i])
        ax['c)'].plot(cell.mtx[:,1], cell.mtx[:,2], color= colors[i])
    fig.legend(labels=label_lst,
               loc="upper right")
    ax['a)'].set_title('Rin based on side branch length')
    ax['a)'].set_xlabel('Length of side branch in lambda')
    ax['a)'].set_ylabel('Rin (megaohms)')
    ax['b)'].set_title('Gna based on side branch length')
    ax['b)'].set_xlabel('Length of side branch in lambda')
    ax['a)'].set_ylabel('Gna')
    ax['c)'].set_title('Rin vs Gna')
    ax['c)'].set_xlabel('Rin (megaohms)')
    ax['c)'].set_ylabel('Gna')
    plt.show()