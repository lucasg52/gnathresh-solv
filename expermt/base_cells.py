import numpy as np
from cells.rincell import RinCell
from tools.Rin_funcs import new_run, plot_3d, plot_2d, save_data
from tools.environment import DeathEnviro
from tools.apdeath import DeathRec
from neuron import h
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

# __MAXGBAR__ = 0.3
# __tstop__ = h.tstop = 15
h.dt = pow(2,-6)


# m = RinCell(0)
b = RinCell(1)
b.setup_stim(0.5)
b.side1.L = 3 * elength(b.side1)
b._normalize()

deathrec = DeathRec(b.main_shaft, b.main_shaft, 6)
e = DeathEnviro(b, deathrec, b.stim)

# loc_lst = [i/100 for i in range(0, 100,10)]
len_lst = [i/100 for i in range(10, 610, 10)]
lab_lst = [0, 0.05, 0.1, 0.15, 0.2, 0.25,0.3,0.35,0.4,0.45,0.5]

def set_Blens(len):
    if len == 0:
        b.side1.disconnect()
        b._normalize()

    else:
        b.side1.L = len*elength(b.side1)
        b._normalize()

def connect():
    b.side1.connect(b.main_shaft(0.6))