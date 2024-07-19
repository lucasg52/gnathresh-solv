from neuron import h
from gnatsolv.cells.tools import APRecorder
from ..cells.tapertypes import ExpCell_notaper
from ..solver import searchclasses
from ..solver.deathsolve import SegDeathSolver
import matplotlib.pyplot as plt
import numpy as np
print(plt)
h.load_file("stdrun.hoc")
h.dt = pow(2,-7)

m = ExpCell_notaper(0.2,3)
m.prop_site.L *= 3
m.prop_site.connect(m.main_shaft(0.3))
aprec = APRecorder(m.main_shaft, 0.9)
mystim = h.IClamp(m.prop_site(0.9))
mystim.delay = 3
mystim.amp = 200
mystim.dur = 5/16
mydeath = h.DeathRec(m.main_shaft(0.3))
m._setup_exp()
def ngui():
    from neuron import gui
    print(gui)
def setg(g):
    m.setgnabar(g)
    m.setgkbar(g)
def proptest(gnabar):
    aprec = m.aprecord
    m.setgnabar(gnabar)
    m.setgkbar(gnabar)
    #print(f"running ah test, gbar_na = {m.getgnabar()}")
    h.finitialize(-69)
    h.continuerun(30)
    ret = aprec.proptest() #NOT recursive, this is the call for the APRecorder to return the success/fail of the last test, and reset
    #print(ret)
    return (ret)
osearch = searchclasses.GNASearch(0, 0.05, proptest)
search = SegDeathSolver(0.29, 0.31, 0.3, m.main_shaft(0.3), setg, 10, -69)
#
#def fullsearch(x, steps):
#    search = searchclasses.GNASearch(0, 0.05, proptest)
#    m.prop_site.connect(m.main_shaft(x))
#    for i in range(steps):
#        print(search.a)
#        search.searchstep()
#    return search.a
#
#

def searchreset(a, err):
    global osearch
    hi = a + err
    lo = a - err
    osearch = searchclasses.GNASearch(lo, hi, proptest)

def fullsolve(steps = 12, a = 0.5, err = 0.5):
    searchreset(a, err)
    for i in range(steps):
            osearch.searchstep()
    return osearch.a

def gengraphdata(glo, ghi, n = 256):
    global g_gdata, g_tdata, g_fun
    assert glo < ghi
    g_gdata = np.linspace(glo, ghi, n)
    g_tdata = [g_fun(g) for g in g_gdata]

def genplot():
    plt.plot(g_gdata, g_tdata)
    plt.show()

