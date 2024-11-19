"""
a DelayClimb search will try to stick to sampling one side of a logarithm curve to find its roots.
"""
import numpy as np
from .searchclasses import ExpandingSearch
#def rangetransform(arr):
#    return (arr - arr[0]) / (arr[-1] - arr[0])
#def rangetransform_inv(arr, x):
#    return (arr[-1] - arr[0]) * x + arr[0]
def unit_expo(base, x):
        return (
                (1 - pow(base, x))
                / (1 - base)
                )

def unit_expo_partialbase(base, x):
    return (
                (
                    (1 - pow(base , x))
                    - (1 - base) * x * pow(base, x-1)
                )
                / pow((1 - base), 2)
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
    thresh = yarr[0] - k * pow(xarr[0])
    return base, thresh

def fit_unit_expo(
        maxiters,
        xtarg, ytarg,
        lo, hi,
        **kwargs
        ):
    search = ExpandingSearch(
            lo, hi,
            propatest = lambda base : ytarg > unit_expo(base, xtarg),
            lim_lo = 0, lim_hi = 1-pow(2,-7),
            **kwargs
            )
    def newton(base_est):
        deriv = unit_expo_partialbase(base_est, xtarg)
        if abs(deriv) < pow(2,-50):
            return -1
        return (
                base_est
                + (
                    ytarg
                    - unit_expo(base_est, xtarg)
                    )
                / deriv
                )
    newtguess = 0
    for i in range(maxiters):
        if search.lo < newtguess < search.hi:
            newtguess = newton(newtguess)
        else:
            if search.searchstep():
                raise ValueError("search failed", {"search" : (search.lo, search.hi), "newtguess" : newtguess, "i" : i})
            if newtguess != -1:
                newtguess = newton(search.a)

    if search.lo < newtguess < search.hi:
        return newtguess
    return search.a

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
    the delay curve is modeled as g_bar(delay) = k*base^delay + thresh
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

        self.base = 0.5
        self.preverror = 0.25
        # curve is modeled as g_bar(delay) = k*base^delay + thresh
        # if two points (del_0, g_0), (del_1, g_1) are already known, then we have
        # k = (g_1 - g_0)/(base^del_1 - base^del_0)
        # thresh = g_0 - k * base^del_0
        # for some base in the interval (0,1)
        self.fititers = 6
        self.safety_factor = 1/10

        self.pnts = [DelayPnt(*t) for t in startpnts]
        self.pnts.sort()

    maxgna = property(lambda self : self.pnts[2].gna)

    def fit(self, fititers = None):
        if fititers is None:
            fititers = self.fititers
        gna = np.array(p.gna for p in self.pnts)
        delay = np.array(p.delay for p in self.pnts)
        newbase, thresh = fit_3pnt_expo(
                fititers,
                delay, gna,
                self.base - self.preverror, self.base + self.preverror
                )
        self.preverror = abs(newbase - self.base)
        self.base = newbase
        return thresh

    def get_nonprop_result(self, gna, depth = 0):
        if depth > 4:
            raise RecursionError("strange... you should probably do a binary search. this is some bs")
        prop, delay = self.propatest(gna)
        if prop:
            print("DelayClimb: Warning: wasted an iteration - safety_factor may be to small")
            return self.get_nonprop_result((gna - self.maxgna)/2, depth + 1)
        return gna, delay


    def searchstep(self, safety_factor = None, fititers = None):
        if safety_factor is None:
            safety_factor = self.safety_factor
        thresh = self.fit(fititers)
        nextgna = thresh - safety_factor * (thresh - self.maxgna)
        nextgna, delay = self.get_nonprop_result(nextgna)
        self.pnts.append(
                DelayPnt(nextgna, delay)
                )
        del self.pnts[0]

