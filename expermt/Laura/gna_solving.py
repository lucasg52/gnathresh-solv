from expermt.Laura.Rin_cells2 import Rin_cell_1, Rin_cell_1y, Rin_cell_3y
from solver.searchclasses import BinSearch, ExpandingSearch
from tools.aprecorder import APRecorder
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import cm as cmap
h.load_file("stdrun.hoc")
def ngui():
    from neuron import gui
    # print(gui)

__MAXGBAR__ = 0.2
m = Rin_cell_1(0)
m.dx = 0.025
n = Rin_cell_1y(1)
n.dx = 0.025
w = Rin_cell_3y(2)
w.dx = 0.025
rec1 = APRecorder(m.prop_site)
rec2 = APRecorder(n.prop_site)
rec3 = APRecorder(w.prop_site)

def proptest_m(gbar):
    m.setgna(gbar)
    h.finitialize(-69)
    h.continuerun(10)
    #print(ret)
    return rec1.proptest()
def searchreset_err_m(a, err):
    global search
    hi = a + err
    lo = a - err
    search = BinSearch(lo, hi, proptest_m)

# def fullsolve_m(steps = 30):
#     search = BinSearch(0, 0.45, proptest_m)
#     h.tstop = 10
#     for i in range(steps):
#             search.searchstep()
#             if rec1.proptest():
#                 if rec1.recorded[0]>h.tstop/2:
#                     h.tstop += 3
#     return search.a

def fullsolve_m(a, err = 2e-3, acc = pow(2,-30), maxsteps = 45, tstop_init = None):
    global __ERRFLAG__
    ptstart = time.process_time()
    if tstop_init is None:
        h.tstop = stim1.delay + 10
    else:
        h.tstop  = tstop_init
    search = ExpandingSearch(a - err, a + err, proptest_m, lim_lo = 0, lim_hi = __MAXGBAR__)
    for i in range(maxsteps):
        if search.searchstep():
            break
        if rec1.proptest():
            if rec1.recorded[0] > h.tstop - 6:
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

def proptest_n(gbar):
    n.setgna(gbar)
    h.finitialize(-69)
    h.continuerun(10)
    #print(ret)
    return rec2.proptest()
def searchreset_err_n(a, err):
    global search
    hi = a + err
    lo = a - err
    search = BinSearch(lo, hi, proptest_m)

# def fullsolve_n(steps = 30):
#     search = BinSearch(0, 0.45, proptest_n)
#     h.tstop = 10
#     for i in range(steps):
#             search.searchstep()
#             if rec2.proptest():
#                     if rec2.recorded[0]>h.tstop/2:
#                         h.tstop += 3
#     return search.a
def fullsolve_n(a, err = 2e-3, acc = pow(2,-30), maxsteps = 45, tstop_init = None):
    global __ERRFLAG__
    ptstart = time.process_time()
    if tstop_init is None:
        h.tstop = stim1.delay + 10
    else:
        h.tstop = tstop_init
    search = ExpandingSearch(a - err, a + err, proptest_n, lim_lo = 0, lim_hi = __MAXGBAR__)
    for i in range(maxsteps):
        if search.searchstep():
            break
        if rec2.proptest():
            if rec2.recorded[0] > h.tstop - 6:
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

def proptest_w(gbar):
    w.setgna(gbar)
    h.finitialize(-69)
    h.continuerun(10)
    #print(ret)
    return rec3.proptest()
def searchreset_err_w(a, err):
    global search
    hi = a + err
    lo = a - err
    search = BinSearch(lo, hi, proptest_w)

# def fullsolve_w(steps = 30):
#     search = BinSearch(0, 0.45, proptest_w)
#     h.tstop = 10
#     for i in range(steps):
#             search.searchstep()
#             if rec3.proptest():
#                 if rec3.recorded[0]>h.tstop/2:
#                     h.tstop += 3
#     return search.a

def fullsolve_w(a, err = 2e-3, acc = pow(2,-30), maxsteps = 45, tstop_init = None):
    global __ERRFLAG__
    ptstart = time.process_time()
    if tstop_init is None:
        h.tstop = stim1.delay + 10
    else:
        h.tstop = tstop_init
    search = ExpandingSearch(a - err, a + err, proptest_w, lim_lo = 0, lim_hi = __MAXGBAR__)
    for i in range(maxsteps):
        if search.searchstep():
            break
        if rec3.proptest():
            if rec3.recorded[0] > h.tstop - 6:
                h.tstop += 3    #addition because for some reason h.tstop does not like being multiplied
                # changed addition to 3 isntead og 5
                print(h.tstop)
        if search.hi - search.lo <= acc:
            break
    print(time.process_time() - ptstart)
    if i == maxsteps - 1:
        print("WARNING!!! U REACHED THE MAX STEPS!!")
#     if abs(search.a - a) > 4*err:
        __ERRFLAG__ = abs(search.a - a)
    return search.a


def set_ELen(section, length, dx):
	Lambda = elength(section)
	section.L = length * Lambda
	gnat.normalize_dlambda(section, dx)

def setting_length(stim_len, dau_len, m=m, n=n):
    m.stim_b.L = stim_len*elength(m.stim_b)
    n.stim_b.L = stim_len*elength(n.stim_b)
    w.stim_b.L = stim_len * elength(w.stim_b)
    m.side1.L = dau_len*elength(m.side1)
    if dau_len == 0.05 or dau_len == 0.1:
        n.side1.L = (dau_len/2)*elength(n.side1)
        n.dau1.L = (dau_len/2)*elength(n.dau1)
        n.dau2.L = (dau_len/2)*elength(n.dau2)
        w.side1.L = (dau_len/2)*elength(w.side1)
        w.dau1.L = (dau_len/2)*elength(w.dau1)
        w.dau2.L = (dau_len/2)*elength(w.dau2)
        w.dau3.L = (dau_len/2)*elength(w.dau3)
        #print("dau_len halved")
    elif dau_len>0.1 and dau_len<2.07:
        n.side1.L = (dau_len)*elength(n.side1)
        n.dau1.L = (dau_len)*elength(n.dau1)
        n.dau2.L = (dau_len)*elength(n.dau2)
        w.side1.L = (dau_len)*elength(w.side1)
        w.dau1.L = (dau_len)*elength(w.dau1)
        w.dau2.L = (dau_len)*elength(w.dau2)
        w.dau3.L = (dau_len)*elength(w.dau3)
        #print("dau_len amended")
    elif dau_len>2.05:
        n.side1.L = dau_len * elength(n.side1)
        n.dau1.L = dau_len * elength(n.dau1)
        n.dau2.L = dau_len * elength(n.dau2)
        w.side1.L = dau_len * elength(w.side1)
        w.dau1.L = dau_len * elength(w.dau1)
        w.dau2.L = dau_len * elength(w.dau2)
        w.dau3.L = dau_len*elength(w.dau3)

stim1 = h.IClamp(m.stim_b(1))
stim1.amp = 200
stim1.delay = 5
stim1.dur = 5/16

stim2 = h.IClamp(n.stim_b(1))
stim2.amp = 200
stim2.delay = 5
stim2.dur = 5/16

stim3 = h.IClamp(w.stim_b(1))
stim3.amp = 200
stim3.delay = 5
stim3.dur = 5/16

h.dt = pow(2,-7)

rin_base = []
rin_eqi = []
rin_eqi2 = []
gna_base = []
gna_eqi = []
gna_eqi2 = []
diff_list2 = []
diff_list3 = []
lengths = []#[j/100 for j in range(5,400,5)]#np.linspace(0.05, 2, 0.05)

def reset():
    rin_base = []
    rin_eqi = []
    rin_eqi2 = []
    gna_base = []
    gna_eqi = []
    gna_eqi2 = []
    diff_list2 = []
    diff_list3 = []
    lengths = []

def Rin(part):
	imp_geter = h.Impedance()
	imp_geter.loc(part(0))
	imp_geter.compute(1)
	return imp_geter.input(part(0))

def my_imped(part):
    h.dt = 0.5
    if part == m.side1:
        m.side1.gbar_nafTraub = 0
        m.side1.gbar_kdrTraub =0
    if part == n.side1:
        n.side1.gbar_nafTraub = 0
        n.side1.gbar_kdrTraub =0
        n.dau1.gbar_nafTraub = 0
        n.dau1.gbar_kdrTraub =0
        n.dau2.gbar_nafTraub = 0
        n.dau2.gbar_kdrTraub =0
    if part == w.side1:
        w.side1.gbar_nafTraub = 0
        w.side1.gbar_kdrTraub =0
        w.dau1.gbar_nafTraub = 0
        w.dau1.gbar_kdrTraub =0
        w.dau2.gbar_nafTraub = 0
        w.dau2.gbar_kdrTraub =0

    stim = h.IClamp(part(0))
    stim.amp = 200
    stim.dur = 100
    stim.delay = 5
    h.finitialize(-70)
    h.continuerun(100)
    stim.amp=0
    return part(0).v / 200
    
def run(stim_len, dau_len, rin_solver, title):
    lengths = [j / 100 for j in range(60, 205, 5)]  # np.linspace(0.05, 2, 0.05)
    for i in lengths:
        setting_length(stim_len,i)
        m.all = m.soma.wholetree()
        n.all = n.soma.wholetree()
        w.all = w.soma.wholetree()
        m._normalize()
        n._normalize()
        w._normalize()
        m.side1.disconnect()
        n.side1.disconnect()
        w.side1.disconnect()
        # print(f"base cell: R_in = {my_imped(m.side1(0))}")
        print(m.side1.L/118.84, n.side1.L/118.84, "i:", i)
        if rin_solver == Rin:
            rin_base.append(Rin(m.side1))#my_imped(m.side1))
        # print(f"equiv: R_in = {my_imped(n.side1(0))}")
            rin_eqi.append(Rin(n.side1))#my_imped(n.side1))
            rin_eqi2.append(Rin(w.side1))
            diff_list2.append(Rin(m.side1)-(Rin(n.side1)))
            diff_list3.append(Rin(m.side1)-(Rin(w.side1)))
        if rin_solver == my_imped:
            rin_base.append(my_imped(m.side1))  # my_imped(m.side1))
            # print(f"equiv: R_in = {my_imped(n.side1(0))}")
            rin_eqi.append(my_imped(n.side1))  # my_imped(n.side1))
            rin_eqi2.append(my_imped(w.side1))
            diff_list2.append(my_imped(m.side1)-(my_imped(n.side1)))
            diff_list3.append(my_imped(m.side1)-(my_imped(w.side1)))

        m.side1.connect(m.main_shaft(0.6))
        n.side1.connect(n.main_shaft(0.6))
        w.side1.connect(w.main_shaft(0.6))
        m.all = m.soma.wholetree()
        n.all = n.soma.wholetree()
        w.all = w.soma.wholetree()
        h.dt= pow(2,-7)
        # print(f"base cell: gna = {fullsolve_m(53)}")
        gna_base.append(fullsolve_m(0.1))
        # print(f"equiv: gna = {fullsolve_n(53)}")
        gna_eqi.append(fullsolve_n(0.1))
        gna_eqi2.append(fullsolve_w(0.1))
    m.side1.disconnect()
    n.side1.disconnect()
    w.side1.disconnect()
    print(f"Control: gna base = {fullsolve_m(0.1)}")
    # print(f"Control: gna equiv = {fullsolve_n(0.1)}")
    # print(f"Control: gna equiv 2 = {fullsolve_w(0.1)}")

    fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(8,4))
    ax[0,0].plot(lengths,rin_base, 'blue', label="Rin for base cell")
    ax[0,0].plot(lengths,rin_eqi, 'orange', label="Rin for eqi cell")
    ax[0,0].plot(lengths, rin_eqi2, 'green', linestyle = 'dashed', label='Rin for eqi2 cell')
    ax[0,1].plot(lengths,gna_base, 'blue',label=f"Gna for base cell; control")
    ax[0,1].plot(lengths,gna_eqi, 'orange', label="Gna for eqi cell")
    ax[0,1].plot(lengths,gna_eqi2, 'green', linestyle = 'dashed', label="Gna for eqi2 cell")
    ax[1,1].plot(rin_base, gna_base, 'blue', label="Rin vs Gna for base cell")
    ax[1,1].plot(rin_eqi, gna_eqi, 'orange', label="Rin vs Gna for equi cell")
    ax[1,1].plot(rin_eqi2, gna_eqi2, 'green', linestyle = 'dashed', label='Rin vs Gna for equiv cell 2')
    ax[1,0].plot(lengths,diff_list2, 'orange', label="base - equiv")
    ax[1,0].plot(lengths,diff_list3, 'green', linestyle = 'dashed', label="base - equiv2")
    ax[0,0].grid()
    ax[1,0].grid()
    ax[0,1].grid()
    ax[1,1].grid()
    ax[0,0].legend()
    ax[1,0].legend()
    ax[0,1].legend()
    ax[1,1].legend()
    ax[0,1].set_xlabel("length in lambda")  # 'length of side branches in lambda'
    ax[0,0].set_ylabel("Rin in mV/nA")  # 'node along main shaft')
    ax[0,1].set_ylabel("Gna thresh")  # 'input resistance')
    ax[1,0].set_ylabel("Difference from base")
    ax[1,0].set_xlabel("Rin")
    ax[1,1].set_xlabel("Rin")
    ax[1,1].set_ylabel("Gna")
    # fig.title(f"Rin vs Gna based on varying side branch lengths; {title}")
    plt.show()