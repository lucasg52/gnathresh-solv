from .aprecorder import APRecorder
from neuron import h
class DeathTester:
    def __init__(self, tree, timeout, tinterval = 1):
        self.tree = tree
        self.timeout = timeout
        self.tinterval = tinterval
        self._initnodes()
    def _initnodes(self):
        self.nodes = []
        for sec in self.tree:
            if sec.parentseg().sec in self.tree:
                self.nodes.append(sec(1))
    
