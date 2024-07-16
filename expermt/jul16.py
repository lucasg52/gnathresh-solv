from ..cells.smartbranch import SmartBranchCell 
from ..cells.tools import APRecorder
from ..solver.searchclasses import BinSearch, ExpandingSearch
from ..cells import adoptedeq as eq
#from ..cells import kinetics as kin
from neuron import h
#from matplotlib import pyplot as plt
import numpy as np
#import random
import time
class SmartBranchCell_mod(SmartBranchCell):
    def __repr__(self):
        return("m[0]")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soma.nseg = 1
        self.prop_site.diam = self.main_shaft.diam
    def _normalize(self):
        for sec in self.all[1::]:
            eq.normalize_dlambda(sec, self.dx)
m = SmartBranchCell_mod(0.2, 3)
rec = APRecorder(m.prop_site)
h.load_file("stdrun.hoc")
h.tstop = 10
__NULLSEC__ = h.Section(name = "nullsec")
__NULLSEC__.L = 0.1
__NULLSEC__.diam = 0.1
stim = h.IClamp(__NULLSEC__(1))

__STEADYDUR__ = 200
__STIMDELAY__ = 1
#__SEED__ = "gna"
__BRAN_LAM__ = eq.elength(m.prop_site) 
__MAIN_LAM__ = eq.elength(m.main_shaft)
__MAIN_L__ = m.main_shaft.L
__MINLAM__ = 0.75
__MAXLAM__ = 2.5
__PAR_ADD_LAM__ = 2
__MAXGBAR__ = 0.45

__DISTTABLE__ = np.load("disttable1.npy")
__LAMTABLE__ = np.load("lamtable1.npy")

__ERRFLAG__ = 0
__APPROXS__ = np.ones(3) * 0.2
npl = np.load
nps = np.save
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
    targdt = h.dt
    h.dt = 0.25
    set_gbar(m, gbar)
    h.finitialize(-69)
    h.t = -__STEADYDUR__
    h.continuerun(0)
    h.dt = targdt

    h.continuerun(h.tstop)
    #print(ret)
def searchreset_err(a, err):
    global search
    hi = a + err
    lo = a - err
    search = BinSearch(lo, hi, proptest)

def fullsolve(a, err = 2e-3, acc = pow(2,-30), maxsteps = 45, tstop_init = None):
    global __ERRFLAG__
    ptstart = time.process_time()
    if tstop_init is None:
        h.tstop = stim.delay + 10
    else:
        h.tstop  = tstop_init
    search = ExpandingSearch(a - err, a + err, proptest, lim_lo = 0, lim_hi = __MAXGBAR__)
    for i in range(maxsteps):
        if search.searchstep():
            break
        if rec.proptest():
            if rec.recorded[0] > h.tstop - 6:
                h.tstop += 3    #addition because for some reason h.tstop does not like being multiplied
                # changed addition to 3 isntead og 5
                print(h.tstop)
        if search.hi - search.lo <= acc:
            break
    print(time.process_time() - ptstart)
    if i == maxsteps - 1:
        print("WARNING!!! U REACHED THWE MAX STEPS!!")
    if abs(search.a - a) > 4*err:
        __ERRFLAG__ = abs(search.a - a)
    return search.a

def experiment(a, dists = None, lens = None, **kwargs):#,discon = True):
    global stim
    assert len(dists) == len(lens)
    print(m.dx)
    print(h.dt)

    lens = np.multiply(lens, __BRAN_LAM__)
    print(dists, lens)
    
    disconnect()
    for d, L, in zip(dists, lens):
        m.newbranch(L , d)
    stim.loc(m.branchlist[0](1))
    stim.amp = 200
    stim.dur = 5/16
    stim.delay = __STIMDELAY__    
    if proptest(0):
        ret = 0.0
    elif not proptest(__MAXGBAR__):
        ret = __MAXGBAR__
    else:
        ret = (fullsolve(a, **kwargs))
    return ret


def disconnect():
    while m.branchlist:
        m.rmbranch(0)

def dtruth(simcnt, disttable = __DISTTABLE__, lamtable = __LAMTABLE__, dt = None, dx = None, steps = 30, **kwargs):
    h.dt = dt 
    m.dx = dx
    return [
            experiment(dists = dists, lens = lens, steps = steps)
            for dists, lens 
            in zip(disttable, lamtable)
            ], disttable, lamtable

def dtruthlite(
        approxs,
        dt = None, dx = None,
        offset = 0,
        **kwargs
        ):
    disttable = __DISTTABLE__.copy()[offset::]
    lamtable = __LAMTABLE__.copy()[offset::]
    if not (len(approxs) == len(disttable) == len(lamtable)):
        disttable = disttable[:len(approxs)]
        lamtable =   lamtable[:len(approxs)]
    h.dt = dt 
    m.dx = dx
    m._normalize()
    return [
            experiment(a, dists = dists, lens = lens, **kwargs)
            for a, dists, lens 
            in zip(approxs, disttable, lamtable)
            ]

class PermuteDict():
    def __init__(self,volume, basekeys = ["dt","dx"]):
        self.basekeys = basekeys
        self.volume = volume
        self.term = False

    def __iter__(self):
        offset = [] 
        rootkey = self.basekeys[0]
        if len(self.basekeys) == 1:
            yield {rootkey : self.volume}
        else:
            offset = self.basekeys[1::]
            for i in range (self.volume + 1):
                yld = {rootkey: i}
                sub = PermuteDict(self.volume - i, basekeys = offset)
                for subyld in sub:
                    yld.update(subyld)
                    yield yld
def dictadd(da,db):
    assert da.keys() == db.keys()
    for k in db:
        da[k] += db[k]

        #assert sweeplen > 1
        #offset = begin.copy()
        #for k in offset:
        #    offset[k] = 0
    #return da

def dtruth_sweep(approxs, volume, base = {"dt": -8, "dx": -6}, **kwargs):    # changed base dx from -5 to -6 due to evidence of -5 being too big

    permute = PermuteDict(volume, basekeys = list(base.keys()))
    ret  =[]
    #hist = []
    #oldres = None
    for dargs in permute:
        if ret:
            approxs = ret[-1]
        dictadd(dargs, base)
        for k in dargs:
            dargs[k] = pow(2, dargs[k])
        res = dtruthlite(approxs, **dargs, **kwargs)
        #if oldres is not None:
        #    for a, b in zip(res[1::], oldres):
        #        assert all(np.equal(a.flatten(), b.flatten()))
        #oldres = res[1::]
        ret.append(res)
    return ret

