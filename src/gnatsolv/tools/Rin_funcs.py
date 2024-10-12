from neuron import h
# graphing functions should not be in tools dir.
import matplotlib.pyplot as plt
import time
import numpy as np
from ..eq import elength
from .environment import DeathEnviro
from .apdeath import DeathRec
h.load_file("stdrun.hoc")

# there is absolutely no reason you would set h.dt outside of an experiment file/ environment class
h.dt = pow(2,-6)

# Unclear what this function is used for. Probably belongs in the experiment file or enviro-
# class, not here.
def creat_len_lst(start, stop, step):
     return [j / 100 for j in range(start, stop, step)]

# Unclear what class "cell" is supposed to be, since it clearly has non-standard attributes
# (cell.csite, cell.set_matx). Please include some documentation on how this function would be
# used in a more general setting. If not applicable, this function should also be defined in the
# experiment file or enviro-class.
def gna_run(cell, branch, branch2, loc_lst, len_lst, file_lst):
    # cell.est = 0.14
    cell.stim.delay = 0.5
    start_all = time.perf_counter()
    deathrec = DeathRec(cell.main_shaft, cell.prop_site, 1)
    e = DeathEnviro(cell, deathrec, cell.stim)
    e.PRINTTIME = True
    cell.set_matx(len(len_lst),2)
    branch.disconnect()
    base_gna = e.fullsolve(cell.est, 1e-6, 1e-12)
    for i, loc in enumerate(loc_lst):
        start = time.perf_counter()
        cell.csite = loc
        branch.connect(branch2(loc))
        for j, lens in enumerate(len_lst):
            # why are we doing element-wise multiplication?
            cell.gna_mtx[j,0] *= lens
            if lens ==0:
                # why are we doing element-wise multiplication?
                cell.gna_mtx[j,1] *= base_gna
                cell.est = base_gna
            else:
                branch.L = lens*elength(branch)
                cell._normalize()
                gna = e.fullsolve(cell.est, 1e-6, 1e-12)
                # why are we doing element-wise multiplication?
                cell.gna_mtx[j,1]*=gna
                cell.est = gna
                print(gna)
        # general-use functions should not save files. Instead, they should return data that can be
        # manipulated for other uses.
        np.save(file_lst[i], cell.gna_mtx)
        cell.set_matx(len(len_lst),2)
        end = time.perf_counter()
        print(f"cell time: {(end-start)/60} mins")
    end_all = time.perf_counter()
    print(f"total time: {(end_all - start_all) / 60} mins")

# same deal as previous function.
def rin_run(cell, branch, branch2, loc_lst, len_lst, file_lst):
    start_all = time.perf_counter()
    # cell.set_matx(len(len_lst),2)
    cell.stim.amp = 0
    cell.setgna(0)
    h.dt = 0.25
    for i, loc in enumerate(loc_lst):
        mtx = np.load(file_lst[i])
        print(f'cell: {loc}')
        start = time.perf_counter()
        cell.csite = loc
        branch.connect(branch2(loc))
        for j, lens in enumerate(len_lst):
            print(f'length: {lens}')
            # mtx[j,0] *= lens
            if lens ==0:
                branch.disconnect()
                mtx[j,1] = cell.getRin(0.2)
                branch.connect(branch2(loc))
            else:
                branch.L = lens*elength(branch)
                cell._normalize()
                rin = cell.getRin(0.2)
                mtx[j, 1] = rin
                print(rin)
        # general-use functions should not save files. Instead, they should return data that can be
        # manipulated for other uses.
        np.save(file_lst[i], mtx)
        # cell.set_matx(len(len_lst),2)
        end = time.perf_counter()
        print(f"cell time: {(end - start)} secs")
    end_all = time.perf_counter()
    print(f"total time: {(end_all - start_all)/60} mins")

# graphing functions should only be in the visual dir (though I still have to figure out where that
# directory will go), or in the experiment file.
def graph(cell_lst, rin_lst, gna_lst, label_lst, title, leg_title):
    fig, ax = plt.subplot_mosaic([['a)', 'b)'], ['c)', 'c)']],
                       layout='constrained')
    colors = ['black','pink', 'purple', 'blue', 'cyan', 'green', 'orange', 'red', 'brown', 'olive', 'grey']
    for i, cell in enumerate(cell_lst):
        cell.rin_mtx = np.load(rin_lst[i])
        cell.gna_mtx = np.load(gna_lst[i])
        ax['a)'].plot(cell.rin_mtx[:,0], cell.rin_mtx[:, 1], color= colors[i])
        # ax['b)'].plot(cell.gna_mtx[:,0], cell.gna_mtx[:,1], color= colors[i])
        # ax['c)'].plot(cell.rin_mtx[:,1], cell.gna_mtx[:,1], color= colors[i])
    ax['c)'].legend(labels=label_lst, fontsize = 'large', title = leg_title, loc="lower left", ncols=2)
    fig.suptitle(title)
    ax['a)'].set_title(r"$\text{R}_{\text{in}}$ (M$\Omega$) base on length")
    ax['a)'].set_xlabel("log$_{10}$(side branch length in $\\lambda$)")
    ax['a)'].set_ylabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
    ax['a)'].grid()
    # ax['b)'].set_title(r"$\text{g}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$ based on length")
    # ax['b)'].set_xlabel("log$_{10}$(side branch length in $\\lambda$)")
    # ax['b)'].set_ylabel(r"$\text{g}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$")
    # ax['b)'].grid()
    # ax['c)'].set_title(r"$\text{R}_{\text{in}}$ vs $\text{g}_{\text{Na}}$")
    # ax['c)'].set_xlabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
    # ax['c)'].set_ylabel(r"$\text{g}_{Na} (\frac{\text{mho}}{\text{cm}^2})$")
    # ax['c)'].grid()

    plt.show()

# this function appears to do what gna_run does, but there are a few special connect/ disconnect
# statements. I assume this is the version that allows for 0-length branches. If thisis the case,
# please consider removing the code for gna_run, since this is the exact same function but with a
# larger domain.
def gna_run2(cell, loc_lst, len_lst, file):
    # cell.est = 0.14
    cell.stim.delay = 0.5
    start_all = time.perf_counter()
    deathrec = DeathRec(cell.main_shaft, cell.prop_site, 1)
    e = DeathEnviro(cell, deathrec, cell.stim)
    e.PRINTTIME = True
    mtx = np.ones((len(len_lst)*len(len_lst),4))
    cell.side1.disconnect()
    cell.dau1.disconnect()
    base_gna = e.fullsolve(cell.est, 1e-6, 1e-12)
    cell.side1.connect(cell.main_shaft(0.6))
    cell.dau1.connect(cell.main_shaft(0.6))
    for i, loc in enumerate(loc_lst):
        cell.est = 0.191
        start = time.perf_counter()
        print(f"side branch len: {loc}")
        if loc == 0:
            cell.side1.disconnect()
        else:
            cell.side1.connect(cell.main_shaft(0.6))
            cell.side1.L = loc*elength(cell.side1)
        for j, lens in enumerate(len_lst):
            mtx[j,0] = loc
            # why are we doing element-wise multiplication?
            mtx[j,1] *= lens
            if lens ==0:
                # why are we doing element-wise multiplication?
                mtx[j,2] *= base_gna
                cell.est = base_gna
            else:
                cell.dau1.L = lens*elength(cell.dau1)
                cell._normalize()
                gna = e.fullsolve(cell.est, 1e-6, 1e-12)
                # why are we doing element-wise multiplication?
                mtx[j,2]*=gna
                cell.est = gna
                print(gna)
        # general-use functions should not save files. Instead, they should return data that can be
        # manipulated for other uses.
        np.save(file, mtx)
        end = time.perf_counter()
        print(f"cell time: {(end-start)/60} mins")
    end_all = time.perf_counter()
    # tests/ calculations that take this long should only be found in experiment files. 
    print(f"total time: {(end_all - start_all) / 60} mins")

# again, this function looks very similar to rin_run. Again, if it is the same function but with
# expanded functionality, please remove the former.
def rin_run2(cell, loc_lst, len_lst, file1, file2):
    start_all = time.perf_counter()
    mtx = np.load(file1)
    cell.stim.amp = 0
    cell.setgna(0)
    h.dt = 0.25
    for i, loc in enumerate(loc_lst):
        print(f'side 1 len: {loc}')
        start = time.perf_counter()
        if loc == 0:
            cell.side1.disconnect()
        else:
            cell.side1.connect(cell.main_shaft(0.6))
            cell.side1.L = loc * elength(cell.side1)
        for j, lens in enumerate(len_lst):
            if lens ==0:
                cell.side1.disconnect()
                cell.dau1.disconnect()
                mtx[j,3] = cell.getRin(0.2)
                cell.side1.connect(cell.main_shaft(0.6))
                cell.dau1.connect(cell.main_shaft(0.6))
            else:
                cell.dau1.L = lens*elength(cell.dau1)
                cell._normalize()
                rin = cell.getRin(0.2)
                # why are we doing element-wise multiplication?
                mtx[j,3] *= rin
                print(rin)
        # general-use functions should not save files. Instead, they should return data that can be
        # manipulated for other uses.
        np.save(file2, mtx)
        end = time.perf_counter()
        print(f"cell time: {(end - start)} secs")
    end_all = time.perf_counter()
    # tests/ calculations that take this long should only be found in experiment files. 
    print(f"total time: {(end_all - start_all)/60} mins")

# Graphing should be done in the experiment file.
def graph2(cell_lst, val_lst1, val_lst2):#, label_lst, leg_title):
    colors = ['black','red', 'purple', 'blue', 'cyan', 'green', 'orange', 'pink', 'brown', 'olive', 'grey']
    for i, cell in enumerate(cell_lst):
        # old = np.load(val_lst2[i])
        # row = [0, 0.15697349]
        mtx2 = np.load(val_lst2[i])#np.vstack((row, old))
        old_rin = np.load(val_lst1[i])
        row2 = [0, 102.94759]
        mtx = np.vstack((row2, old_rin))#np.load(val_lst1[i]) #
        plt.plot((mtx[:,0]), mtx[:,1], color= colors[i])

    plt.title(r"$\text{R}_{\text{in}}$ Based on Length")
    plt.xlabel("Side Branch Length ($\\lambda$)")
    plt.ylabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
    plt.grid()
    # plt.title(r"$\bar{\text{g}}_{\text{Na}}$ Based on Length")
    # plt.ylabel(r"$\bar{\text{g}}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$")
    # plt.title(r"$\text{R}_{\text{in}}$ vs $\bar{\text{g}}_{\text{Na}}$")
    # plt.xlabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
    # plt.legend(labels=label_lst, fontsize='large', title=leg_title,
    #            bbox_to_anchor=(1.5, 1.05), loc="upper right", ncols=2, fancybox=True)
    plt.show()

# In conclusion, most of the symbols in this file should not be in the tools directory. The only
# conceptual "tool" that I can think of in your experiments is that which records R_in of a cell.
# That said, most of the symbols here should instead be in an environment class.
# The fact that the functions here rely on the "cell" argument being a specific subclass of the
# base cell is a similar issue, but does not need to be addressed as urgently.
