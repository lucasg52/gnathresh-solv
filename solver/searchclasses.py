# Lucas Swanson -- Ripon College '27

# This file (for now) simply lays out what I believe the solver could look like.

import math

class BinSearch(): # should change name to BinSearch ?
    """
    Sets up a binary search
        lo, hi,           the assumed window (lower and upper bounds) in which the solution lies
        propatest,        the function that will return True if propagation succeeds, False otherwise
        a = math.nan,     optionally, a first guess can be provided (otherwise is the median between lo and hi)
        stopcond = None   for use of fullsearch() . if left as None, will throw warning, and not iterate

    """
    def __init__(
                 self,
                 lo, hi,
                 propatest,
                 a = math.nan,
                ):
        self.lo = lo
        self.hi = hi
        self.term = False
        self.propatest = propatest
        if math.isnan(a):
            self.a = (lo + hi) / 2

    def searchstep (self): 
        """ Iterate the search
        pass approximation (a) to propatest, if true is returned, assume approximation too high, if false, vise-versa.
        Returns: None
        """
        if self.propatest(self.a):
            self.hi = self.a
        else:
            self.lo = self.a
        self.a = (self.lo + self.hi) / 2

#    def fullsearch (self):
#        if self.stopcond is None:
#            sys.stderr.write("GNASearch: called fullsearch() without stop condition")
#        else:
#            while self.stopcond(self): #and self.term is True:
#                self.searchstep()
#        
#        return self.a


class ExpandingSearch(BinSearch):
    # This class will be useful when bounds for the solution may be provided that are not consistent (there may be a chance that the provided bounds do not contain the solution)
    # the search will thus expand the bounds accordingly before switching to a binary search again.
    """
    Identifies more feisable bounds before initiating a binary search
        lo, hi,           the assumed window (lower and upper bounds) in which the solution lies
        propatest,        the function that will return True if propagation succeeds, False otherwise
        lim_lo, lim_hi,   since the search may expand, these will provide hard upper and lower bounds
        a = math.nan,     optionally, a first guess can be provided (otherwise is the median between lo and hi)
        stopcond = None   for use of fullsearch() . if left as None, will throw warning, and not iterate

    """
    def __init__(
                 self,
                 lo, hi,
                 propatest,
                 lim_lo, lim_hi,
                 a = math.nan
                ):
        self.lim_lo = lim_lo
        self.lim_hi = lim_hi
        super().__init__(lo, hi, propatest, a = a)

    def searchstep(self):
        """ Iterate the search
        Checks if alledged solution lies between hi and lo before proceeding as a binary search (see help(BinSearch))
        if alledged solution does not lie therein, search range expands by 2x and is shifted accordingly.
        if alledged solution does not lie between lim_lo and lim_hi, returns True and no iteration occurs
        Returns: 
            None if successful, True if failure (see above)
        """
        self.hi = min(self.lim_hi, self.hi)
        self.lo = max(self.lim_lo, self.lo)
        d = self.hi - self.lo
        if d == 0:
            self.a = self.lo
            return True
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


GNASearch = BinSearch       # for legacy code (BinSearch was formally GNASearch)
