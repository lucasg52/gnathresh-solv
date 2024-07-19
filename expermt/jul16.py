from ..cells.smartbranch import SmartBranchCell 
from ..cells.tools import APRecorder
from ..solver.searchclasses import ExpandingSearch
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
    def _normalize(self):
        for sec in self.all[1::]:
            eq.normalize_dlambda(sec, self.dx)
        self._taperIS()
    def _taperIS(self):
        n = self.IS.nseg
        taperarr = np.linspace(self.IS_diam, self.main_diam, n+1)
        for seg, diam in zip(self.IS, taperarr):
            seg.diam = diam
m = SmartBranchCell_mod(0.2, 3)
rec = APRecorder(m.prop_site)
rec.nc.threshold = -10
hardrec = APRecorder(m.prop_site, ran = 0.5+ 2/m.prop_site.nseg )
hardrec.nc.threshold = 10
h.load_file("stdrun.hoc")
g_tstop = 10
g_dt = 1
__NULLSEC__ = h.Section(name = "nullsec")
__NULLSEC__.L = 0.1
__NULLSEC__.diam = 0.1
stim = h.IClamp(__NULLSEC__(1))

__STEADYDUR__ = 200
__STIMDELAY__ = 1
__BRAN_LAM__ = eq.elength(m.prop_site) 
m.prop_site.diam = m.main_shaft.diam
__MAIN_LAM__ = eq.elength(m.main_shaft)
__MAIN_L__ = m.main_shaft.L
__MAXGBAR__ = 0.45

__DISTTABLE__ = np.load("disttable1.npy")
__LAMTABLE__ = np.load("lamtable1.npy")

__ERRFLAG__ = 0
__APPROXS__ =[0.15405218191444875, 0.15160289444029335, 0.17652581892907618, 0.15295877344906333, 0.16470029912889003] #np.ones(3) * 0.2
npl = np.load
nps = np.save
def ngui():
    from neuron import gui
    print(gui)
def check_dlamb(sec, dx):
    return (sec.L/(eq.elength(sec)*dx), sec.nseg)
def set_gbar(m, gbar):
    for sec in m.soma.wholetree():
        try:
            sec.gbar_nafTraub = gbar
            sec.gbar_kdrTraub = gbar
        except AttributeError:
            pass
def proptest(gbar):
    print(gbar)
    prerun(gbar)
    h.continuerun(g_tstop)
    return rec.proptest()
def prerun(gbar):
    global g_dt
    targdt = g_dt
    h.dt = g_dt = 0.25
    assert h.dt == g_dt
    set_gbar(m, gbar)
    h.finitialize(-69)
    h.continuerun(__STEADYDUR__)
    h.dt = g_dt = targdt
    assert h.dt == g_dt

def fullsolve(a, err = 2e-3, acc = pow(2,-30), maxsteps = 45, tstop_init = None):
    global __ERRFLAG__
    global g_tstop
    ptstart = time.process_time()
    if tstop_init is None:
        g_tstop = stim.delay + 10
    else:
        g_tstop  = __STEADYDUR__ + tstop_init
    search = ExpandingSearch(a - err, a + err, proptest, lim_lo = 0, lim_hi = __MAXGBAR__)
    for i in range(maxsteps):
        if search.searchstep():
            break
        if rec.proptest():
            print(rec.recorded[0])
            if not hardrec.proptest():
                print("halted due to partial prop:\nt:" + str(time.process_time() - ptstart))
                print("depth:" + str(search.hi-search.lo))
                return (0-search.a) # to distinguish partial proppers
            if rec.proptest() > 1:
                print("DIE!!!!")
            if rec.recorded[0] > g_tstop - 6:
                g_tstop += 3    #addition because for some reason g_tstop does not like being multiplied
                # changed addition to 3 isntead og 5
                print(g_tstop)
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

    h.define_shape() # for consistent results when looking at movierun

    stim.loc(m.branchlist[0](1))
    stim.amp = 200
    stim.dur = 5/16
    stim.delay = __STIMDELAY__ + __STEADYDUR__ 
    #if proptest(0):
    #    ret = 0.0
    #elif not proptest(__MAXGBAR__):
    #    ret = __MAXGBAR__
    #else:
    #    ret = (fullsolve(a, **kwargs))
    ret = (fullsolve(a, **kwargs))
    return ret


def disconnect():
    while m.branchlist:
        m.rmbranch(0)

def dtruthlite(
        approxs,
        dt = None, dx = None,
        offset = 0,
        **kwargs
        ):
    global g_dt
    disttable = __DISTTABLE__.copy()[offset::]
    lamtable = __LAMTABLE__.copy()[offset::]
    if not (len(approxs) == len(disttable) == len(lamtable)):
        disttable = disttable[:len(approxs)]
        lamtable =   lamtable[:len(approxs)]
    h.dt = g_dt = dt 
    assert h.dt == g_dt
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

def dtruth_sweep(approxs, volume, base = {"dt": -8, "dx": -6}, **kwargs):    # changed base dx from -5 to -6 due to evidence of -5 being too big

    permute = PermuteDict(volume, basekeys = list(base.keys()))
    ret  =[]
    #hist = []
    #oldres = None
    for dargs in permute:
        if ret:
            approxs = ret[-1]
        else:
            approxs = __APPROXS__
        dictadd(dargs, base)
        for k in dargs:
            dargs[k] = pow(2, dargs[k])
        res = dtruthlite(approxs, **dargs, **kwargs)
        ret.append(res)
    return ret

