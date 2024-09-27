from gnatsolv.cells.DCell import DCell
import matplotlib.pyplot as plt
from gnatsolv.cells.adoptedeq import elength
import gnatsolv.cells.adoptedeq as gnat
from neuron import h
from gnatsolv.solver.searchclasses import ExpandingSearch as ES, BinSearch
from aprecorder import APRecorder
from gnatsolv.cells import kinetics as kin
import numpy as np
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
    dist_arr3 = []
    the_cell.side[2].disconnect()
    for seg1 in the_cell.main_shaft:
        arr2 = []
        dist_arr1.append(seg1.x * the_cell.main_shaft.L / elength(the_cell.main_shaft))
        the_cell.side[1].connect(seg1)
        count = 0
        count += 1
        for d in the_cell.iter_dist(3):
            gna = fullsolve()
            print(gna)
            h.topology()
            arr2.append(gna)
            if count == 1:
              dist_arr3.append(d)
        the_cell.side[1].disconnect()
        gna_arr.append(arr2)
    return dist_arr1, dist_arr3, gna_arr#gna_arr2 is rectangular

class Cell(DCell):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # self.aprecord = APRecorder(self.main_shaft, ran=1)
        pass


    # def topo(self):
    #     self.parentb = h.Section('parentb', self)
    #     self.b1 = h.Section('b1',self)
    #     self.b3 = h.Section('b3', self)
    #     self.b1.diam = self.parentb.diam = self.b3.diam = self.prop_site.diam
    #     self.prop_site.connect(self.main_shaft(1))
    #     self.parentb.connect(self.main_shaft(0.2))
    #     self.b1.connect(self.main_shaft(0.6))
    #     self.b3.connect(self.parentb(0.75))
    #     for sec in self.all[1::]:
    #         kin.insmod_Traub(sec,"axon")

    #import tapered IS and add repr function to class
#set up
the_cell = DCell()
the_cell._setup_exp()
h.topology(the_cell)
myrec = APRecorder(the_cell.prop_site)
stim = h.IClamp(the_cell.parent(0.5))
stim.amp = 0.2 #nA
stim.delay = 5 #ms
stim.dur = 5/16 #ms

def main():
    # dist_arr1, dist_arr3, gna_arr = collect_gna()
    # print(gna_arr)
    # print(dist_arr1)
    # print(dist_arr3)
    # plt.plot(dist_arr1,gna_arr)
    # plt.xlabel("Distance of Side Branch from Soma")
    # plt.ylabel("Gna") # convert to lambda
    # plt.show()
    the_cell.parent.connect(the_cell.main_shaft(0.2))
    the_cell.side[1].disconnect()
    the_cell.side[2].disconnect()
    the_cell.side[3].disconnect()
    print(f"basegNa = {fullsolve()}")

if __name__ == "__main__":
    main()