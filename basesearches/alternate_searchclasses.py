import math

# solves for largest x such that f(x) <= y
# f must increase monotonically when analyzed with the expressions y > f(x) , y < f(x)
# if f is not provided, solves for the largest x such that the expression y <= x is true

class BinSearch:
    def __init__(
                self,
                y,
                lo,
                hi,
                f = lambda x : x,
                a = math.nan
                ):
        self.f = f
        self.lo = lo
        self.hi = hi
        self.term = False
        self.y = y
        if math.isnan(a):
            self.a = (lo + hi) / 2
        else:
            self.a = a

    #
    def searchstep (self):
        if self.y < self.f.__call__(self.a):
            self.hi = self.a
        elif self.y > self.f(self.a):
            self.lo = self.a
        else:
            self.term = True
        self.a = (self.lo + self.hi) / 2

class GNASearch(BinSearch):
    class Test:
        def __init__(self,f):
            self.f = f
        def __lt__(self,other):
            return self.f(other)
        def __gt__(self,other):
            return (not self.f(other))
    def __init__ (self, lo, hi, propotest, a = math.nan):
        super().__init__(self.Test(propotest), lo, hi , a = a)

