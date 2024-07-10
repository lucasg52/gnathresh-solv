from  neuron import h
from .adoptedeq import elength, normalize_dlambda
from .base import BaseExpCell
from . import kinetics as kin
from math import ulp as __ulp__

class LambdaSec():
    # bad idea for a class, will likely slow down all large scale experiments even if done correctly
    def __init__(self, *args, **kwargs):
        self.sec = h.Section(*args, **kwargs)
    def _get_L(self):
        return self.sec.L / elength(self.sec)
    def _set_L(self, newL):
        diffL = newL - self._get_L()


class SmartShaft():
    """unimplemented"""
    #give it a dx
    def __init__(self):
        self.shaftlist = []
    def measureto(self, dist):
        totaldist = dist
        for i, sec in enumerate(self.shaftlist):
            if totaldist - sec.L < 0:
                return i, sec, totaldist
            else:
                totaldist -= sec.L
        return None, None, None
    def split(self, sec, dist):
        #if dist == sec.L:
        #    return sec
        parent = sec.parentseg()
        new = h.Section()
        new.diam = sec.diam
        new.L = dist
        new.connect(parent)
        sec.connect(new(1)) 
        sec.L -= dist
        return new
    def merge(self,i):
        if isinstance(i, int):
            sec = self.shaftlist[i]
        else:
            sec = i
            i = self.shaftlist.index(sec)
        mergesec = self.shaftlist[i+1]
        children = sec.children()
        if len(children) > 1:
            print("gnatsolv.cells.smartbranch.SmartShaft: WARNING: removing section with connected branches")
        if mergesec not in children:
            print("gnatsolv.cells.smartbranch.SmartShaft: WARNING: shaft is not continuous during merge")
        parent = sec.parentseg()
        sec.disconnect()
        mergesec.L += sec.L
        mergesec.connect(parent)
        self.shaftlist.pop(i)
        h.delete_section(sec = sec)
        return mergesec

    def insert(self, dist):
        i, splitsec, splitdist = self.measureto(dist)
        if i is None:
            print("gnatsolv.cells.smartbranch.SmartShaft: WARNING: attempted to insert branch beyond total branch distance")
            return
        if splitdist <= 4 * __ulp__(splitsec.L):
            print(f"gnatsolv.cells.smartbranch.SmartShaft: WARNING: attempted to insert a branch very close to, or at already existing branchpoint: sec: {splitsec} dist: {splitdist}")
        newsec = self.split(splitsec, splitdist) 
        self.shaftlist.insert(i, newsec)
        return i, newsec

class SmartBranchCell(BaseExpCell):
    __doc__ = BaseExpCell.__doc__ + "\nunimplemented"
    def __init__(
            self,
            dx,
            ratio,
            gid = 0,
            layer = 0
            ):
        super().__init__(dx, ratio, gid = gid, layer = layer)
        self.shaftlist  = [self.main_shaft]
        self.shaft = SmartShaft()
        self.shaft.shaftlist = self.shaftlist
        self.branchcnt = 0
        self.branchlist = []
    def newbranch(self, L, dist, diam = None, new = None):
        if diam is None:
            diam = self.main_diam/self.ratio
        if new is None:
            new = h.Section(name = f"branch[{self.branchcnt}]", cell = self)
            kin.insmod_Traub(new        , "axon")
        self.branchcnt += 1
        new.L = L
        new.diam = diam
        self.branchlist.append(new)
        i ,parsec = self.shaft.insert(dist)
        new.connect(parsec(1))
        self.all = self.soma.wholetree()
        kin.insmod_Traub(parsec     , "axon")
        self._normalize() #needs to be removed
    def rmbranch(self, ind):
        if isinstance(ind,int):
            branch = self.branchlist[ind]
        else:
            branch = ind
            ind = self.branchlist.index(branch)
        parent = branch.parentseg().sec
        branch.disconnect()
        self.branchlist.pop(ind)
        self.shaft.merge(parent)
        
    def _setup_morph(self):
        super()._setup_morph()
        self.IS.diam = self.IS_diam

    def _connect(self):
        self.IS.connect(self.soma(1))
        self.main_shaft.connect(self.IS(1)) # (line 107)
        self.prop_site.connect(self.main_shaft(1)) 
    def _setup_bioph(self):
        kin.insmod_Traub(self.soma          , "soma")
        kin.insmod_Traub(self.IS            , "axon")
        kin.insmod_Traub(self.main_shaft    , "axon")
        kin.insmod_Traub(self.prop_site     , "axon")

    def _normalize(self): # line 166, not clear why some sections get normalized differently. so I am just assuming it is homogenous. also made my own subroutine 
        for sec in self.all:
            normalize_dlambda(sec, self.dx)

    def __repr__(self):
        return(f"SmartBranchCell[{self.gid}]")

