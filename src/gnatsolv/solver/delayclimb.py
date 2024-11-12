"""
a DelayClimb search will try to stick to sampling one side of a logarithm curve to find its roots.
"""
import numpy as np
class DelayPnt:
    def __init__(self, *args):
        self.data = args
    gna = property(lambda self : self.data[0])
    delay = property(lambda self : self.data[1])
    def __lt__(self, other):
        return self.gna < other.gna
    def __eq__(self, other):
        return self.gna == other.gna
    def __gt__(self, other):
        return self.gna > other.gna
class DelayClimb:
    """
    a DelayClimb search will try to stick to sampling one side of a logarithm curve to find its
    roots.
    the delay curve is modeled as delay(g) = offset + power * ln(thresh-g)
    """
    def __init__(
                 self,
                 propatest,
                 startpnts
                ):
        print("WARNING! DelayClimb is NOT YET STABLE. Limit usage to small experiments only to avoid time loss")
        if len(startpnts) != 3:
            raise TypeError("startpnts should be a 3 x 2 array of numbers")

        self.propatest = propatest

        self.state = np.nan * np.ones(3)
        # curve is modeled as delay(g) = offset + ln((thresh-g)^power)
        # which is equal to offset + power * ln(thresh-g)
        self.newtoniters = 2
        self.safety_factor = 1/8
        
        # ada lovelace was the daughter of a poet
        
        self.pnts = [DelayPnt(*t) for t in startpnts]
        self.pnts.sort()

    maxgna = property(lambda self : self.pnts[2].gna)

    offset = property(
            fget = lambda self : self.state[0],
            fset = lambda self, val : self.state.__setitem__(0, val))
    power  = property(
            fget = lambda self : self.state[1],
            fset = lambda self, val : self.state.__setitem__(1, val))
    thresh = property(
            fget = lambda self : self.state[2],
            fset = lambda self, val : self.state.__setitem__(2, val))
    def fit(self, numiters = None):
        if numiters is None:
            numiters = self.newtoniters
        if np.isnan(self.offset):
            self.offset = self.pnts[1].delay
        if np.isnan(self.power):
            self.power = -0.15
        if np.isnan(self.thresh):
            self.thresh = self.maxgna + (self.maxgna - self.pnts[1].gna)/4
        gna = np.array([self.pnts[i].gna for i in range(3)])
        delay = np.array([self.pnts[i].delay for i in range(3)])
        for i in range(numiters):
            if max(gna) > self.thresh:
                d = max(gna)-self.thresh
                new =self.thresh + 1.25*d
                print(f"DelayClimb: Warning: insoluable threshold estimate on iteration {i+1}" 
                        + f" (was {self.thresh:0.12g}, is now {new:0.12g})")
                self.thresh = new
            delta = self.thresh * np.ones(3) - gna
            error = (self.offset * np.ones(3) + self.power * np.log(delta)) - delay
            jaco = np.array([np.ones(3), np.log(delta), self.power * delta ** -1]).T
            self.state -= (np.linalg.solve(jaco, error))
    def get_nonprop_result(self, gna, depth = 0):
        if depth > 4:
            raise RecursionError("strange... you should probably do a binary search. this is some bs")
        prop, delay = self.propatest(gna)
        if prop:
            print("DelayClimb: Warning: wasted an iteration - safety_factor may be to small")
            return self.get_nonprop_result((gna - self.maxgna)/2, depth + 1)
        return gna, delay 


    def searchstep(self, safety_factor = None, numiters = None):
        if safety_factor is None:
            safety_factor = self.safety_factor
        try:
            self.fit(numiters = numiters)
        except np.linalg.LinAlgError as e:
            print("curve fit failed -- nonsingular jacobian")
            raise e
        if (
                self.power >= 0
                or self.thresh < self.maxgna
                ):
            raise RuntimeError("curve fitting failed")
        nextgna = self.thresh - safety_factor * (self.thresh - self.maxgna)
        nextgna, delay = self.get_nonprop_result(nextgna)
        self.pnts.append(
                DelayPnt(nextgna, delay)
                )
        del self.pnts[0]



