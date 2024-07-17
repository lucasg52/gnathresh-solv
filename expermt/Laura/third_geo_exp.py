from expermt.Laura.Rin_cells2 import Rin_cell_3y
from solver.searchclasses import BinSearch
from tools.aprecorder import APRecorder
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
h.load_file("stdrun.hoc")
def ngui():
    from neuron import gui
    # print(gui)

w = Rin_cell_3y(2)
rec3 = APRecorder(w.prop_site)

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

def fullsolve_w(steps = 30):
    search = BinSearch(0, 0.45, proptest_w)
    h.tstop = 10
    for i in range(steps):
            search.searchstep()
            if rec3.proptest():
                if rec3.recorded[0]>h.tstop/2:
                    h.tstop += 3
    return search.a

def set_ELen(section, length, dx):
	Lambda = elength(section)
	section.L = length * Lambda
	gnat.normalize_dlambda(section, dx)

def setting_length(stim_len, dau_len):
    w.stim_b.L = stim_len*elength(w.stim_b)
    if dau_len>0.1 and dau_len<2.07:
        w.side1.L = (dau_len-0.09)*elength(w.side1)
        w.dau1.L = (dau_len-0.09)*elength(w.dau1)
        w.dau2.L = (dau_len-0.09)*elength(w.dau2)
        w.dau3.L = (dau_len-0.09)*elength(w.dau3)
    else:
        w.side1.L = dau_len * elength(w.side1)
        w.dau1.L = dau_len * elength(w.dau1)
        w.dau2.L = dau_len * elength(w.dau2)
        w.dau3.L = dau_len*elength(w.dau3)

stim3 = h.IClamp(w.stim_b(1))
stim3.amp = 200
stim3.delay = 5
stim3.dur = 5/16

h.dt = pow(2,-5)

rin_equ2 = []
gna_equ2 = []
lengths = [j/100 for j in range(5,400,5)]#np.linspace(0.05, 2, 0.05)

def reset():
    rin_equ2 = []
    gna_equ2 = []
    lengths = []

def Rin(part):
	imp_geter = h.Impedance()
	imp_geter.loc(part(0))
	imp_geter.compute(1)
	return imp_geter.input(part(0))

def my_imped(part):
    h.dt = 0.5
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
    lengths = [j / 100 for j in range(5, 405, 5)]  # np.linspace(0.05, 2, 0.05)
    for i in lengths:
        setting_length(stim_len,i)
        w.all = w.soma.wholetree()
        w._normalize()
        w.side1.disconnect()
        print(w.side1.L/118.84)
        if rin_solver == Rin:
            rin_equ2.append(Rin(w.side1))#my_imped(n.side1))
        if rin_solver == my_imped:
            rin_equ2.append(my_imped(w.side1))  # my_imped(n.side1))

        w.side1.connect(w.main_shaft(0.5))
        w.all = w.soma.wholetree()
        h.dt= pow(2,-5)
        gna_equ2.append(fullsolve_w(40))
    w.side1.disconnect()
    print(f"Control: gna equiv2 = {fullsolve_w(40)}")

    fig, ax = plt.subplots(nrows=2, ncols=1,figsize=(10,8))
    ax[0].plot(lengths,rin_equ2, label="Rin for eqi cell")
    ax[1].plot(lengths,gna_equ2, label="Gna for eqi cell")
    ax[0].grid()
    ax[1].grid()
    ax[1].legend()
    ax[0].legend()
    ax[1].set_xlabel("length in lambda")  # 'length of side branches in lambda'
    ax[0].set_ylabel("Rin in mV/nA")  # 'node along main shaft')
    ax[1].set_ylabel("Gna thresh")  # 'input resistance')
    ax[0].set_title(f"Rin vs Gna based on varying side branch lengths; {title}")
    plt.show()