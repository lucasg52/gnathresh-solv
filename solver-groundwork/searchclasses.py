# Lucas Swanson Ripon College '27

# This file (for now) simply lays out what I believe the solver could look like.

import math

class GNASearch():

    def __init__(
                 self,
                 lo, hi,                # the assumed window in which the solution lies
                 propotest,             # the function that will return True if propogation succeeds, False otherwise
                 a = math.nan           # optionally, a first guess can be provided (otherwise is the median between lo and hi)
                ):
        self.lo = lo
        self.hi = hi
        self.term = False
        self.propotest = propotest
        if math.isnan(a):
            self.a = (lo + hi) / 2

    def searchstep (self):
        if self.propotest(self.a):
            self.hi = self.a
        else:
            self.lo = self.a
        self.a = (self.lo + self.hi) / 2

class ExpandingSearch(GNASearch):
    # This class will be useful when bounds for the solution may be provided that are not consistent (there may be a chance that the provided bounds do not contain the solution)
    # the search will thus expand the bounds accordingly before switching to a binary search again.
    def __init__(
                 self,
                 lo, hi,                # the assumed window in which the solution lies
                 propotest,             # the function that will return True if propogation succeeds, False otherwise
                 lim_lo, lim_hi,        # since the search may expand, these will provide hard upper and lower bounds
                                        # (NOT IMPLIMENTED YET)
                 a = math.nan           # optionally, a first guess can be provided (otherwise is the median between lo and hi)
                ):
        self.lim_lo = lim_lo
        self.lim_hi = lim_hi
        super().__init__(lo, hi, propotest, a = a)

    def searchstep(self):
        d = self.hi - self.lo
        if not self.propotest(self.hi):
            self.hi += 2 * d
            self.lo += d
            self.a = (self.lo + self.hi) / 2
        elif self.propotest(self.lo):
            self.lo -= 2 * d
            self.hi -= d 
            self.a = (self.lo + self.hi) / 2
        else:
            super().searchstep()



