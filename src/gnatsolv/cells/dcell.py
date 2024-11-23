from warnings import warn
from neuron import h
import numpy as np
from .. import eq
from . import kinetics as kin
from .tapertypes import BaseTaperCell

class DCell(BaseTaperCell):
    def __init__(self, **kwargs):
        super().__init__(pow(2,-5), 3, **kwargs)
        self.lmax = np.ones(4) * 4
    
    def __repr__(self):
        return(f"DCell[{self.gid}]")
    def _setup_bioph(self):
        for sec in [self.IS, self.main_shaft, self.prop_site]:
            kin.insmod_Traub(sec, "axon")
        for sec in self.side:
            kin.insmod_Traub(sec, "axon")
        kin.insmod_Traub(self.soma, "soma")

    def defaultparams(self):
        self.l = np.ones(4) * 4
        self.d = np.ones(4) * 0
        self.d[0] = 0.2
        self.parentdict = [self.main_shaft] * 3
        self.parentdict.append(self.parent)
    def _create_secs(self):
        self.parent=  h.Section(cell = self, name = 'parent') 
        self.side = [self.parent]
        self.side.extend(
                h.Section(cell = self, name = f"side[{n}]")
                for n in range(1,4)
                )
        self.defaultparams()

    def _setup_morph(self):
        self.main_length = 4
        self.soma.L = self.soma.diam = self.soma_diam
        self.IS.L = 40 # line 98
        self.main_shaft.L = self.main_length * eq.elength(self.main_shaft, d = self.main_diam)
        self.main_shaft.diam = self.main_diam
        self.prop_site.diam = self.main_diam
        self.prop_site.L = self.main_shaft.L
        self.IS.diam = self.IS_diam

        for n in range(4):
            self.side[n].diam = self.main_diam/self.ratio
        self._connect()
        self._normalize()
        self.update_dist(0)
        self.update_geom()


    def update_geom(self, dists = None, lengths = None):
        """
        Update the geometry of the cell completely (using information in d and l tables)
        Not recommended unless you are setting up an initial geometry before iteration, or 
        unless youre setting up a random geometry

        For a more confined update to either branch distances or lengths, one or both of the
        corresponding arguments can be specified as sets of branch ids to be updated
        """
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
        """
        Update the length of an individual side-branch such that side[n].L (in terms of
        lambda) is equal to l[n]. By default, the former will be set unless length is
        specified.
        That is, the information the table l is a fallback if arg 'length' is not provided 
        """
        if length is None:
            length = self.l[n]
        else:
            self.l[n] = length
        if length == 0:
            self.side[n].disconnect()
            length = self.dx/2  # make branch short to ensure lower memory footprint
        else:
            if self.side[n].parentseg() is None:
                self.side[n].connect(
                        self.parentdict[n]
                        (self.d[n])
                        )
        elength = eq.elength(self.parent, d = self.main_diam/self.ratio)
        self.side[n].L = length * elength
        eq.normalize_dlambda(self.side[n], dx = self.dx)

    def update_dist(self, n, dist = None):
        """
        Update the attachment point of an individual side-branch such that side[n] is attached
        at distance d[n]. By default, the former will be set unless dist is specified.
        That is, the information the table d is a fallback if arg 'dist' is not provided 
        """
        if dist is None:
            dist = self.d[n]
        if self.l[n] != 0:
            self.side[n].disconnect()
        else:
            if self.side[n].parentseg() is not None:
                warn(f"side[{n}] was attached despite having length zero", Warning)
                self.side[n].disconnect()
        self.side[n].connect(
                self.parentdict
                [n]
                (dist)
                )
        dist = self.side[n].parentseg().x
        if self.l[n] == 0:
            self.side[n].disconnect()
        self.d[n] = dist

    def iter_length(self, branchid, dxratio = 1, start = 0, end = None):
        if end is None:
            end = self.lmax[branchid]
        for length in np.linspace(
                start, end,
                int((end-start)/(dxratio*self.dx))
                ):
            self.update_length(branchid, length)
            yield length
    def iter_dist(self, branchid, nowarn = False):
        """
        iterates the attachment distance, i.e. d[branchid] of side[branchid] by attaching
        it to each segment that it can be attached to

        example usage:
        for x in my_cell.iter_dist(1):
            print(f"side branch 1 is now attached to {x}")
        """
        #if not isinstance(segperstep, int):
        #    raise TypeError
        zerolength = False
        if self.l[branchid] == 0:
            zerolength = True
            if not nowarn:
                warn(
                        "iterating branch distance for branch of 0 length."
                        +" specify nowarn=True to ignore",
                        Warning
                        )
            if self.side[branchid].nseg > 1:
                warn(f"side[{branchid}] is long despite having l[{branchid}] equal to zero."
                        + " preformance may suffer",
                        Warning)
        for seg in (
                list(
                    self.parentdict[branchid]
                    .allseg()
                    )
                [1:-1]
                ):
            self.side[branchid].disconnect()
            self.side[branchid].connect(seg)
            self.d[branchid] = seg.x
            if zerolength:
                self.side[branchid].disconnect()
            yield seg.x


    def getsegindex(self, sec, ran):  
        nseg = sec.nseg
        if ran == 1:
            ran = 0.9999
        return(int(ran*nseg))


