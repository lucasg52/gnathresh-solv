from expermt.Laura.Rin_cells2 import Rin_cell_1, Rin_cell_1y, setting_lengths, imped, my_imped
from solver.searchclasses import BinSearch
from tools.aprecorder import APRecorder
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from neuron import h
h.load_file("stdrun.hoc")
def ngui():
    from neuron import gui
    # print(gui)

m = Rin_cell_1(0)
n = Rin_cell_1y(1)

rec1 = APRecorder(m.prop_site)
rec2 = APRecorder(n.prop_site)

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

def fullsolve_m(steps = 30):
    search = BinSearch(0, 0.45, proptest_m)
    h.tstop = 10
    for i in range(steps):
            search.searchstep()
            if rec1.proptest():
                if rec1.recorded[0]>h.tstop/2:
                    h.tstop += 3
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

def fullsolve_n(steps = 30):
    search = BinSearch(0, 0.45, proptest_n)
    h.tstop = 10
    for i in range(steps):
            search.searchstep()
            if rec2.proptest():
                    if rec2.recorded[0]>h.tstop/2:
                        h.tstop += 3
    return search.a

def set_ELen(section, length, dx):
	Lambda = elength(section)
	section.L = length * Lambda
	gnat.normalize_dlambda(section, dx)

def setting_length(stim_len, dau_len, m=m, n=n):
	m.stim_b.L = stim_len*elength(m.stim_b)
	n.stim_b.L = stim_len*elength(n.stim_b)

	m.side1.L = dau_len*elength(m.side1)
	n.side1.L = dau_len*elength(n.side1)

	n.dau1.L = dau_len*elength(n.dau1)
	n.dau2.L = dau_len*elength(n.dau2)

stim = h.IClamp(m.stim_b(1))
stim.amp = 200
stim.delay = 5
stim.dur = 5/16

stim2 = h.IClamp(n.stim_b(1))
stim2.amp = 200
stim2.delay = 5
stim2.dur = 5/16

h.dt = pow(2,-5)

def run(stim_len, dau_len):
    setting_length(stim_len,dau_len)
    m.all = m.soma.wholetree()
    n.all = n.soma.wholetree()
    m._normalize()
    n._normalize()
    m.side1.disconnect()
    n.side1.disconnect()
    print(f"base cell: R_in = {my_imped(m.side1(0))}")
    print(f"equiv: R_in = {my_imped(n.side1(0))}")
    m.side1.connect(m.main_shaft(0.5))
    n.side1.connect(n.main_shaft(0.5))
    m.all = m.soma.wholetree()
    n.all = n.soma.wholetree()
    print(f"base cell: gna = {fullsolve_m(53)}")
    print(f"equiv: gna = {fullsolve_n(53)}")