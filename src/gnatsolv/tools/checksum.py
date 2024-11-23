from hashlib import md5 as __md5__
from neuron import h
import numpy as np

def secchecksum_multivar(sec, varnames = ["diam"]):
    varmatrix = []
    for vname in varnames:
        rvar = h.RangeVarPlot(varname, sec(0), sec(1))
        v = h.Vector()
        rvar.to_vector(v)
        varmatrix.append(v)
    rawbin = np.array(varmatrix).flatten(order = "F").tobytes()
    return __md5__(rawbin).digest()
        
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

    @classmethod
    def treechecksum(cls, rootsec, attach = -1):
        attachbin = np.array((float(attach),)).tobytes()
        ssum = __md5__(secchecksum(rootsec) + attachbin).digest()
        children = np.array(rootsec.children())
        if len(children) == 0:
            return ssum
        hashes = np.array([
            cls.treechecksum(sec, attach = sec.parentseg().x) for sec in children
            ]) 
        hashes.sort()
        return __md5__(hashes.tobytes()).digest()

class GeomChecksum2(GeomChecksum):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.branchstruct = None

    def genhasharr(self, cell = None):
        pass
