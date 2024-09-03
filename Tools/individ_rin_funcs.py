from neuron import h
import matplotlib.pyplot as plt
import numpy as np
from cells.adoptedeq import elength
from Tools.environment import DeathEnviro
from Tools.apdeath import DeathRec
from cells.rincell import RinCell, Rin_Ycell, Rin_Trident, Rin_Vcell, Rin_Tcell, Rin_2bbcell
import time
h.load_file("stdrun.hoc")

h.dt = pow(2,-6)

len_lst = [i/100 for i in range(0, 610, 10)]

def gna_run(cell, len_lst, file):
    matrix = np.ones((len(len_lst),2))
    cell.stim.delay = 0.5
    cell.est = 0.15695
    deathrec = DeathRec(cell.main_shaft, cell.prop_site, 1)
    e = DeathEnviro(cell, deathrec, cell.stim)
    e.PRINTTIME = True
    cell.side1.disconnect()
    cell.side2.disconnect()
    base_gna = e.fullsolve(cell.est, 1e-6, 1e-12)
    start = time.perf_counter()
    cell.side1.connect(cell.main_shaft(0.5))
    cell.side2.connect(cell.main_shaft(0.7))
    for j, lens in enumerate(len_lst):
        print(f'length: {lens}')
        matrix[j,0] = lens
        start_cell = time.perf_counter()
        if lens ==0:
            matrix[j,1] = base_gna
            cell.est = 0.15695
        else:
            cell.side1.L = (lens/1)*elength(cell.side1)
            cell.side2.L = (lens/1)*elength(cell.side2)
            # cell.dau2.L = (lens/2)*elength(cell.dau2)
            # cell.dau3.L = (lens/2)*elength(cell.dau3)
            cell._normalize()
            gna = e.fullsolve(cell.est, 1e-6, 1e-12)
            matrix[j,1]=gna
            cell.est = gna
            print(gna)
        end_cell = time.perf_counter()
        print(f'length time = {(end_cell-start_cell)/60} mins')
    np.save(file, matrix)
    end = time.perf_counter()
    print(f"cell time: {(end-start)/60} mins")

def rin_run(cell, len_lst, file):
    start = time.perf_counter()
    cell.stim.amp = 0
    cell.setgna(0)
    mtx = np.ones((len(len_lst),2))
    h.dt = pow(2,-6)
    for j, lens in enumerate(len_lst):
        print(f'length: {lens}')
        mtx[j,0] = lens
        if lens ==0:
            cell.side1.disconnect()
            cell.side2.disconnect()
            mtx[j,1] = cell.getRin()
            cell.side1.connect(cell.main_shaft(0.5))
            cell.side2.connect(cell.main_shaft(0.7))
        else:
            cell.side1.L = (lens/1)*elength(cell.side1)
            cell.side2.L = (lens/1) * elength(cell.side2)
            # cell.dau2.L = (lens/2) * elength(cell.dau2)
            # cell.dau3.L = (lens/2)*elength(cell.dau3)
            cell._normalize()
            rin = cell.getRin()
            mtx[j,1] = rin
            print(rin)
    np.save(file, mtx)
    end = time.perf_counter()
    print(f"cell time: {(end - start)} secs")

# file_lst = ['../modfiles/Y_all_6l_act.npy','../modfiles/Tri_all_6l_act.npy',
#             '../modfiles/V_all_6l_act.npy','../modfiles/Wide_all_6l_act.npy',
#             '../modfiles/T_all_6l_act.npy','../modfiles/TwoB_all_6l_act.npy']
#
# def graph(cell_count, file_lst, file_lst2, label_lst, leg_title):
#     # fig, ax = plt.subplot_mosaic([['a)', 'b)'], ['c)', 'c)']],
#     #                    layout='constrained')
#     colors = ['orange', 'green', 'red', 'blue', 'purple', 'brown', 'pink', 'cyan', 'olive', 'gray', 'black']
#     matrix = np.load('../modfiles/base_06_rin_6l_tak3.npy')
#     matrix2 = np.load('../modfiles/base_06_gna_6l_tak2.npy')
#     plt.plot(matrix[:,1], matrix2[:,1], color = 'black')
#     for i in range(cell_count + 1):
#         mtx = np.load(file_lst[i])
#         mtx2 = np.load(file_lst2[i])
#         plt.plot(mtx[1::,2], mtx2[1::,1]-0.00085, color= colors[i])
#         # plt.plot(mtx[:,0], mtx[:,1], color= colors[i])
#         # plt.plot(mtx[:,2], mtx[:,1], color= colors[i])
#     plt.legend(labels=label_lst, loc="upper right", fontsize = 'large', title = leg_title)
#     # plt.title(r"$\text{R}_{\text{in}}$ (M$\Omega$) Base on Length [Equivalent Cables]", fontsize=14)
#     # plt.xlabel("log$_{10}$(side branch length in $\\lambda$)",
#     #            fontsize=14)  # f"Length of {branch} branch in", "$\\lambda$")
#     # plt.ylabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)", fontsize=14)
#     plt.grid()
#     # plt.title(r"$\text{g}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$ Based on Length [Equivalent Cables]", fontsize = 14)
#     # plt.xlabel("log$_{10}$(side branch length in $\\lambda$)", fontsize = 14)
#     # plt.ylabel(r"$\text{g}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$", fontsize = 14)
#     plt.title(r"$\text{R}_{\text{in}}$ vs $\text{g}_{\text{Na}}$ [Equivalent Cables]", fontsize=14)
#     plt.xlabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)", fontsize = 17)
#     plt.ylabel(r"$\text{g}_{Na} (\frac{\text{mho}}{\text{cm}^2})$", fontsize = 14)
#     # ax['c)'].grid()
#     plt.show()