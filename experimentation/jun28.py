from neuron import h
from gnatsolv.transcribed.celltemplates import APRecorder, ExpCell_notaper
from gnatsolv.solver import searchclasses
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
    h.finitialize(-68.5)
    h.continuerun(10)
    ret = aprec.proptest()
    print(ret)
    return (ret)
search = searchclasses.GNASearch(0, 0.05, proptest)

def fullsearch(x, steps):
    search = searchclasses.GNASearch(0, 0.05, proptest)
    m.prop_site.connect(m.main_shaft(x))
    for i in range(steps):
        print(search.a)
        search.searchstep()
    return search.a



