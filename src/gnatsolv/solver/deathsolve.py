from .newton import dualderiv_inv ,DiscreteNewton_dualfun as DNewton
#from ..tools.apdeath import DeathTester
from ..tools.aprecorder import APRecorder
from neuron import h
from math import nan as __nan__, e as __e__ 
#
#class SegDeathSolver(DeathTester):
#    def __init__ (self, dseg, setg, *args, **kwargs):
#        kwargs["tree"] = []
#        self.seg = dseg
#        self.setg = setg
#        self.search = DNewton()
#        super().__init__(*args, **kwargs)
#    def _initnodes(self):
#        self.nodes = [h.DeathRec(self.seg)]
#
#    def timetest(self):
#        self.proptest()
#        return self.
#
#
#    def solve(self, acc):
#
class SegDeathSolver:
    def __init__ (self,
            lo,
            hi,
            a,
			dseg,
			setg,
			tstop,
			vinitial,
			interval = 3,
			maxsteps = 100,
            coef = pow(2, -4)
            ):
        self.lo = lo
        self.hi = hi
        self.seg = dseg
        self.setg = setg
        self.tstop = tstop
        self.vinitial = vinitial
        self.interval = interval
        self.maxsteps = maxsteps
        self.coef = coef
        self.search = DNewton(self.timedualderiv, a, (self.hi - self.lo) * coef)
        self.rec = h.DeathRec(self.seg)
        self.aprec = APRecorder(self.seg.sec, self.seg.x)
        self.aprec.nc.threshold = -10
    def _initnodes(self):       #should be changed to have more nodes
        self.nodes = [h.DeathRec(self.seg)]

    def timetest(self, g):
        self.setg(g)
        h.finitialize(self.vinitial)
        h.continuerun(self.tstop)
        for i in range(self.maxsteps):
            if self.rec.deatht == 0:
                if h.t > 5 and self.rec.begin == 0:
                    return __nan__
                h.continuerun(h.t + self.interval)
            else:
                if i > 0:
                    self.interval *= i+1//2
                    self.tstop = self.rec.deatht + self.interval
                    break
        return self.rec.deatht 

    def timedualderiv(self,g , dg, adjustdx = True):
        dx = self.search.dx
        fa = self.timetest(g)
        fb = self.timetest(g+dx)
        fc = self.timetest(g+ 2*dx)
        if adjustdx:
            minsteps = int(min(fb-fa, fc-fb) / h.dt)
            if minsteps > 4:
                self.search.dx /= minsteps-2
                print("new dx" + str(self.search.dx))
        return dx/(fb-fa), dx/(fc-fb)

    def solve(self, acc):
        if (self.hi - self.lo) < acc:
            print("no solve cus acc too big")
        while (self.hi - self.lo) > acc:
            line = self.search.searchstep()
            print(line)
            #if self.aprec.proptest():
            #    self.hi = line.inter
            #else:
            #    self.lo = line.inter
            #assert self.lo < self.hi
            #self.search.dx = (self.hi - self.lo) * self.coef

    def _set_tstop(self, val):
        h.tstop = self.__tstop = val
    def _get_tstop(self):
        return self.__tstop
    tstop = property(fget = _get_tstop, fset = _set_tstop, doc = \
            "the time that the simulation should run to if the other attributes are" 
            "calibrated correctly."
            "if sync_tstop is True then h.tstop will change alongside it")



