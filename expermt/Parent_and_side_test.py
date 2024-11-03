import numpy as np
from tqdm import tqdm
from gnatsolv.eq import elength
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
import time
h.load_file("stdrun.hoc")

#       PARENT AND SIDE BRANCH EXPERIMENT        #
#   NOTE: add brief description
def collect_gna(e, est, err):
    cell = e.m
    # NOTE: should we change this naming convention (e.cell instead of e.m)?
    main_elength = 4
    print(main_elength)
    mtx = np.zeros((cell.main_shaft.nseg,2))
    start = time.perf_counter()
    for i,x in enumerate(cell.iter_dist(1)):
        print(f"NEW SPOT: seg = {x}")
        # binary search for g_Na,Thresh given current geometry, up to 9 digits of accuracy
        gna = e.fullsolve(est, err, 1e-9)
        mtx[i,0] = x * main_elength
        mtx[i,1] = gna
        # guess subsequent error based on previous error
        err = (abs(est - gna) + err)/2
        # update the estimate to ensure faster convergence of subsequent binary search
        est = gna
        print(f"g_Na,Thresh for x = {x}: {gna}")
    end = time.perf_counter()
    print(f"collect_gna: total runtime = {end - start}")
    return mtx

def main():
    cell = DCell()  # create cell
    cell.dx = pow(2,-4) # reduce spacial discretization (ensures faster runtime, but reduces numerical accuacy)
    cell.l[2] = cell.l[3] = 0  # sets lengths of unneeded branches to 0
    cell.l[1]=4.0
    cell.update_geom(lengths=[1,2, 3])  # removes the side branches we don't want

    # h.topology() #checks the topology of the cell
    stim = h.IClamp(cell.parent(0.5)) #setups the stimulator
    stim.amp = 0.2 #gives it an amp in mV
    stim.delay = 0 #delay of Clamp from start in ms
    stim.dur = 5 / 16 #duration of clamp in ms

    # set up death recorder and gna solver
    deathrec = DeathRec(cell.main_shaft, cell.main_shaft, 1)
    e = DeathEnviro(cell, deathrec, stim)
    e.PRINTTIME = True # enable solver to print runtime of each individual solve

    initial_estimate = 0.15
    initial_error = 0.05

    data = collect_gna(
            e,
            initial_estimate, initial_error
            )
    np.save('parent_and_side_test_data',data)

if __name__ == '__main__':
    main()
