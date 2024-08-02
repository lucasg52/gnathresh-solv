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
        self.nodes = []
        for sec in seclist:
            self.nodes.extend(list(sec.allseg()))
        for s in seclist:
            s.insert("apdeath")
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
        h.updatet_deathupdate = self.tstop
        h.continuerun(self.tstop)
        i = self.maxsteps
        while i and self.prelifetest():
            i -=1 
            assert (h.updatet_deathupdate >= 1e9)
            h.updatet_deathupdate = h.t + self.tinterval
            h.continuerun(h.t + self.tinterval)
        while i and self.lifetest():
            i -= 1
            h.updatet_deathupdate = h.t + self.tinterval
            h.flagactive_apdeath = 0
            h.continuerun(h.t + self.tinterval)
        if i == 0:
            print("U suck")
            print(str(h.flagbegin_apdeath)+str(h.flagactive_apdeath))
    def prelifetest(self):
        #return all(
        #            node.begin_apdeath == 0 
        #            for node in self.nodes
        #        )
        return h.flagbegin_apdeath == 0

    def lifetest(self):
        #return not all(
        #        bool(node.begin_apdeath) == bool(node.deatht_apdeath)
        #        for node in self.nodes
        #        )
        return h.flagactive_apdeath
    def getdeathtime(self):
        self.deathtime = max(node.deatht_apdeath for node in self.nodes)
        return self.deathtime

