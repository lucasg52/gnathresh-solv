import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
h.load_file("stdrun.hoc")

def collect_gna(cell, e, est):
    mtx = np.zeros((cell.main_shaft.nseg,2))
    for i,x in enumerate(cell.iter_dist(0)):
        print(f"NEW SPOT: seg = {x}")
        gna = e.fullsolve(est, 1e-4, 1e-9)
        mtx[i,0]=x*4
        mtx[i,1]=gna
        if i<=10:
            est = gna - 0.02
        else:
            est = gna
        print(f"gna for seg {x} = {gna}")
        # print(x*4+0.2)
    return mtx

def main(est):
    cell = DCell()  # set up cell
    cell.l[1] = cell.l[2] = cell.l[3] = 0  # sets lengths of unneeded branches to 0
    cell.update_geom(lengths=[1, 2, 3])  # removes the side branches we don't want

    # h.topology() #checks the topology of the cell
    stim = h.IClamp(cell.parent(0.5))
    stim.amp = 0.2
    stim.delay = 0
    stim.dur = 5 / 16

    # set up death recorder and gna solver
    deathrec = DeathRec(cell.main_shaft, cell.main_shaft, 1)
    e = DeathEnviro(cell, deathrec, stim)
    e.PRINTTIME = True
    est = est  # estimate for initial gna

    data = collect_gna(cell,e, est)
    np.save('parent_branch_base_test',data)

# main(0.15816538)
main(0.45)