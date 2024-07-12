from cells.smartbranch import SmartBranchCell
from tools.aprecorder import APRecorder
from solver.searchclasses import BinSearch
from cells import adoptedeq as eq
from cells import kinetics as kin
from neuron import h
#from matplotlib import pyplot as plt
import numpy as np
import random
import matplotlib.pyplot as plt

m = SmartBranchCell(0.2, 3)
rec = APRecorder(m.prop_site)
h.dt = pow(2, -8)
m.dx = pow(2, -5)
stim = b_p = b_s = None
__SEED__ = "gna"
__BRAN_LAM__ = eq.elength(m.prop_site)
m.prop_site.diam = m.main_shaft.diam
__MAIN_LAM__ = eq.elength(m.main_shaft)
__MAIN_L__ = m.main_shaft.L
__MINLAM__ = 0.1
__MAXLAM__ = 3
__PAR_ADD_LAM__ = 2
__MAXGBAR__ = 0.45
h.load_file("stdrun.hoc")
def ngui():
    from neuron import gui
    print(gui)
def check_dlamb(sec, dx):
    return (sec.L/(eq.elength(sec)*dx), sec.nseg)
def set_gbar(m, gbar):
    for sec in m.all:
        if sec is not m.soma:
            if sec is not m.IS:
                sec.gbar_nafTraub = gbar
                sec.gbar_kdrTraub = gbar
def proptest(gbar):
    set_gbar(m, gbar)
    h.finitialize(-69)
    h.continuerun(10)
    #print(ret)
    return rec.proptest()
def searchreset_err(a, err):
    global search
    hi = a + err
    lo = a - err
    search = BinSearch(lo, hi, proptest)

def fullsolve(steps = 12):
    search = BinSearch(0, __MAXGBAR__, proptest)
    for i in range(steps):
            search.searchstep()
    return search.a

def experiment(d1, d2, l1, l2, steps = 12):#,discon = True):
    global stim,b_p,b_s
    assert h.dt == pow(2,-8)
    assert m.dx == pow(2,-5)
    if b_p is None:
        b_p = h.Section(name = "parent"    ,cell = m)
        kin.insmod_Traub(b_p        , "axon")
    if b_s is None:
        b_s = h.Section(name = "side"      ,cell = m)
        kin.insmod_Traub(b_s        , "axon")
    if stim is None:
        stim = h.IClamp(b_p(1))
        stim.amp = 200
        stim.dur = 5/16
        stim.delay = 5
    disconnect()
    m.newbranch( (l1+ __PAR_ADD_LAM__) * __BRAN_LAM__, d1, new= b_p)
    m.newbranch(l2 * __BRAN_LAM__, d2, new= b_s)
    # if proptest(0):
    #     ret = 0.0
    # elif not proptest(__MAXGBAR__):
    #     ret = __MAXGBAR__
    # else:
    ret = (fullsolve(steps = steps))
    return ret

def imped(loc):
    stim = h.IClamp(loc)
    stim.amp = 200
    stim.dur = 51
    stim.delay = 5
    h.finitialize(-70)
    h.continuerun(25)
    return loc.v/200

def rin(sec):
		zz = h.Impedance()
		zz.loc(sec)
		zz.compute(0)
		return zz.input(sec)

def experiment_resist(d1, d2, l1, l2, loc):
    global stim,b_p,b_s
    assert h.dt == pow(2,-8)
    assert m.dx == pow(2,-5)
    if b_p is None:
        b_p = h.Section(name = "parent"    ,cell = m)
        kin.insmod_Traub(b_p        , "axon")
    if b_s is None:
        b_s = h.Section(name = "side"      ,cell = m)
        kin.insmod_Traub(b_s        , "axon")
    if stim is None:
        pass
        # stim = h.IClamp(b_p(1))
        # stim.amp = 200
        # stim.dur = 21 #5/16
        # stim.delay = 5
    disconnect()
    m.newbranch( (l1+ __PAR_ADD_LAM__) * __BRAN_LAM__, d1, new= b_p)
    m.newbranch(l2 * __BRAN_LAM__, d2, new= b_s)
    for sec in m.all:
            if sec is not m.soma:
                if sec is not m.IS:
                    sec.gbar_nafTraub = 0
                    sec.gbar_kdrTraub = 0
    ret = (imped(loc))
    return ret

def experiment_resist2(d1, d2, l1, l2, loc):
    global stim,b_p,b_s
    assert h.dt == pow(2,-8)
    assert m.dx == pow(2,-5)
    if b_p is None:
        b_p = h.Section(name = "parent"    ,cell = m)
        kin.insmod_Traub(b_p        , "axon")
    if b_s is None:
        b_s = h.Section(name = "side"      ,cell = m)
        kin.insmod_Traub(b_s        , "axon")
    if stim is None:
        stim = h.IClamp(b_p(1))
        stim.amp = 200
        stim.dur = 21 #5/16
        stim.delay = 5
    disconnect()
    m.newbranch( (l1+ __PAR_ADD_LAM__) * __BRAN_LAM__, d1, new= b_p)
    m.newbranch(l2 * __BRAN_LAM__, d2, new= b_s)
    for sec in m.all:
            if sec is not m.soma:
                if sec is not m.IS:
                    sec.gbar_nafTraub = 0
                    sec.gbar_kdrTraub = 0
    ret = (rin(loc))
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

def makepairs(leng, lo, hi, seed = __SEED__, offset = 0, lohi2 = None):
    if lohi2 is not None:
        lo2, hi2 = lohi2 #unimplimented
    genlen = leng+ offset
    randarr = np.array(makerand(genlen *2, seed = seed))
    randarr = randarr * (hi-lo)
    randarr += lo * np.ones(genlen * 2)
    randarr = randarr.reshape(genlen ,2)
    if offset:
        randarr = randarr[offset::]
    return randarr


def groundtruth(simcnt, steps = 12, **kwargs):
    dists = makepairs(simcnt, 0, __MAIN_L__, **kwargs)
    lengs = makepairs(simcnt, __MINLAM__, __MAXLAM__ , **kwargs)
    h.dt = pow(2,-8)
    m.dx = pow(2,-5)
    joint = np.hstack((dists,lengs))
    return [experiment(*row, steps = steps) for row in joint], joint

def groundtruth_resist(simcnt, loc, **kwargs):
    dists = makepairs(simcnt, 0, __MAIN_L__, **kwargs)
    lengs = makepairs(simcnt, __MINLAM__, __MAXLAM__ , **kwargs)
    h.dt = pow(2,-8)
    m.dx = pow(2,-5)
    joint = np.hstack((dists,lengs))
    return [experiment_resist(*row, loc) for row in joint], joint

def both(simcnt, loc, steps = 12, plt=1, print=1, **kwargs):
    dists = makepairs(simcnt, 0, __MAIN_L__, **kwargs)
    lengs = makepairs(simcnt, __MINLAM__, __MAXLAM__ , **kwargs)
    h.dt = pow(2,-8)
    m.dx = pow(2,-5)
    joint = np.hstack((dists, lengs))
    resist_list = [experiment_resist(*row, loc) for row in joint]
    resist_list2 = [experiment_resist2(*row, loc) for row in joint]
    gna_list = [experiment(*row, steps = steps) for row in joint]
    if plt ==1:
        plot(resist_list, gna_list, 'imped', resist_list2, gna_list, 'rin', 'Rin', 'gna')
    if plt == 0:
        pass
    if print ==1:
        return resist_list, gna_list, joint
    if print == 0:
        pass
    return

def dryrun(simcnt, **kwargs):
    dists = makepairs(simcnt, 0, __MAIN_L__, **kwargs)
    print(dists)
    lengs = makepairs(simcnt, __MINLAM__, __MAXLAM__ , **kwargs)
    print(lengs)

    return np.hstack((dists,lengs))

def plot(x,y, llab, x2, y2, llab2, xlab, ylab):
    plt.plot(x,y,'o', label = llab)
    plt.plot(x2, y2, 'o', label = llab2)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend()
    plt.grid()
    plt.show()