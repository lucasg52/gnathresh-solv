from neuron import h
#from gnatsolv.cells.tools import APRecorder
from ..cells.tapertypes import ExpCell_notaper
from ..solver import searchclasses
import matplotlib.pyplot as plt
h.load_file("stdrun.hoc")
m = ExpCell_notaper(0.2,3)
m.prop_site.connect(m.main_shaft(0.3))
#aprec = APRecorder(m.main_shaft, 0.9)
mystim = h.IClamp(m.prop_site(0.9))
mystim.delay = 3
mystim.amp = 200
mystim.dur = 5/16
m._setup_exp()
def proptest(gnabar):
    aprec = m.aprecord
    m.setgnabar(gnabar)
    m.setgkbar(gnabar)
    #print(f"running ah test, gbar_na = {m.getgnabar()}")
    h.finitialize(-69)
    h.continuerun(10)
    ret = aprec.proptest() #NOT recursive, this is the call for the APRecorder to return the success/fail of the last test, and reset
    #print(ret)
    return (ret)
search = searchclasses.GNASearch(0, 0.05, proptest)
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
    global search
    hi = a + err
    lo = a - err
    search = searchclasses.GNASearch(lo, hi, proptest)

def fullsolve(steps = 12, a = 0.5, err = 0.5):
    searchreset(a, err)
    for i in range(steps):
            search.searchstep()
    return search.a


results = []
xpnts = []
ypnts = []
def fullexperiment():
    global xpnts, ypnts
    for i, seg in enumerate(m.main_shaft):
        plate = [seg.x]
        m.prop_site.disconnect()
        m.prop_site.connect(seg)
        plate.append(fullsolve(15, pow(2,-5), pow(2,-6)))
        results.append(tuple(plate))

    xpnts = [x for x,y in results]
    ypnts= [y for x,y in results]

fullexperiment()
plt.plot(xpnts,ypnts)

