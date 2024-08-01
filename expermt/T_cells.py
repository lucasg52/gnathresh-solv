from cells.rincell import Rin_Tcell, RinCell
from tools.Rin_funcs import new_run, save_data, plot_2d, plot_3d
from neuron import h
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

__MAXGBAR__ = 0.3
__tstop__ = h.tstop = 15
h.dt = pow(2,-6)

# m = RinCell(0)
t = Rin_Tcell(1)
t.setup_stim(0.5)
t.side1.L = 3 * elength(t.side1)
t._normalize()

# loc_lst = [i/100 for i in range(0, 100,10)]
len_lst = [i/100 for i in range(10, 610, 10)]
lab_lst = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] #'no',



def set_Tlens(len):
    if len == 0:
        t.side1.disconnect()
        t._normalize()

    else:
        t.dau1.L = len*elength(t.dau1)
        t._normalize()

def connect():
    t.side1.connect(t.main_shaft(0.6))