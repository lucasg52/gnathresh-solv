from .aprecorder import APRecorder
from neuron import h

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


