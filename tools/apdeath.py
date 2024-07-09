from .aprecorder import APRecorder
from neuron import h
class DeathTester(APRecorder):
    def __init__(self, tree, timeout, tinterval = 1, threshold = -50, maxsteps = 100):
        self.tree = tree
        self.timeout = timeout
        self.tinterval = tinterval
        self.threshold = threshold
        self._initnodes()
    def _initnodes(self):
        self.nodes = []
        for sec in self.tree:
            if sec.parentseg().sec in self.tree:
                self.nodes.append(sec(1))
    def proptest(self):
        for i in range(self.maxsteps):
            superret = super().proptest()
            if not superret:
                if self.lifetest():
                    h.continuerun(self.interval) # we are still alive
                else:       # not propogating and we dead a hell
                    break
            else:
                self.proptime = self.recorded[0]
                return superret
        return 0
    def lifetest(self):
        """returns true if there are any nodes where the AP is still alive"""
        for n in self.nodes:
            if n.v > self.threshold:
                return True
        return False
