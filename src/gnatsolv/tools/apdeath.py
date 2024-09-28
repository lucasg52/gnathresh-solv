import time
from neuron import h
from .aprecorder import APRecorder
from .oldapdeath import DeathTester
#from .. import eq
class DeathRec:
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
        self.aprec = APRecorder(recend, 1)
        self.proptest = self.aprec.proptest
        self.tstop = tstop
        #self.recinterval = recinterval
        self.minapspeed =  minapspeed 
        self.tinterval  =  tinterval 
        self.maxsteps = maxsteps



    def _setup_nodes(self, begin, end):
        beginseg = begin(0)
        endseg = end(1)
        seclist = h.SectionList()
        rvp = h.RangeVarPlot("x", beginseg, endseg)
        rvp.list(seclist)
        for s in seclist:
            s.insert("apdeath")
        self.deathrvp = h.RangeVarPlot("deatht_apdeath", beginseg, endseg)
        self.beginrvp = h.RangeVarPlot("begin_apdeath", beginseg, endseg)
        self.deathvec = h.Vector()
        self.beginvec = h.Vector()
        #else:
        #    print (self.nodes)
        #    h.RangeVarPlot(
        #            lambda segx : self.nodes.append(h.cas()(segx)),
        #            beginseg, endseg
        #            )
        #    print (self.nodes)
        #    for n in self.nodes: 
        #        n.insert("apdeath")

    def run(self):
        h.continuerun(self.tstop)
        i = self.maxsteps
        while i and self.prelifetest():
            i -=1 
            h.continuerun(h.t + self.tinterval)
        while i and self.lifetest():
            i -= 1
            h.continuerun(h.t + self.tinterval)
        if i == 0:
            print(f"DeathRec: WARNING: did not detect cell stimulation between t = {self.tstop} and t = {h.t}")
            print(self.lifetest())
    def prelifetest(self):
        #return all(
        #            node.begin_apdeath == 0 
        #            for node in self.nodes
        #        )
        #return h.flagbegin_apdeath == 0
        self.beginrvp.to_vector(self.beginvec)
        return self.beginvec.max() == 0

    def lifetest(self):
        #return not all(
        #        bool(node.begin_apdeath) == bool(node.deatht_apdeath)
        #        for node in self.nodes
        #        )
        self.beginrvp.to_vector(self.beginvec)
        self.deathrvp.to_vector(self.deathvec)
        return (self.beginvec.sub(self.deathvec)).max() > 0
    def getdeathtime(self):
        self.deathrvp.to_vector(self.deathvec)
        self.deathtime = self.deathvec.max() 
        return self.deathtime

