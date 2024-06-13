from templates_transcribe import Expcell_demo, h
from neuron.units import ms, mV
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')


m = Expcell_demo(2,3,1,1)
t = h.Vector().record(h._ref_t)

recs = dict()
plots = dict()

def set_recvec(seg, attr):


originalrecs = {
        "somaV " : (m.soma(0.5)      ,"ref_v"),
        "axonV " : (m.main_shaft(0.8),"ref_v"),
        "axonV2" : (m.main_shaft(0.5),"ref_v"),
        "axonV3" : (m.main_shaft(0.2),"ref_v"),
        "ISV   " : (m.IS(0.5)        ,"ref_v")
    }

def setup_record():
    global recs 

    #global dendV
    recs.update({
        "somaV " : h.Vector().record(m.soma(0.5)._ref_v),
        "axonV " : h.Vector().record(m.main_shaft(0.8)._ref_v),
        "axonV2" : h.Vector().record(m.main_shaft(0.5)._ref_v),
        "axonV3" : h.Vector().record(m.main_shaft(0.2)._ref_v),
        "ISV   " : h.Vector().record(m.IS(0.5)._ref_v)
    })
    #dendV = h.Vector().record(m.dend(0.5)._ref_v)

def rerun():
    h.finitialize(-69.7 * mV)
    h.continuerun(50 * ms)

def replot():
    global plots, recs 
    #global gd

    plots.update({"ga" : plt.plot(t,recs["axonV"], label = "axonV")})
    plots.update({"gs" : plt.plot(t,recs["somaV"], label = "somaV")})
    plots.update({"g"  : plt.plot(t,recs["ISV"], label = "ISV")})
    #plots.update({#gd : plt.plot(t,dendV,label = "dendV")
    plt.legend()

setup_record()
#setup_stim(m.dend(1))   
rerun()
replot()
