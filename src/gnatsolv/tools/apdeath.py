import time
from neuron import h
from .aprecorder import APRecorder
from .oldapdeath import DeathTester

class DeathRec:
    def __init__(
            self,
            recbegin, recend,       # for the time being, these must be the same h.Section. (the recodring zone will only be that section)
            tstop,                  # NOTE: should be refactored to tstart
            minapspeed = 1,         # lambda/ms (unused)
            tinterval  = 0.25,      # ms
            maxsteps   = 100        
            ):
        self.deathtime = None

        self._setup_nodes(recbegin, recend)
        self.aprec = APRecorder(recend, 1)
        self.proptest = self.aprec.proptest
        self.tstop = tstop
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

    def run(self):
        """
        Run the simulation until membrane activity in the recording zone has died
        Prints warnings if no stimulation is detected after t = self.maxsteps * self.tinterval
        """
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
            # print(f"DeathRec: lifetest: {self.lifetest()}")
            
    def prelifetest(self):
        self.beginrvp.to_vector(self.beginvec)
        return self.beginvec.max() == 0

    def lifetest(self):
        self.beginrvp.to_vector(self.beginvec)
        self.deathrvp.to_vector(self.deathvec)
        return (self.beginvec.sub(self.deathvec)).max() > 0
        
    def getdeathtime(self):
        """
        Calculates and returns the time at which membrane activity in recording zone has dropped below DEATHMECH_VTHRESH
        (see deathmech.mod for details)
        Sets self.deathtime to the calculated value
        """
        self.deathrvp.to_vector(self.deathvec)
        self.deathtime = self.deathvec.max() 
        return self.deathtime

