"""
Environments will be the standard method of setting up experiments that involve calculating gna thresh for a particular geometry or family of cell geometries.
Instance attributes:
m:         m(y Cell) -- the cell for which gna thresh is computed
stim:      The stimulus for the cell. Often an h.IClamp

Instance methods:
fullsolve:   Compute the gna thresh for the cell, given some arguments for optimization.
prerun(gna): Achieve a steady state by running a large time step from the initial condition, from a negative value for t.
"""

from abc import ABC, abstractmethod

class AbstractEnviro(ABC):
    def __init__(self, m, aprec, stim, dt = pow(2,-6), **kwargs):
        self.m = m
        self.aprec = aprec
        self.stim = stim
        self.dt = dt
        self._init_options(**kwargs)

    @abstractmethod
    def _init_options(self, **kwargs):
        '''
        initialize the environment's options which are attributes in ALL CAPS
            Options are things that the user may want to change on the fly in an interactive terminal
            Otherwise they should be configurable via class inheretance (redefining methods)
        '''
        pass

    #def _setup(self):
    #     
    def set_gbar(self, gbar):
        for sec in self.m.soma.wholetree():
            try:
                sec.gbar_nafTraub = gbar
                sec.gbar_kdrTraub = gbar
            except AttributeError:
                pass

    @abstractmethod
    def fullsolve(self):
        '''solve for gNa_Thresh given the current state of the environment'''
        pass


