import math


class Line():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def _get_slope(self):
        return((self.a[1]-self.b[1]) / (self.a[0] - self.b[0]))
    slope = property(_get_slope) 
    def _get_inter(self):
        if self.slope == 0:
            return math.nan
        return (-self.a[1]/self.slope) + self.a[0]
    inter = property(_get_inter)
    def __repr__(self):
        return f"{self.a}, {self.b}, {self.inter}"

class DiscreteNewton:
    def __init__(
            self,
			#lim_lo, lim_hi,
            fun,
            a,
            dx
			):
        #self.lim_lo     = lim_lo
        #self.lim_hi     = lim_hi
        self.fun        = fun
        self.a          = a
        self.dx         = dx
    def searchstep(self, dx = math.nan):
        if math.isnan(dx):
            dx = self.dx
        assert(abs(dx) > 2* math.ulp(self.a))
        a = self.a
        b = a + dx
        p_a = (a, self.fun(a))
        p_b = (b, self.fun(b))
        line = Line(p_a, p_b)
        self.a = line.inter
        return line



