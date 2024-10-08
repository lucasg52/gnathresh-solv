import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
import time
h.load_file("stdrun.hoc")

def collect_gna(cell, e, est):
    mtx = np.zeros((cell.main_shaft.nseg,2))
    start = time.perf_counter()
    for i,x in enumerate(cell.iter_dist(1)):
        print(f"NEW SPOT: seg = {x}")
        gna = e.fullsolve(est, 1e-4, 1e-9)
        mtx[i,0]=x*4
        mtx[i,1]=gna
        est = gna - 0.02
        print(f"gna for seg {x} = {gna}")
        # print(x*4+0.2)
    end = time.perf_counter()
    print(f"time = {end - start}")
    return mtx

def main(est):
    cell = DCell()  # set up cell
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
    e.PRINTTIME = True #traacks how long it takes
    # est = est  # estimate for initial gna

    data = collect_gna(cell,e, est)
    np.save('parent_and_side_test_data',data)

main(0.15816538)
# main(0.45)