import math

class GNASearch():

    def __init__ (self, lo, hi, propotest, a = math.nan):
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
    def __init__(self, lo, hi, propotest, lim_lo, lim_hi, a = math.nan):
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



