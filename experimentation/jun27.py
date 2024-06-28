from neuron import h
from gnatsolv.transcribed.celltemplates import APRecorder, ExpCell_notaper
from gnatsolv.solver_groundwork import searchclasses
h.load_file("stdrun.hoc")
m = ExpCell_notaper(0.2,3)
m.prop_site.connect(m.main_shaft(0.3))
aprec = APRecorder(m.main_shaft, 0.9)
mystim = h.IClamp(m.prop_site(0.9))
mystim.delay = 3
mystim.amp = 200
mystim.dur = 5/16
def proptest(gnabar):
    print(f"running ah test, gbar_na = {m.getgnabar()}")
    m.setgnabar(gnabar)
    h.finitialize()
    h.continuerun(10)
    ret = aprec.proptest()
    print(ret)
    return (ret)
search = searchclasses.ExpandingSearch(0.05, 0.5, proptest, 0, 5)

