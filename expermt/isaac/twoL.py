from gnatsolv.cells.tapertypes import BaseTaperCell
import matplotlib.pyplot as plt
from gnatsolv.cells.adoptedeq import elength
import gnatsolv.cells.adoptedeq as gnat
from neuron import h, units
from gnatsolv.solver.searchclasses import ExpandingSearch as ES, BinSearch
# from gnatsolv.cells.base import BaseExpCell
from aprecorder import APRecorder
from gnatsolv.cells import kinetics as kin
h.load_file("stdrun.hoc")
#globals
low = 0
high = 0.45


def set_sec_gbar(sec, gbar):
    try:
        # sec.gbar_nafTraub = gbar
        sec.nafTraub.gbar = gbar
        sec.kdrTraub.gbar = gbar
    except ValueError:
        pass


def prop_test(gna):
    the_cell.setgnabar(gna)
    h.finitialize(-69)
    h.continuerun(15)
    return the_cell.aprecord.proptest()

def fullsolve(steps=12):
    search = BinSearch(low,high, propatest=prop_test)
    for i in range(steps):
        search.searchstep()
    return search.a

def set_ELen(section, length, dx):
    Lambda = elength(section)
    section.L = length * Lambda
    gnat.normalize_dlambda(section, dx)
    return
    #   print(Lambda)

def collect_gna():
    len_lst = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0]
    gna_arr = []
    for l in len_lst:
        arr = []
        set_ELen(the_cell.b1, l, dx)
        # for l in len_lst:
            # set_ELen(the_cell.b2, l, dx)
            # gna = fullsolve()
            # print(gna)
            # h.topology()
            # arr.append(gna)
        gna_arr.append(fullsolve())
    return len_lst, gna_arr#gna_arr is rectangular


class Cell(BaseTaperCell):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._setup_exp()
    pass
    def topo(self):
        self.parentb = h.Section('parentb', self)
        self.b1 = h.Section('b1',self)
        self.b2 = h.Section('b2', self)
        # self.b3 = h.Section('b3', self)
        self.b1.diam = self.parentb.diam = self.b2.diam = self.prop_site.diam
        self.prop_site.connect(self.main_shaft(1))
        self.parentb.connect(self.main_shaft(0.2))
        self.b1.connect(self.main_shaft(0.2))
        self.b2.connect(self.main_shaft(0.2))
        # self.b3.connect(self.parentb(0.75))
        for sec in self.all[1::]:
            kin.insmod_Traub(sec,"axon")

    def basegna(self):
        self.parentb.connect(self.main_shaft(0.2))
        self.b2.disconnect()
        self.b1.disconnect()
        # self.b3.disconnect()
        return fullsolve()

    #import tapered IS and add repr function to class
#set up
dx = 0.05 #in terms of lambda, at most 2^-5,
ratio = 3
the_cell = Cell(dx,ratio)
the_cell.topo()
set_ELen(the_cell.main_shaft, 4, dx)
set_ELen(the_cell.prop_site, 4, dx)
set_ELen(the_cell.parentb,4,dx)
set_ELen(the_cell.b1, 4, dx)
set_ELen(the_cell.b2,4,dx)
h.topology(the_cell)
myrec = APRecorder(the_cell.prop_site)
stim = h.IClamp(the_cell.parentb(0.5))
stim.amp = 0.2 #nA
stim.delay = 5 #ms
stim.dur = 5/16 #ms
# make them global??

#why use code
#why does the gnathresh matter
#for the poster^^^^^^^


def main():
    dist_arr, gna_arr = collect_gna()
    print(gna_arr)
    print(dist_arr)
    plt.plot(dist_arr,gna_arr)
    plt.xlabel("Length of Side Branch")
    plt.ylabel("Gna") # convert to lambda
    plt.show()
    print(f"basegna = {the_cell.basegna()}")
    # h.topology()
if __name__ == "__main__":
    main()