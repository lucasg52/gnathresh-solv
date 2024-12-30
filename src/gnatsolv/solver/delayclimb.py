"""
a DelayClimb search will try to stick to sampling one side of a logarithm curve to find its roots.
"""
import numpy as np
from .searchclasses import ExpandingSearch

def unit_expo(base, x):
    x = float(x)
    base = float(base)
    return (
            (1 - pow(base, x))
            / (1 - base)
            )

def fit_3pnt_expo(
        maxiters,
        xarr, yarr,
        lo, hi,
        **kwargs
        ):
    x_scale = xarr[-1] - xarr[0]
    y_scale = yarr[-1] - yarr[0]
    xtarg = (xarr[1] - xarr[0]) / x_scale
    ytarg = (yarr[1] - yarr[0]) / y_scale
    lotrans = pow(lo, x_scale)
    hitrans = pow(hi, x_scale)
    restrans = fit_unit_expo(
            maxiters,
            xtarg, ytarg,
            lotrans, hitrans,
            **kwargs
            )
    base = pow(restrans, 1/x_scale)
    k = y_scale/(pow(base, xarr[2]) - pow(base, xarr[0]))
    thresh = yarr[0] - k * pow(base, xarr[0])
    return base, thresh

def fit_unit_expo(
        maxiters,
        xtarg, ytarg,
        lo, hi,
        radius = 0,
        **kwargs
        ):
    search = ExpandingSearch(
            lo, hi,
            proptest = lambda base : ytarg > unit_expo(base, xtarg),
            lim_lo = 0, lim_hi = 1-pow(2,-7),
            **kwargs
            )
    for i in range(maxiters):
        d = search.hi-search.lo
        if d < radius:
            return search.a
        if search.searchstep():
            raise ValueError("search failed")
    return search.a

class DelayPnt(tuple):
    """
    Represents a point (gna, delay) where delay is the AP death time (see gnatsolv.tools.apdeath)
    """
    gna = property(lambda self : self[0])
    delay = property(lambda self : self[1])

class DelayClimb:
    """
    A DelayClimb search will try to stick to sampling one side of a logarithm curve to find its
    roots.
    The delay curve is modeled as g_bar(delay) = k*base^delay + thresh
        proptest,   function that takes one parameter, gna, and returns prop, delay:
            prop:   True if AP propogates, false otherwise
            delay:  AP death delay
        startpnts   array of three starting points (gna, delay) with sub-threshold gna
    Properties:
        base:           previous base of the fitted exponential
        preverror:      difference between the previous guess (for the base of the exp.) and self.base
        safety_factor:  factor by which the threshold is avoided, between 0 and 1.
                        Making it smaller allows for faster convergence, but simulation runs may be wasted due to having above-threshold gna.
                        Making it too large will slow down convergence.
        fititers:       number of binary search iterations to fit the exponential
        pnts:           array of 3 DelayPoints, in order of increasing gna
        maxgna:         self.pnts[2].gna
    """
    def __init__(
                 self,
                 proptest,
                 startpnts
                ):
        if len(startpnts) != 3:
            raise TypeError("startpnts should be a 3 x 2 array of numbers")

        self.proptest = proptest

        self.base = 0.5
        self.preverror = 0.25
        # curve is modeled as g_bar(delay) = k*base^delay + thresh
        # if two points (del_0, g_0), (del_1, g_1) are already known, then we have
        # k = (g_1 - g_0)/(base^del_1 - base^del_0)
        # thresh = g_0 - k * base^del_0
        # for some base in the interval (0,1)
        self.fititers = 10
        self.safety_factor = 1/10

        self.pnts = [DelayPnt(t) for t in startpnts]
        self.pnts.sort()

    maxgna = property(lambda self : self.pnts[2].gna)

    def _fit(self, fititers = None):
        # curve fitting precision increases despite a constant number of search iterations thanks to:
        #   points being closer to the asymptote
        #   guessing subsequent exponential base using error of previous guess
        if fititers is None:
            fititers = self.fititers
        gna = np.array([p.gna for p in self.pnts])
        delay = np.array([p.delay for p in self.pnts])
        newbase, thresh = fit_3pnt_expo(
                fititers,
                delay, gna,
                self.base - self.preverror, self.base + self.preverror
                )
        self.preverror = abs(newbase - self.base)
        self.base = newbase
        return thresh

    def get_nonprop_result(self, gna, depth = 0):
        """
        Tries to find a sub-threshold gna between gna and self.maxgna
        Returns:
            gna -- a sufficent gna
            delay -- the time it took for the AP to die
        Raises RecursionError upon failure
        """
        if depth > 4:
            raise RecursionError("failed to find nonpropogating gna value")
        prop, delay = self.proptest(gna)
        if prop:
            print("DelayClimb: Warning: wasted an iteration - safety_factor may be to small")
            return self.get_nonprop_result((gna + self.maxgna)/2, depth + 1)
        return gna, delay


    def searchstep(self, safety_factor = None, fititers = None):
        """
        calls proptest with a gna closer to the threshold by a factor of approximately
        safety_factor, and logs the death time associated with that gna (pushing it to the front
        of self.pnts)
        Returns: None
        Raises RuntimeError if unable to find a sub-threshold gna
        """
        if safety_factor is None:
            safety_factor = self.safety_factor
        thresh = self._fit(fititers)
        nextgna = thresh - safety_factor * (thresh - self.maxgna)
        try:
            nextgna, delay = self.get_nonprop_result(nextgna)
        except RecursionError as e:
            raise RuntimeError(str(e) + f"\nsearched between {self.maxgna} and {nextgna}")
        self.pnts.append(
                DelayPnt((nextgna, delay))
                )
        del self.pnts[0]

