from templates_transcribe import Expcell_demo, h
from neuron.units import ms, mV
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')


m = Expcell_demo(2,3,1,1)
t = h.Vector().record(h._ref_t)

recs = dict()
plots = dict()



recdict = { #make function for destroying keys
        "somaV " : (m.soma(0.5)      ,"_ref_v"),
        "axonV " : (m.main_shaft(0.8),"_ref_v"),
        "axonV2" : (m.main_shaft(0.5),"_ref_v"),
        "axonV3" : (m.main_shaft(0.2),"_ref_v"),
        "ISV   " : (m.IS(0.5)        ,"_ref_v")
}

for i in [0.1,0.4,0.7,1]:
    recdict["axon_m({})".format(i)] = (m.main_shaft(i),"_ref_m_nafTraub") 
    recdict["axon_h({})".format(i)] = (m.main_shaft(i),"_ref_h_nafTraub")
    recdict["axon_n({})".format(i)] = (m.main_shaft(i),"_ref_m_kdrTraub")


recs = dict()
plots = dict()

def setup_record():
    global recdict, recs 

    #global dendV
    for k in recdict:
        recs[k] = h.Vector().record(
                getattr(*(recdict[k]))
                )



    #dendV = h.Vector().record(m.dend(0.5)._ref_v)

def rerun(initialv  = -69.7 * mV, runtime = 50 * ms):
    h.finitialize(-69.7 * mV)
    h.continuerun(50 * ms)

def replot():
    global plots, recs 
    for k in recs:
        plots[k] = plt.plot(t, recs[k], label = k)

    #plots.update({"ga" : plt.plot(t,recs["axonV"], label = "axonV")})
    #plots.update({"gs" : plt.plot(t,recs["somaV"], label = "somaV")})
    #plots.update({"g"  : plt.plot(t,recs["ISV"], label = "ISV")})
    #plots.update({#gd : plt.plot(t,dendV,label = "dendV")
    plt.legend()

setup_record()
#setup_stim(m.dend(1))   
rerun()
replot()

def reall():
    setup_record()
    rerun()
    replot()
