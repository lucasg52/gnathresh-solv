from neuron import h
import numpy as np
from .. import eq
from .tapertypes import BaseTaperCell

class DCell(BaseTaperCell):
    #class ModList(list):
    #    def __setnotify(self,f):
    #        self.__notify = f
    #    def __getitem__(self, item, *args, **kwargs):
    #        if isinstance(item, int):
    #            self.__notify(item)
    #        else:
    #            self.__notify(None)
    #        return super().__getitem__(item, *args, **kwargs)
    def __init__(self, **kwargs):
        super().__init__(pow(2,-5), 3, **kwargs)
        self.main_length = 4
        self.lmax = np.ones(4) * 4
        self.defaultparams()
    def defaultparams(self):
        self.l = np.ones(4) * 4
        self.d = np.ones(4) * 0
        self.d[0] = 0.2
    def _create_secs(self):
        self.parent=  h.Section(cell = self, name = 'parent') 
        self.side = [self.parent]
        self.side.extend(
                h.Section(cell = self, name = f"side[{n}]")
                for n in range(1,4)
                )

    def _setup_morph(self):
        self.soma.L = self.soma.diam = self.soma_diam
        self.IS.L = 40 # line 98
        self.main_shaft.L = self.main_length * eq.elength(self.main_shaft, d = self.main_diam)
        self.main_shaft.diam = self.main_diam
        self.prop_site.diam = self.main_diam

        for n in range(4):
            self.side[n].diam = self.main_diam/self.ratio
        self.update_geom()

        self._connect()      
        self._normalize()

    def update_geom(self, dists = None, lengths = None):
        if dists is None and lengths is None:
            dists = lengths = range(4)
        elif dists is None:
            dists = []
        elif lengths is None:
            lengths = []
        if isinstance(dists, int):
            dists = [dists]
        if isinstance(lengths, int):
            lengths = [lengths]
        for n in dists:
            self.update_dist(n, self.d[n])
        for n in lengths:
            self.update_length(n)

    def update_length(self, n, length = None):
        if length is None:
            length = self.l[n]
        else:
            self.l[n] = length
        elength = eq.elength(self.parent, d = self.main_diam/self.ratio)
        self.side[n].L = length * elength

    def update_dist(self, n, dist = None):
        if dist is None:
            dist = self.d[n]
        if self.l[n] != 0:
            self.side[n].connect(
                    self.side[n]
                    .parentseg()
                    .sec(dist)
                    )
            dist = self.side[n].parentseg().x
        else:
            assert self.side[n].parentseg() is None

            dist = self.side[n].parentseg().x
        self.d[n] = dist

    def iterlength(self, branchid, dxratio = 1, start = 0, end = None):
        if end is None:
            end = self.lmax[branchid]
        for length in np.linspace(
                start, end,
                (end-start)/(dxratio*self.dx)
                ):
            self.updatelength(branchid, length)


    def getsegindex(self, sec, ran):  
        nseg = sec.nseg
        if ran == 1:
            ran = 0.9999
        return(int(ran*nseg))


