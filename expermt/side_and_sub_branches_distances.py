import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
from tqdm import tqdm
import time
h.load_file("stdrun.hoc")


def collect_gna(e, est, err): #collects gna for each geometry by changing the distance of the side branch and the the subbranch
    cell = e.m
    gna_mtx = np.zeros((cell.main_shaft.nseg,cell.main_shaft.nseg))
    seg_mtx = np.zeros((cell.parent.nseg,1))
    start = time.perf_counter()
    for l,m in enumerate(cell.iter_dist(1)):
        gna_lst = []
        # print(f"NEW SPOT: b1 seg = {x}")

        # for y in cell.iter_dist(3):
        for y,seg in enumerate(
                list(cell.parent.allseg())
                [1:-1]
        ):
            cell.side[3].connect(seg)
            seg_mtx[0,l] = seg.x
            h.topology()
            # print(f"NEW SPOT: seg = {y}")
            gna = e.fullsolve(est, err, 1e-9)
            gna_lst.append(gna)

            # guess subsequent error based on previous error
            err = (abs(est - gna) + err) / 2
            # update the estimate to ensure faster convergence of subsequent binary search
            est = gna

        gna_mtx[l,:]=gna_lst

            # print(f"gna for seg {x} = {gna}")
    # end = time.perf_counter()
    # print(f"time = {end - start}")
    return gna_mtx, seg_mtx

def main():

    global cell
    cell = DCell()  # set up cell
    cell.l[2] = 0  # sets lengths of unneeded branches to 0
    cell.l[1] = 4.0
    cell.l[3] =4.0
    cell.update_geom(lengths=[1,2,3])  # removes the side branches we don't want


    # h.topology() #checks the topology of the cell
    global stim
    stim = h.IClamp(cell.parent(0.5)) #setups the stimulator
    stim.amp = 0.2 #gives it an amp in mV
    stim.delay = 0 #delay of Clamp from start in ms
    stim.dur = 5 / 16 #duration of clamp in ms

    # set up death recorder and gna solver
    global e
    deathrec = DeathRec(cell.main_shaft, cell.main_shaft, 1)
    e = DeathEnviro(cell, deathrec, stim)
    e.PRINTTIME = True #enable solver to print runtime of each individual solve

    initial_estimate = 0.15
    initial_error = 0.05

    gna_data, seg_data = collect_gna(
        e,
        initial_estimate, initial_error
    )
    np.save('side_and_sub_branches_distances_gna_matrix1',gna_data)
    np.save('side_and_sub_branches_distances_seg_matrix_for_parent1', seg_data)
    print(f"gna stored in: side_and_sub_branches_distances_gna_matrix1.npy")
    print(f"seg stored in: side_and_sub_branches_distances_seg_matrix_for_parent1.npy")

if __name__ == '__main__':
    main()