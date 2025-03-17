import random
import sys
from neuron import h
import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.apdeath import DeathRec
# from gnatsolv import eq
from gnatsolv.tools.environment import DeathEnviro
#from ..tools.aprecorder import APRecorder
h.load_file('stdrun.hoc')

def calcthreshes(
        seed='gnat',    # Specify an rng seed for morphologies
        leng=10         # how many cells to create
    ):
    global cell, stim, e, deathrec # only for debug.
    ### MORPHOLOGY PARAMETERS: ###
    cell = DCell()
    cell.dx =pow(2,-7)
    cell._normalize()
    deathrec = DeathRec(cell.main_shaft, cell.main_shaft, tstart = 1)
    stim = h.IClamp(cell.parent(1))
    stim.amp = 0.2
    stim.delay = 0
    stim.dur = 5/16
    cell.update_length(1, 0) # remove one of the side branches

    e = DeathEnviro(
            cell,
            deathrec,
            stim
            )
    ret = []
    random.seed(seed)
    
    for i in range(leng):
        print(f'calculating threshes for geometry {i+1} out of {leng}')
        cell.l= np.array(
                [4, 0, 4*random.random(), 2*random.random()]
                )
        cell.d= np.array(
                [0.4, 0, 0.5*random.random(), random.random()]
                )
        cell.update_geom()
        ret.append(accsweep(e))
    return ret

def normalizerange(est, rad, acc): # an attempt to both optimize search radius, and force gNaT into bins of size `acc`, when using an adaptive ExpandingBinSearch sweep
                                   # To disable, simply call fullsolve (see within accsweep) with raw parameters
    n = int(est/acc)
    est_n = n*acc
    dif = abs(est_n - est)
    i = 1
    while pow(2, i)*acc < rad + dif:
        i += 1
    return est_n, pow(2, i)*acc, acc


def accsweep(    # create a list of gNaT computed by environment `e` under bit roundoff from 0 to rmax, with steps of 4 bits
        e, # environment
        rmax = 40,    # maximum roundoff. cannot be higher than 51
        est_init = 0.15, rad_init = 0.05, # initial search estimate and radius
        acc = pow(2,-14)                  # search accuracy 
    ):
    est = est_init
    rad = rad_init
    ret = []

    for i in range(0, rmax +1, 4):
        print('|',end = '')
        sys.stdout.flush()
        h.roundoff_nafTraub = i
        h.roundoff_kdrTraub = i

        gnat = e.fullsolve(*normalizerange(est, rad, acc))
        # disable normalizerange:
        # gnat = e.fullsolve(est, rad, acc)
        err = abs(est-gnat)
        est = gnat
        rad = (err+acc)*1.5
        ret.append(gnat)

    return ret

