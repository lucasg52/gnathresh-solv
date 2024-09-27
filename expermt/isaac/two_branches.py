# from gnatsolv.cells.base import BaseExpCell
from gnatsolv.cells.tapertypes import BaseTaperCell
import matplotlib.pyplot as plt
from gnatsolv.cells.adoptedeq import elength
import gnatsolv.cells.adoptedeq as gnat
from neuron import h, units
from gnatsolv.solver.searchclasses import ExpandingSearch as ES, BinSearch
# from gnatsolv.cells.base import BaseExpCell
from aprecorder import APRecorder
from gnatsolv.cells import kinetics as kin
# import numpy as np
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
    dist_arr1 = []
    gna_arr = []
    dist_arr2 = []
    for seg1 in the_cell.main_shaft:
        arr2 = []
        dist_arr1.append(seg1.x * the_cell.main_shaft.L / elength(the_cell.main_shaft))
        the_cell.b1.connect(seg1)
        for seg2 in the_cell.main_shaft:
            the_cell.b2.connect(seg2)
            gna = fullsolve()
            print(gna)
            h.topology()
            arr2.append(gna)
            the_cell.b2.disconnect()
        the_cell.b1.disconnect()
        gna_arr.append(arr2)
    return dist_arr2, gna_arr#gna_arr2 is rectangular


class Cell(BaseTaperCell):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._setup_exp()
    pass
    def topo(self):
        self.parentb = h.Section('parentb', self)
        self.b1 = h.Section('b1',self)
        self.b2 = h.Section('b2', self)
        self.b1.diam = self.parentb.diam = self.b2.diam = self.prop_site.diam
        self.prop_site.connect(self.main_shaft(1))
        self.parentb.connect(self.main_shaft(0.2))
        self.b1.connect(self.main_shaft(0.5))
        self.b2.connect(self.main_shaft(0.75))
        for sec in self.all[1::]:
            kin.insmod_Traub(sec,"axon")

    def basegna(self):
        self.parentb.connect(self.main_shaft(0.2))
        self.b2.disconnect()
        self.b1.disconnect()
        return fullsolve()

    #import tapered IS and add repr function to class
#set up
dx = 0.1 #in terms of lambda, at most 2^-5,
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
    plt.xlabel("Distance of Side Branch from Soma")
    plt.ylabel("Gna") # convert to lambda
    plt.show()
    # print(the_cell.basegna())
    # get rid of notices by doing a disconnect statement before reconnecting

if __name__ == "__main__":
    main()