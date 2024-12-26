import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
import time
h.load_file("stdrun.hoc")

def collect_gna(e, est, err):
    cell = e.m
    mtx = np.zeros((cell.main_shaft.nseg,cell.main_shaft.nseg))
    seg_mtx = []
    start = time.perf_counter()
    for l,x in enumerate(cell.iter_dist(1)):
        gna_lst = []
        seg_mtx.append(x)
        # print(f"NEW SPOT: b1 seg = {x}")
        for y in cell.iter_dist(2):
            # print(f"NEW SPOT: seg = {y}")
            # binary search for g_Na,Thresh given current geometry, up to 9 digits of accuracy
            gna = e.fullsolve(est, err, 1e-9)
            gna_lst.append(gna)
            # guess subsequent error based on previous error
            err = (abs(est - gna) + err) / 2
            # update the estimate to ensure faster convergence of subsequent binary search
            est = gna
            # print(f"gna for seg {x} = {gna}")
        print(gna_lst)
        mtx[l,:]=gna_lst
    end = time.perf_counter()
    print(f"time = {end - start}")
    return mtx, seg_mtx

def main():

    cell = DCell()  # set up cell
    cell.dx=pow(2,-3)
    cell._normalize()
    cell.l[3] = 0  # sets lengths of unneeded branches to 0
    cell.l[1] = cell.l[2] =4.0
    cell.update_geom(lengths=[1,2,3])  # removes the side branches we don't want

    # h.topology() #checks the topology of the cell
    stim = h.IClamp(cell.parent(0.5)) #setups the stimulator
    stim.amp = 0.2 #gives it an amp in mV
    stim.delay = 0 #delay of Clamp from start in ms
    stim.dur = 5 / 16 #duration of clamp in ms

    # set up death recorder and gna solver
    deathrec = DeathRec(cell.main_shaft, cell.main_shaft, 1)
    e = DeathEnviro(cell, deathrec, stim)
    e.PRINTTIME = True #tracks how long it take

    initial_estimate = 0.15
    initial_error = 0.05

    gna_data, main_seg_data = collect_gna(
        e,
        initial_estimate, initial_error
    )
    np.save('2_side_branch_distances_gna_matrix1',gna_data)
    np.save('side_and_sub_branches_distances_seg_matrix_for_main1', main_seg_data)
    print(f"gna stored in: side_and_sub_branches_distances_gna_matrix1.npy")
    print(f"seg stored in: side_and_sub_branches_distances_seg_matrix_for_main1.npy")
if __name__ == '__main__':
    main()