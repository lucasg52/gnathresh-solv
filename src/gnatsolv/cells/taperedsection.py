from neuron import h
import numpy as np
from .adoptedeq import normalize_dlambda
from  math import ulp as __ulp__
"""I don't expect anyone to read this file yet. Please tell me if you read this"""
#KISS:
#Keep It Simple, Stupid.
__NORMEPSILON__ = __ulp__(5)
class TaperedSection():
    """Create a tapered section in the same position as originsec, which tapers to diameters at distances specified in taperpnts"""
    def __init__(
            self,
            name,
            cell, 
            taperpnts = [],
            originsec = None,
            directionvec = np.array((1,0,0))
            ):
        class ModTuple(tuple):
            def __gt__(self, other):
                return self[0] > other[0]
            def __lt__(self, other):
                return self[0] < other[0]
            def __eq__(self, other):
                return self[0] == other[0]
        taperpnts = [] + [ModTuple(t) for t in taperpnts]
        print(taperpnts)

        self.taperpnts = taperpnts
        taperpnts.sort()

        assert (abs(np.dot(directionvec, directionvec) - 1) <= __NORMEPSILON__) 
        self.directionvec = directionvec

        # Initialize nescessary attributes based on originsec, create one if not avaliable
        if originsec is None:
            originsec = h.Section(name, cell)

        self.parentseg = originsec.parentseg() # inheret the parent segment for getting proper initial diam 
        #h.define_shape()
        #self.originpos = (
        #        originsec.x3d(0),
        #        originsec.y3d(0),
        #        originsec.z3d(0)
        #        )
        self._L = float(originsec.L) # float casting probably not nescessary, but ensures we are not referencing an object.
        if self.parentseg:
            self.startdiam = self.parentseg.diam # not casting because it does not hurt to have it be a reference.
        else:
            self.startdiam = float(originsec.diam) # float casting probably not nescessary, but ensures we are not referencing an object.
        self.enddiam = float(originsec.diam)
 
        self.seclist = []
        self._create_sections(taperpnts, originsec, name, cell)
    def _create_sections(self, taperpnts, originsec, name, cell):
        for i, t in enumerate(taperpnts):
            self.seclist.append(
                        h.Section(name = f"{name}[{i}]", cell = cell)
                    )
        self.seclist.append(originsec) # originsec is preserved as the last section to preserve children attached to the 

        for i, sec in enumerate(self.seclist[1::]):
            sec.connect(self.seclist[i](1))
        if self.parentseg is not None:
            self.seclist[0].connect(self.parentseg) # connect to the parent segment, if avaliable

        self.reinsert_all() 

        self.Lerror() # calculate the total length and error
        # range vars and such could be either inserted w/ dictionary copying from originsec or by patiently assigning them afterwards
    def reinsert_all(self):
        for i, sec in enumerate(self.seclist):
            self.reinsert_section(i, sec)
    def _getargs(self, i):
        if i == -1:
            #return((*self.originpos, self.startdiam))
            return((0, 0, 0, self.startdiam))
        elif i == len(self.taperpnts):
            return((*tuple(self.directionvec * self._L), self.enddiam))
        x, diam = self.taperpnts[i]
        return((*tuple(self.directionvec * x), diam))

    def reinsert_section(self, i, sec):
        prevargs = self._getargs(i-1)
        nextargs = self._getargs(i)
        h.pt3dclear(sec = sec)
        h.pt3dadd(*prevargs , sec = sec) 
        h.pt3dadd(*nextargs , sec = sec) 

        # print("review celltemplates.py, reinsert_section")


### The following methods are not part of the __init__ block, and are not nescessary for review. They only exist for syntatic convience.###

    def Lerror(self): # calculate the total length and error
        self.L = sum([sec.L for sec in self.seclist])
        return (self.L, self._L)
    def connect(self, seg):
        self.startdiam = seg.diam
        self.seclist[0].connect(seg)
        self.update_edge_diams()
    def update_edge_diams(self):

        if self.parentseg is not None:
            self.startdiam = self.parentseg.diam
        #if len(self._children) == 1:
        #    self.enddiam = (self._children[0](0)).diam

        h.pt3dchange(0,self.startdiam, sec = self.seclist[0])
        h.pt3dchange(1,self.enddiam, sec = self.seclist[-1])
    def __iter__(self, *args):
        self.seclist.__iter__(*args)
    def __index__(self, *args):
        self.seclist.__index__(*args)

class TaperedSection_compress(TaperedSection):
    """create a tapered section and display explicit statments to build the equivalent section"""
    def __init__(
            self,
            name,
            cell, 
            taperpnts = [],
            originsec = None,
            directionvec = np.array((1,0,0))
            ):
        print("compressed TaperedSection:")
        print("self.seclist = []")
        for i, t in enumerate(taperpnts):
            print("\
            self.seclist.append(\n\
                        h.Section(name = \"{}[{}]\")\n\
                    )".format(name,i)
                )
        print("self.seclist.append(originsec)")
        super().__init__(
                name,
                cell, 
                taperpnts,
                originsec,
                directionvec
                )

        #super()._create_sections(taperpnts, originsec, name, cell)
        for i, sec in enumerate(self.seclist[1::]):
            print("sec.connect(self.seclist[{}])".format(i))
        if self.parentseg is not None:
            self.seclist[0].connect(self.parentseg)
    def reinsert_section(self, i, sec):
        prevargs = self._getargs(i-1)
        nextargs = self._getargs(i)
        print("h.pt3dclear(sec = self.seclist[{}])".format(i))
        print("h.pt3dadd(*{}, sec = self.seclist[{}])".format(str(prevargs), i)) # print deez 
        print("h.pt3dadd(*{}, sec = self.seclist[{}])".format(str(nextargs), i))

        super().reinsert_section(i, sec)

