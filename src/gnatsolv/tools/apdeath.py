from warnings import warn
from neuron import h
from .aprecorder import APRecorder

class DeathRec:
    """
    monitors when (and where) an AP begins and subsequently dies using h.RangeVarPlot
    over the 'begin' and 'death' range variables defined in modfiles/deathmech.mod 
    a recording zone is defined using two sections (see __init__)
    an aprecorder (self.aprec) is placed at the end of the recording zone, and
    its proptest method is aliased as self.proptest for compatability
    """
    def __init__(
            self,
            recbegin, recend,       # the beginning section and ending section of the recording zone. May be the same section.
            tstart,                 # time when death detection begins; ideally, it is tuned to be exactly when AP reaches the recording zone
            minapspeed = 1,         # lambda/ms (unused)
            tinterval  = 0.25,      # ms
            maxsteps   = 100        # maximum number of steps of length tinterval to run simulation
            ):
        self.deathtime = None

        self._setup_nodes(recbegin, recend)
        self.aprec = APRecorder(recend, 1)
        self.proptest = self.aprec.proptest
        self.tstart = tstart
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
        h.continuerun(self.tstart)
        i = self.maxsteps
        while i and self.prelifetest():
            i -=1 
            h.continuerun(h.t + self.tinterval)
        while i and self.lifetest():
            i -= 1
            h.continuerun(h.t + self.tinterval)
        if i == 0:
            if self.prelifetest():
                warn(f"AP detected at t = {self.beginvec.min()} but did not die before t = {h.t}",
                        Warning, stacklevel=2)
            else:
                warn(f"did not detect cell stimulation between t = {self.tstart} and t = {h.t}",
                        Warning, stacklevel=2)
            
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

