# Lucas Swanson -- Ripon College '27

# This file (for now) simply lays out what I believe the solver could look like.

import math
import sys

class StrictInt(int):
    def __truediv__(self,other):
        return StrictInt(super().__truediv__(other))
    def __mul__(self,other):
        return StrictInt(super().__mul__(other))
    def __add__(self,other):
        return StrictInt(super().__add__(other))
    def __sub__(self,other):
        return StrictInt(super().__sub__(other))

class GNASearch(): # should change name to BinSearch ?

    def __init__(
                 self,
                 lo, hi,                # the assumed window in which the solution lies
                 propatest,             # the function that will return True if propagation succeeds, False otherwise
                 a = math.nan,           # optionally, a first guess can be provided (otherwise is the median between lo and hi)
                 stopcond = None        # for use of fullsearch() . if left as None, will throw warning, and not iterate
                ):
        self.lo = lo
        self.hi = hi
        self.term = False
        self.propatest = propatest
        self.stopcond = stopcond
        if math.isnan(a):
            self.a = (lo + hi) / 2

    def searchstep (self):
        if self.propatest(self.a):
            self.hi = self.a
        else:
            self.lo = self.a
        self.a = (self.lo + self.hi) / 2

    def fullsearch (self):
        if self.stopcond is None:
            sys.stderr.write("GNASearch: called fullsearch() without stop condition")
        else:
            while self.stopcond(self): #and self.term is True:
                self.searchstep()
        
        return self.a


class ExpandingSearch(GNASearch):
    # This class will be useful when bounds for the solution may be provided that are not consistent (there may be a chance that the provided bounds do not contain the solution)
    # the search will thus expand the bounds accordingly before switching to a binary search again.
    def __init__(
                 self,
                 lo, hi,                # the assumed window in which the solution lies
                 propatest,             # the function that will return True if propagation succeeds, False otherwise
                 lim_lo, lim_hi,        # since the search may expand, these will provide hard upper and lower bounds
                                        # (NOT IMPLIMENTED YET)
                 a = math.nan           # optionally, a first guess can be provided (otherwise is the median between lo and hi)
                ):
        self.lim_lo = lim_lo
        self.lim_hi = lim_hi
        super().__init__(lo, hi, propatest, a = a)

    def searchstep(self):
        d = self.hi - self.lo
        if not self.propatest(self.hi):
            self.hi += 2 * d
            self.lo += d
            self.a = (self.lo + self.hi) / 2
        elif self.propatest(self.lo):
            self.lo -= 2 * d
            self.hi -= d 
            self.a = (self.lo + self.hi) / 2
        else:
            self.searchstep = super().searchstep
            super().searchstep()



