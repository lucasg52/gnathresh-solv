"""
Environments will be the standard method of setting up experiments that involve calculating gna thresh for a particular geometry or family of cell geometries.
Instance attributes:
m:         m(y Cell) -- the cell for which gna thresh is computed
stim:      The stimulus for the cell. Often an h.IClamp

Instance methods:
fullsolve:   Compute the gna thresh for the cell, given some arguments for optimization.
prerun(gna): Achieve a steady state by running a large time step from the initial condition, from a negative value for t.
"""
