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


def collect_gna(cell, e, est):

    mtx = np.zeros((cell.main_shaft.nseg,2))
    start = time.perf_counter()
    for x in tqdm(cell.iter_length(1)):
        gna_lst = []
        # print(f"NEW SPOT: b1 seg = {x}")
        for y in tqdm(cell.iter_length(2)):
            time.sleep(0.1)
            # h.topology()
            # print(f"NEW SPOT: seg = {y}")
            gna = e.fullsolve(est, 1e-4, 1e-9)
            gna_lst.append(gna)
            est = gna
            # print(f"gna for seg {x} = {gna}")
            # print(x*4+0.2)
            # bar.update(i)
    end = time.perf_counter()
    print(f"time = {end - start}")
    return mtx

def main(est):

    cell = DCell()  # set up cell
    cell.l[3] = 0  # sets lengths of unneeded branches to 0
    cell.l[1] = cell.l[2] =4.0
    cell.update_geom(lengths=[1,2,3])  # removes the side branches we don't want
    cell.side[1].connect(cell.main_shaft(0.4))
    cell.side[2].connect(cell.main_shaft(0.6))

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

    data = collect_gna(cell,e, est)
    np.save('2_side_branches_lengths_gna_matrix',data)
    # h.psection(sec=cell.side[1])
    # print(cell.side[1].parentseg())

main(0.15816538)
# main(0.45)