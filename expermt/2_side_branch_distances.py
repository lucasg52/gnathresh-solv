import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
from tqdm import tqdm
import time
import progressbar
h.load_file("stdrun.hoc")

# bar = progressbar.ProgressBar()
def collect_gna(cell, e, est, err):
    mtx = np.zeros((cell.main_shaft.nseg,cell.main_shaft.nseg))
    start = time.perf_counter()
    for x in tqdm(cell.iter_dist(1)):
        gna_lst = []
        # print(f"NEW SPOT: b1 seg = {x}")
        for y in tqdm(cell.iter_dist(2)):
            # print(f"NEW SPOT: seg = {y}")
            # binary search for g_Na,Thresh given current geometry, up to 9 digits of accuracy
            gna = e.fullsolve(est, err, 1e-9)
            gna_lst.append(gna)
            # guess subsequent error based on previous error
            err = (abs(est - gna) + err) / 2
            # update the estimate to ensure faster convergence of subsequent binary search
            est = gna
            # print(f"gna for seg {x} = {gna}")
        mtx[x,:]=gna_lst
    end = time.perf_counter()
    print(f"time = {end - start}")
    return mtx

def main(est):

    cell = DCell()  # set up cell
    cell.dx = pow(2,-3)
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
    e.PRINTTIME = True #traacks how long it takes
    est = est  # estimate for initial gna

    initial_estimate = 0.15
    initial_error = 0.05

    data = collect_gna(
        e,
        initial_estimate, initial_error
    )
    np.save('2_side_branch_distances_gna_matrix',data)

main(0.15816538)
# main(0.45)