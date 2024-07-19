# from gnatsolv.cells.base import BaseExpCell
from gnatsolv.cells.tapertypes import ExpCell_notaper
import matplotlib.pyplot as plt
from gnatsolv.cells.adoptedeq import elength
import gnatsolv.cells.adoptedeq as gnat
from neuron import h, units
from gnatsolv.solver.searchclasses import ExpandingSearch as ES, BinSearch
# from gnatsolv.cells.base import BaseExpCell
#from aprecorder import APRecorder
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

def fullsolve():
    search = BinSearch(low,high, propatest=prop_test)
    for i in range(12):
        search.searchstep()
    return search.a

def set_ELen(section, length, dx):
    Lambda = elength(section)
    section.L = length * Lambda
    gnat.normalize_dlambda(section, dx)
    return
    #   print(Lambda)

def collect_gna():
    lst = []
    gna = fullsolve()
    for seg in the_cell.main_shaft:
        the_cell.prop_site.connect(seg)
        gna = fullsolve()
        lst.append(gna)
    return lst


class Cell(ExpCell_notaper):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._setup_exp()
    pass

dx = 0.1
ratio = 3
the_cell = Cell(dx,ratio)
set_ELen(the_cell.main_shaft, 4, dx)
set_ELen(the_cell.prop_site, 4, dx)
h.topology(the_cell)
stim = h.IClamp(the_cell.prop_site(0.5))
stim.amp = 200 #nA
stim.delay = 5 #ms
stim.dur = 5/16 #ms
lst_of_gnat = collect_gna()

node_lst = [i for i in range(0,the_cell.main_shaft.nseg)]
plt.plot(node_lst, lst_of_gnat)
plt.xlabel("Segment connected along main shaft")
plt.ylabel("GNA Threshold due to distance from propagation site")
plt.show()
