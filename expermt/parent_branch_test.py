import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
h.load_file("stdrun.hoc")

def collect_gna(cell, e, est):
    mtx = np.zeros((cell.main_shaft.nseg,2))
    for i,seg in enumerate(cell.main_shaft):
        cell.prop_site.connect(seg)
        gna = e.fullsolve(est, 1e-5, 1e-12)
        mtx[i,0]=seg
        mtx[i,1]=gna
        est = gna
        print(f"gna for seg {i} = {gna}")
    return mtx

if True:
    cell = DCell()  # set up cell
    cell.l[1] = cell.l[2] = cell.l[3] = 0  # sets lengths of unneeded branches to 0
    cell.update_geom(lengths=[1, 2, 3])  # removes the side branches we don't want

    # h.topology() #checks the topology of the cell
    stim = h.IClamp(cell.parent(0.5))
    stim.amp = 0.2
    stim.delay = 0
    stim.dur = 5 / 16

    # set up death recorder and gna solver
    deathrec = DeathRec(cell.main_shaft, cell.prop_site, 1)
    e = DeathEnviro(cell, deathrec, stim)
    e.PRINTTIME = True
    est = 0.18  # estimate for initial gna

    # collect_gna(cell,e, est)

# main(0.2)