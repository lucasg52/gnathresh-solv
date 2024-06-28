from gnatsolv.transcribed.celltemplates import *
import matplotlib.pyplot as plt

#making the cell
m = ExpCell_notaper(0.2,3)

#making cell geometry adjustments
m.prop_site.connect(m.main_shaft(0.012))
m.IS.diam = 3

#creating a stimulation
stim = h.IClamp(m.prop_site(1))
stim.delay = 2
stim.dur = 0.2375
stim.amp = 0.015

#creating recordering vectors
t = h.Vector().record(h._ref_t)
prop_v0 = h.Vector().record(m.prop_site(0)._ref_v)
main_v1 = h.Vector().record(m.main_shaft(1)._ref_v)
IS_v05 = h.Vector().record(m.IS(0.5)._ref_v)
soma_v0 = h.Vector().record(m.soma(0)._ref_v)

#plotting
plt.plot(t,prop_v0,label="prop 0")
plt.plot(t,main_v1,label="main 1")
plt.plot(t,IS_v05,label="IS 0.5")
plt.plot(t,soma_v0,label="soma 0")
plt.legend()
plt.show()
