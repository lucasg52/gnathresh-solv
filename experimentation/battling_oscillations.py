from gnatsolv.transcribed.celltemplates import *
import matplotlib.pyplot as plt
h.load_file("stdrun.hoc")

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
prop_v00625 = h.Vector().record(m.prop_site(0.0625)._ref_v)
main_v1 = h.Vector().record(m.main_shaft(1)._ref_v)
main_v0 = h.Vector().record(m.main_shaft(0)._ref_v)
IS_v05 = h.Vector().record(m.IS(0.5)._ref_v)
IS_v1 = h.Vector().record(m.IS(1)._ref_v)
soma_v0 = h.Vector().record(m.soma(0)._ref_v)

#getting spike times
nc_prop = h.NetCon(m.prop_site(0)._ref_v, None, sec=m.prop_site)
st_prop = h.Vector()
nc_prop.record(st_prop)

nc_prop2 = h.NetCon(m.prop_site(0.0625)._ref_v, None, sec=m.prop_site)
st_prop2 = h.Vector()
nc_prop2.record(st_prop2)

nc_main = h.NetCon(m.main_shaft(1)._ref_v, None, sec=m.main_shaft)
st_main = h.Vector()
nc_main.record(st_main)

nc_main2 = h.NetCon(m.main_shaft(0)._ref_v, None, sec=m.main_shaft)
st_main2 = h.Vector()
nc_main2.record(st_main2)

nc_IS = h.NetCon(m.IS(0.5)._ref_v, None, sec=m.IS)
st_IS = h.Vector()
nc_IS.record(st_IS)

nc_IS2 = h.NetCon(m.IS(1)._ref_v, None, sec=m.IS)
st_IS2 = h.Vector()
nc_IS2.record(st_IS2)

nc_soma = h.NetCon(m.soma(0)._ref_v, None, sec=m.soma)
st_soma = h.Vector()
nc_soma.record(st_soma)


#running the simulations
h.finitialize(-65)
h.continuerun(20)

#spikes
print(f"number of spikes at prop 0: {len(list(st_prop))}")
#print(f"spike times prop 0: {list(st_prop)}")

print(f"number of spikes at porp 0.0625: {len(list(st_prop2))}")
#print(f"spike times prop 0.0625: {list(st_prop2)}")

print(f"number of spikes at main 1: {len(list(st_main))}")
#print(f"spike times main 1: {list(st_main)}")

print(f"number of spikes at main 0: {len(list(st_main2))}")
#print(f"spike times main 0: {list(st_main2)}")

print(f"number of spikes at IS 0.5: {len(list(st_IS))}")
#print(f"spike times IS 0.5: {list(st_IS)}")

print(f"number of spikes at IS 1: {len(list(st_IS2))}")
#print(f"spike times IS 1: {list(st_IS2)}")

print(f"number of spikes at soma 0: {len(list(st_soma))}")
#print(f"spike times soma 0: {list(st_soma)}")

#plotting
plt.plot(t,prop_v0,label="prop 0")
plt.plot(t, prop_v00625, label = "prop 0.0625")
plt.plot(t,main_v1,label="main 1")
plt.plot(t,main_v0,label="main 0")
plt.plot(t,IS_v1,label="IS 1")
plt.plot(t,soma_v0,label="soma 0")
plt.legend()
plt.grid()
plt.show()
