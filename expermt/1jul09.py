from ..cells.smartbranch import SmartBranchCell 
from ..cells.tools import APRecorder
from ..solver.searchclasses import BinSearch
from ..cells import adoptedeq as eq
from ..cells import kinetics as kin
from neuron import h
#from matplotlib import pyplot as plt
import numpy as np
import random
m = SmartBranchCell(0.2, 3)
rec = APRecorder(m.prop_site)
h.tstop = 10
stim = b_p = b_s = None
__SEED__ = "gna"
__BRAN_LAM__ = eq.elength(m.prop_site) 
m.prop_site.diam = m.main_shaft.diam
__MAIN_LAM__ = eq.elength(m.main_shaft)
__MAIN_L__ = m.main_shaft.L
__MINLAM__ = 1
__MAXLAM__ = 3
__PAR_ADD_LAM__ = 2
__MAXGBAR__ = 0.4
h.load_file("stdrun.hoc")
def ngui():
    from neuron import gui
    print(gui)
def check_dlamb(sec, dx):
    return (sec.L/(eq.elength(sec)*dx), sec.nseg)
def set_gbar(m, gbar):
    for sec in m.all:
        try:
            sec.gbar_nafTraub = gbar
            sec.gbar_kdrTraub = gbar
        except AttributeError:
            pass
def proptest(gbar):
    set_gbar(m, gbar)
    h.finitialize(-69)
    h.continuerun()
    #print(ret)
    return rec.proptest()
def searchreset_err(a, err):
    global search
    hi = a + err
    lo = a - err
    search = BinSearch(lo, hi, proptest)

def fullsolve(steps = 30, tstop_init = 10):
    h.tstop  = tstop_init
    search = BinSearch(0, __MAXGBAR__, proptest)
    for i in range(steps):
            search.searchstep()
            if proptest():
                if (h.tstop - rec.recorded[0]) > h.tstop/2:
                    h.tstop *= 1.5
    return search.a

def experiment(dists, lens, steps = 12):#,discon = True):
    global stim
    assert len(dists) == len(lens)
    assert h.dt == pow(2,-8)
    assert m.dx == pow(2,-5)
    
    disconnect()
    for d, L, in zip(dists, lens):
        m.newbranch(d, L)
        m.branchlist[-1].insmod_Traub() # idk
    if stim is None:
        stim = h.IClamp(b_p(1))
        stim.amp = 200
        stim.dur = 5/16
        stim.delay = 5
    if proptest(0):
        ret = 0.0
    elif not proptest(__MAXGBAR__):
        ret = __MAXGBAR__
    else:
        ret = (fullsolve(steps = steps))
    return ret

def disconnect():
    while m.branchlist:
        m.rmbranch(0)

def makerand(leng, seed = __SEED__):
    retarr = []
    random.seed(seed)
    for i in range(leng):
        retarr.append(random.random())
    return retarr

def randtable(leng, los, his, seed = __SEED__, offset = 0):
    colcnt = len(los)
    assert colcnt == len(his)
    coef = np.identity(colcnt) * np.array([[hi - lo,] for (lo, hi) in zip(los, his)])
    lomatx = np.tile(los, (leng, 1)) 
    rand = np.array(makerand(colcnt * leng)[(colcnt * offset)::])
    rect = rand.reshape(leng, colcnt)
    scaled = np.matmul(rect, coef)
    ret = scaled + lomatx
    return ret

def groundtruth(simcnt, steps = 12, **kwargs):
    table = randtable(
                leng = simcnt,
                los  = (0,0,__MIN)
            )
    h.dt = pow(2,-8) 
    m.dx = pow(2,-5)
    return [experiment(row[:4], row[4::], steps = steps) for row in table]


def dryrun(simcnt, **kwargs):
    dists = randtable(simcnt, 0, __MAIN_L__, **kwargs)
    print(dists)
    lengs = randtable(simcnt, __MINLAM__, __MAXLAM__ , **kwargs)
    print(lengs)

    return np.hstack((dists,lengs))
