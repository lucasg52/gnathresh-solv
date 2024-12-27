import time
from warnings import warn
from neuron import h
from ..tools.aprecorder import APRecorder
from ..solver.searchclasses import ExpandingSearch
from .base import AbstractEnviro

class BasicEnviro(AbstractEnviro):
    '''
    ### Options ###
    
    PRINTTIME = False       # Prints the runtime of fullsolve if True
    
    STEADYDUR = 200         # simulation time for calculating steady state
    
    STEADYDT =  pow(2, -2)  # the dt used to reach a steady state
    
    APTRAVELTIME = 10       # expected time it takes for AP to travel normally
    
    TSTOPSAFETY = 6         # maximum amount of sim time allowed between ap propagation and
                            # end of simulation
                            # in future iterations this may be depreciated
    
    TSTOPINCREMENT = 3      # amount of sim time added (when nescessary) as search deepens
    
    MAXGBAR = 0.45          # maximum gbar for search (search will not go above this value)
    
    MINGBAR = 0.1           # minimum gbar for search (search will not go below this value)

    SEARCH_RAD_WARN = 4     # multiple of search radius beyond which solutions will trigger
                            # warnings (see fullsolve)
    
    ### Objects ###
    
    cell = None                # the cell to do experiments on
    aprec = None            # the APRecorder object on the cell
    stim = None             # the IClamp object on the cell (MUST BE SET MANUALLY)
    
    ### Globals ###
    
    TSTOP = None            # the simulation's tstop, should be considered read-only
                            # in future iterations this may be depreciated
    
    dt = pow(2,-6)          # the dt used in the simulation after steady state is reached
    '''

    
    def _init_options(self, **kwargs):
        ### Options ###
        self.PRINTTIME = False       # Prints the runtime of fullsearch if True
        self.STEADYDUR = 200         # simulation time for calculating steady state
        self.STEADYDT =  2           # the dt used to reach a steady state
        self.APTRAVELTIME = 10       # expected time it takes for AP to travel normally
        self.TSTOPSAFETY = 6         # maximum amount of sim time allowed between ap propagation and 
                                # end of simulation
                                # in future iterations this may be depreciated
        self.TSTOPINCREMENT = 3      # increment for increasing tstop
        self.MAXGBAR = 0.45          # maximum gbar for search (search will not go above this value)
        self.MINGBAR = 0.1
        self.SEARCH_RAD_WARN = 4
        
        self.savestate = h.SaveState()
        self.savestategbar = -1
        
        self.TSTOP = None            # the simulation's tstop, should be considered read-only
                                # in future iterations this may be depreciated
        
        
    def setup_aprec(self, cell = None, prop_site = None, ran = None): 
        '''automatically puts an APRecorder at the center of the cell's 'prop_site' section'''
        if cell is None:
            cell = self.cell
        if prop_site is None:
            prop_site = cell.prop_site
        if ran is not None:
            args = (prop_site, ran)
        else:
            args = (prop_site)
        self.aprec = APRecorder(*args)

    def prerun(self,gbar, steadydur = None):
        self.set_gbar(gbar)
        if steadydur is None:
            steadydur = self.STEADYDUR
        h.dt = self.STEADYDT
        h.finitialize(-69)
        h.t = 0 - abs(self.STEADYDUR)
        h.continuerun(0)
        h.dt = self.dt

    #def prerun(self, gbar, steadydur = None):
    #    if self.savestategbar == gbar:
    #        self.savestate.restore()
    #    else:
    #        self.newprerun(gbar, steadydur = steadydur)
    def proptest(self, gbar):
        self.prerun(gbar)
        h.continuerun(self.TSTOP)
        return self.aprec.proptest()
    
    def fullsolve(self, est, rad, acc, maxsteps = 45, tstop_init = None):
        '''
        do a full gnathresh search using self.stim as the stimulus and self.aprec as the
        propagation test-site, expecting a solution in the range (est-rad, est+rad).
        returns an estimated solution within acc/2 of true solution.
        self-halts after maxsteps iterations.
        use tstop-init if providing a relatively deep estimate

        External Options:
        SEARCH_RAD_WARN determines how far outside of the search radius a solution can be before
        triggering a warning. That is, if the difference between the true solution
        and est is greater than SEARCH_RAD_WARN*rad, a warning is printed.
        see options SHAPECONFIG and PRINTTIME for extra configuration
        '''
        ptstart = time.process_time()
        if tstop_init is None:
            tstop = self.stim.delay + self.APTRAVELTIME
        else:
            tstop  = tstop_init
        search = ExpandingSearch(
                est - rad, est + rad, self.proptest, 
                lim_lo = self.MINGBAR, lim_hi = self.MAXGBAR)
        for i in range(maxsteps):
            if self.fullsolveiter(search, tstop, acc):
                break
        if self.PRINTTIME:
            print(time.process_time() - ptstart)
        if i == maxsteps - 1:
            warn(
                    f"Threshold search halted after exceeding max number of steps ({maxsteps})",
                    Warning,
                    stacklevel = 2
                    )
        if abs(search.a - est) > self.SEARCH_RAD_WARN*rad:
            warn(
                    f"Solution found beyond {self.SEARCH_RAD_WARN}x search radius."
                    + " consider using a larger search radius or implement stronger estimation",
                    Warning,
                    stacklevel = 2
                    )
        return search.a
    
    def fullsolveiter(self, search, tstop, acc):
        """designed to iterate a step of the search in fullsolve
        returns 1 if search must be halted due to going out of bounds
        returns 2 if accuracy has been achieved
        """
        self.TSTOP = tstop
        if search.searchstep():
            return 1
        if self.aprec.proptest():
            if self.aprec.proptest() > 1:
                warn("double propagation detected", Warning)
            if self.aprec.recorded[0] > tstop - self.TSTOPSAFETY:
                tstop += self.TSTOPINCREMENT
        if search.hi - search.lo <= acc:
            return 2
        return 0
    


