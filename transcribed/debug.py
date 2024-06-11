from templates_transcribe import Expcell_demo, h
from neuron.units import ms, mV
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')


m = Expcell_demo(2,3,1,1)
t = h.Vector().record(h._ref_t)


def setup_record():
    global somaV
    global axonV
    #global dendV
    somaV = h.Vector().record(m.soma(0.5)._ref_v)
    axonV = h.Vector().record(m.main_shaft(0.5)._ref_v)
    #dendV = h.Vector().record(m.dend(0.5)._ref_v)

def rerun():
    h.finitialize(-70 * mV)
    h.continuerun(50 * ms)

def replot():
    global ga    
    global gs       
    #global gd

    ga = plt.plot(t,axonV, label = "axonV")
    gs = plt.plot(t,somaV, label = "somaV")
    #gd = plt.plot(t,dendV,label = "dendV")
    plt.legend()

setup_record()               
#setup_stim(m.dend(1))   
rerun()
replot()
