from hashlib import md5 as __md5__
from neuron import h
import numpy as np

def secchecksum(sec, varname = None):
    if varname is None:
        varname = "diam"
    rvar = h.RangeVarPlot(varname, sec(0), sec(1))
    rawbin = np.array(rvar.vector()).tobytes()
    return (__md5__(rawbin)).digest()

class GeomChecksum:
    def __init__(self, cell, varname = "diam"):
        self.varname = varname
        self.secnames, self.hasharr = self.genhasharr(cell)

    def genhasharr(self, cell):
        d = {sec.name() : secchecksum(sec, self.varname) for sec in cell.all}
        keys = list(d.keys())
        keys.sort()
        secnames = keys.copy()
        hasharr = [d[k] for k in keys]
        return secnames, hasharr
    def compare(self, other):
        ret = []
        if self.digest() != other.digest():
            for name, selfh, otherh in zip(self.secnames, self.hasharr, other.hasharr):
                if selfh != otherh:
                    ret.append((name, selfh, otherh))
        return ret
    def digest(self):
        return __md5__(b''.join(self.hasharr)).digest()
