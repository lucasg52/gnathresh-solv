from expermt.Laura.Rin_cells2 import Rin_cell_1, Rin_cell_1y
from solver.searchclasses import BinSearch
from tools.aprecorder import APRecorder
from cells.adoptedeq import elength
import cells.adoptedeq as gnat
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
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
    if dau_len>0.1 and dau_len<2.07:
        n.side1.L = (dau_len-0.09)*elength(n.side1)
        n.dau1.L = (dau_len-0.09)*elength(n.dau1)
        n.dau2.L = (dau_len-0.09)*elength(n.dau2)
    else:
        n.side1.L = dau_len * elength(n.side1)
        n.dau1.L = dau_len * elength(n.dau1)
        n.dau2.L = dau_len * elength(n.dau2)


# def setting_length(stim_len, dau_len, m=m, n=n):
# 	m.stim_b.L = stim_len*elength(m.stim_b)
# 	n.stim_b.L = stim_len*elength(n.stim_b)
#
# 	m.side1.L = dau_len*elength(m.side1)
#
# 	n.side1.L = dau_len*elength(n.side1)
#
# 	n.dau1.L = dau_len*elength(n.dau1)
# 	n.dau2.L = dau_len*elength(n.dau2)
#     if 0.12<n.side1.L/118<2.02:
#         n.side1.L = (dau_len +0.1) * elength(n.side1)
#         n.dau1.L = (dau_len +0.1) * elength(n.dau1)
#         n.dau2.L = (dau_len +0.1) * elength(n.dau2)
stim = h.IClamp(m.stim_b(1))
stim.amp = 200
stim.delay = 5
stim.dur = 5/16

stim2 = h.IClamp(n.stim_b(1))
stim2.amp = 200
stim2.delay = 5
stim2.dur = 5/16

h.dt = pow(2,-5)

rin_base = []
rin_eqi = []
gna_base = []
gna_eqi = []
diff_list = []
lengths = [j/100 for j in range(5,400,5)]#np.linspace(0.05, 2, 0.05)

def reset():
    rin_base = []
    rin_eqi = []
    gna_base = []
    gna_eqi = []
    diff_list = []

def Rin(part):
	imp_geter = h.Impedance()
	imp_geter.loc(part(0))
	imp_geter.compute(1)
	return imp_geter.input(part(0))

def my_imped(part):
    h.dt = 0.5
    if part == m.side1:
        m.side1.gbar_nafTraub = 0
        m.side1.gbar_kdrTraub =0
    if part == n.side1:
        n.side1.gbar_nafTraub = 0
        n.side1.gbar_kdrTraub =0
        n.dau1.gbar_nafTraub = 0
        n.dau1.gbar_kdrTraub =0
        n.dau2.gbar_nafTraub = 0
        n.dau2.gbar_kdrTraub =0
    stim = h.IClamp(part(0))
    stim.amp = 200
    stim.dur = 100
    stim.delay = 5
    h.finitialize(-70)
    h.continuerun(100)
    stim.amp=0
    return part(0).v / 200
    
def run(stim_len, dau_len, rin_solver, title):
    lengths = [j / 100 for j in range(5, 405, 5)]  # np.linspace(0.05, 2, 0.05)
    for i in lengths:
        setting_length(stim_len,i)
        m.all = m.soma.wholetree()
        n.all = n.soma.wholetree()
        m._normalize()
        n._normalize()
        m.side1.disconnect()
        n.side1.disconnect()
        # print(f"base cell: R_in = {my_imped(m.side1(0))}")
        print(m.side1.L/118.1, n.side1.L/118.1)
        if rin_solver == Rin:
            rin_base.append(Rin(m.side1))#my_imped(m.side1))
        # print(f"equiv: R_in = {my_imped(n.side1(0))}")
            rin_eqi.append(Rin(n.side1))#my_imped(n.side1))
            diff_list.append(Rin(m.side1)-(Rin(n.side1)))
        if rin_solver == my_imped:
            rin_base.append(my_imped(m.side1))  # my_imped(m.side1))
            # print(f"equiv: R_in = {my_imped(n.side1(0))}")
            rin_eqi.append(my_imped(n.side1))  # my_imped(n.side1))

        m.side1.connect(m.main_shaft(0.5))
        n.side1.connect(n.main_shaft(0.5))
        m.all = m.soma.wholetree()
        n.all = n.soma.wholetree()
        h.dt= pow(2,-5)
        # print(f"base cell: gna = {fullsolve_m(53)}")
        gna_base.append(fullsolve_m(40))
        # print(f"equiv: gna = {fullsolve_n(53)}")
        gna_eqi.append(fullsolve_n(40))
    m.side1.disconnect()
    n.side1.disconnect()
    print(f"Control: gna base = {fullsolve_m(40)}")
    print(f"Control: gna equiv = {fullsolve_n(40)}")


    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))
    # ax = fig.add_subplot(projection='3d')
    # x = [i/10 for i in range(0, dau_len*10, 1)]
    # x0 = np.meshgrid(x,x)
    # x_base, y_base = np.meshgrid(x, rin_base)
    # z_base = np.meshgrid(x, gna_base)
    # ax.plot_surface(x_base, y_base, z_base, alpha=0.5, cmap=cmap.viridis, label='base call')
    # ax.plot_surface(x, rin_eqi, gna_eqi, alpha=0.5, cmap=cmap.rdpu, label = "equiv cell")
    # ax.set_xlabel("length in lambda")  # 'length of side branches in lambda'
    # ax.set_ylabel("Rin in mV/nA")  # 'node along main shaft')
    # ax.set_zlabel("Gna thresh")  # 'input resistance')
    # ax.set_title("Rin vs Gna based on varying side branch lengths")
    # ax.legend()
    fig, ax = plt.subplots(nrows=3, ncols=1,figsize=(10,8))
    ax[0].plot(lengths,rin_base, label="Rin for base cell")
    ax[0].plot(lengths,rin_eqi, label="Rin for eqi cell")
    ax[1].plot(lengths,gna_base, label=f"Gna for base cell; control")
    ax[1].plot(lengths,gna_eqi, label="Gna for eqi cell")
    # ax[2].plot(rin_base, gna_base, label="Rin vs Gna for base cell")
    # ax[2].plot(rin_eqi, gna_eqi, label="Rin vs Gna for equi cell")
    ax[2].plot(lengths,diff_list)
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    ax[2].legend()
    ax[1].legend()
    ax[0].legend()
    ax[1].set_xlabel("length in lambda")  # 'length of side branches in lambda'
    ax[0].set_ylabel("Rin in mV/nA")  # 'node along main shaft')
    ax[1].set_ylabel("Gna thresh")  # 'input resistance')
    ax[2].set_ylabel("Gna")
    ax[2].set_xlabel("Rin")
    ax[0].set_title(f"Rin vs Gna based on varying side branch lengths; {title}")
    plt.show()