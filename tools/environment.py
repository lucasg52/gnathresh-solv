'''
A tool for setting up a pretty good simulation environment, similar to the one I described 
last monday
That is, a tool to set up a gnathresh-solving environment that will automatically adjust tstop 

### Options ###

SHAPECONFIG = None      # determine a function for specificing pt3d info at each solve 

PRINTTIME = False       # Prints the runtime of fullsearch if True

STEADYDUR = 200         # simulation time for calculating steady state

STEADYDT =  pow(2, -2)  # the dt used to reach a steady state

APTRAVELTIME = 10       # expected time it takes for AP to travel normally

TSTOPSAFETY = 6         # maximum amount of sim time allowed between ap propogation and 
                        # end of simulation
                        # in future iterations this may be depreciated

TSTOPINCREMENT = 3      # increment for increasing tstop

MAXGBAR = 0.45          # maximum gbar for search (search will not go above this value)

### Objects ###

m = None                # the cell to do experiments on
aprec = None            # the APRecorder object on the cell
stim = None             # the IClamp object on the cell (MUST BE SET MANUALLY)

### Globals ###

TSTOP = None            # the simulation's tstop, should be considered read-only
                        # in future iterations this may be depreciated

dt = pow(2,-6)          # the dt that will be used to model the simulation after steady
                        # state is reached
'''

import time
from neuron import h
from .aprecorder import APRecorder
from ..solver.searchclasses import ExpandingSearch


### Options ###
SHAPECONFIG = None      # determine a function for specificing pt3d info for this bullshit 
PRINTTIME = False       # Prints the runtime of fullsearch if True
STEADYDUR = 200         # simulation time for calculating steady state
STEADYDT =  pow(2, -2)  # the dt used to reach a steady state
APTRAVELTIME = 10       # expected time it takes for AP to travel normally
TSTOPSAFETY = 6         # maximum amount of sim time allowed between ap propogation and 
                        # end of simulation
                        # in future iterations this may be depreciated
TSTOPINCREMENT = 3      # increment for increasing tstop
MAXGBAR = 0.45          # maximum gbar for search (search will not go above this value)

### Objects ###
m = None                # the cell to do experiments on
aprec = None            # the APRecorder object on the cell
stim = None             # the IClamp object on the cell (MUST BE SET MANUALLY)

### Globals ###

#def setdx(self,dx):
#    self.m.dx = dx
#    self.m._normalize()
#
#def getdx(self,dx):
#    return self.m.dx


TSTOP = None            # the simulation's tstop, should be considered read-only
                        # in future iterations this may be depreciated
#dx = property(setdx, getdx)
#                        # the cell's dx, (yes, in terms of lambda)
#                        # Setting it will automatically normalize the nseg in m

dt = pow(2,-6)          # the dt that will be used to model the simulation after steady
                        # state is reached


def setup_aprec(cell = m, prop_site = None, ran = None): 
    '''automatically puts an APRecorder at the center of the cell's 'prop_site' section'''
    global aprec
    if prop_site is None:
        prop_site = m.prop_site
    if ran is not None:
        args = (prop_site, ran)
    else:
        args = (prop_site)
    aprec = APRecorder(*args)

def set_gbar(gbar):
    for sec in m.soma.wholetree():
        try:
            sec.gbar_nafTraub = gbar
            sec.gbar_kdrTraub = gbar
        except AttributeError:
            pass

def prerun(gbar, steadydur = None):
    set_gbar(gbar)
    if steadydur is None:
        steadydur = STEADYDUR
    h.dt = STEADYDT
    h.finitialize(-69)
    h.t = 0 - abs(STEADYDUR)
    h.continuerun(0)
    h.dt = dt

def proptest_basic(gbar):
    prerun(gbar)
    h.continuerun(TSTOP)
    return aprec.proptest()

def fullsolve(a, err, acc, maxsteps = 45, tstop_init = None):
    '''
    do a full gnathresh search on the experimental cell, m, expecting a solution in
    the range (a-err, a+err),
    returns an estimated solution within acc/2 of true solution
    self-halts after maxsteps iterations,
    use tstop-init if providing a relatively deep estimate
    see globals SHAPECONFIG and PRINTTIME for extra options
    '''
    ptstart = time.process_time()
    if tstop_init is None:
        tstop = stim.delay + APTRAVELTIME
    else:
        tstop  = tstop_init
    if SHAPECONFIG is not None:
        SHAPECONFIG()
    search = ExpandingSearch(a - err, a + err, proptest_basic, lim_lo = 0, lim_hi = 0.45)
    for i in range(maxsteps):
        if fullsolveiter(search, tstop, acc):
            break
    if PRINTTIME:
        print(time.process_time() - ptstart)
    if i == maxsteps - 1:
        print("WARNING!!! U REACHED THWE MAX STEPS!!")
    if abs(search.a - a) > 4*err:
        print("true error exceeded 4 times expected:" + str(search.a - a))
    return search.a

def fullsolveiter(search, tstop, acc):
    """designed to iterate a step of the search in fullsolve
    returns 1 if search must be halted due to going out of bounds
    returns 2 if accuracy has been achieved
    """
    global TSTOP
    TSTOP = tstop
    if search.searchstep():
        return 1
    if aprec.proptest():
        if aprec.proptest() > 1:
            print("double propogation detected")
        if aprec.recorded[0] > tstop - TSTOPSAFETY:
            tstop += TSTOPINCREMENT
    if search.hi - search.lo <= acc:
        return 2
    return 0


