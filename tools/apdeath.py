from neuron import h
from .aprecorder import APRecorder
from .. import eq

class DeathTester(APRecorder):
    def __init__(
            self,
			tree,
			tstop,
			*args,
			interval = 3,
			threshold = -50,
			maxsteps = 100,
			sync_tstop = True,
			**kwargs):
        super().__init__(*args, **kwargs)
        self.tree = tree
        self.sync_tstop = sync_tstop
        self.tstop = tstop
        self.interval = interval
        self.threshold = threshold
        self.maxsteps = maxsteps
        self.dtime = self.dsteps = self.proptime = 0
        self._initnodes()
    def checkinterval(self):
        print("unimplemented")      # assert that none of the sections are too long for an AP to cross in interval
    def _initnodes(self):
        self.nodes = []
        for sec in self.tree:
            if sec.parentseg() is None:
                continue
            if sec.parentseg().sec in self.tree:
                self.nodes.append(h.DeathRec(sec(1)))
    def proptest(self):
        for i in range(self.maxsteps):
            superret = super().proptest()
            if not superret:
                if self.lifetest():             # we are still alive
                    h.continuerun(h.t + self.interval) 
                else:                           # not propogating and we dead a hell
                    self.deathtime = max(n.deatht for n in self.nodes)
                    break
            else:
                self.proptime = self.recorded[0]
                self.dsteps = 0
                return superret
        return 0

    proptest.__doc__ = APRecorder.proptest.__doc__ + "\nadditionally, continue running simulation until AP is dead"
    def calibrate(self):
        if self.dsteps:
            if self.dsteps >= 2:
                self.interval *= 2
            self.tstop = self.dtime + self.interval
        if self.proptime > self.tstop - self.interval:
            self.tstop  = self.proptime + self.interval
    def lifetest(self):
        """returns true if there are any nodes where the AP is still alive"""
        for n in self.nodes:
            #if n.v > self.threshold:
            if n.deatht == 0:
                return True
        return False

    def _set_tstop(self, val):
        if self.sync_tstop:
            h.tstop = self.__tstop = val
        else:
            self.__tstop = val
    def _get_tstop(self):
        return self.__tstop
    tstop = property(fget = _get_tstop, fset = _set_tstop, doc = \
            "the time that the simulation should run to if the other attributes are" 
            "calibrated correctly."
            "if sync_tstop is True then h.tstop will change alongside it")


class DeathWatcher:
    def __init__(
            self,
            recbegin, recend,
            tstop,                  # ms
            #recinterval = 0.25,     # lambda
            minapspeed = 1,         # lambda/ms (unused)
            tinterval  = 0.25,      # ms
            maxsteps   = 100        
            ):
        self.deathtime = None

        self._setup_nodes(recbegin, recend)
        self.tstop = tstop
        #self.recinterval = recinterval
        self.minapspeed =  minapspeed 
        self.tinterval  =  tinterval 
        self.maxsteps = maxsteps

    #def _setkwattr(self, defaults, kwargs):
    #    unexpected = kwargs.keys().difference(defaults.keys)
    #    if unexpected:
    #        raise TypeError(f"unexpected keyword args: {unexpected}")
    #    d = defaults.copy()
    #    d.update(kwargs)
    #    for name, v in d.items:
    #        setattr(self, name, v)
#
#    def _setup_nodes(self, begin, end, interval):
#        rangevarplot = h.RangeVarPlot("x", begin, end)
#        seclist = h.SectionList()
#        rangevarplot.list(seclist)
#        if len(list(seclist)) > 1:
#            print("DeathWatcher: ERROR: multiple-section paths not supported")
#            print(list(seclist))
#            raise NotImplementedError
#        self.nodes = []
#        sec = begin.sec
#        nseg = sec.nseg
#        segpernode = int(
#                interval
#                * eq.elength(sec)
#                * nseg 
#                / sec.L)
#        if segpernode == 0:
#            print("DeathWatcher: WARNING: recinterval too fine for section")
#            segpernode = 1
#        self.nodesegs = list(sec)[int(begin.x*nseg):int(end.x*nseg):segpernode]
#        self.nodesegs.append(end)
#        self.nodes = [h.DeathRec(s) for s in self.nodesegs]
#

    def _setup_nodes(self, begin, end):
        seclist = h.SectionList()
        rvp = h.RangeVarPlot("x", begin, end)
        rvp.list(seclist)
        self.nodes = []
        if begin.x == 0 and end.x == 1:
            map(self.nodes.extend, (sec.allseg() for sec in seclist))
            for s in seclist:
                s.insert("apdeath")
        else:
            h.RangeVarPlot(
                    lambda seg : self.nodes.append(seg),
                    begin, end
                    )
            for n in self.nodes: 
                n.insert("apdeath")

    def run(self):
        h.continuerun(self.tstop)
        i = self.maxsteps
        while i and self.prelifetest():
            i -=1 
            h.continuerun(h.t + self.tinterval)
        while i and self.lifetest():
            i -= 1
            h.continuerun(h.t + self.tinterval)
    def prelifetest(self):
        return all(
                    node.begin == 0 
                    for node in self.nodes
                )

    def lifetest(self):
        return not all(
                bool(node.begin) == bool(node.deatht)
                for node in self.nodes
                )
    def getdeathtime(self):
        self.deathtime = max(node.deatht for node in self.nodes)
        return self.deathtime


