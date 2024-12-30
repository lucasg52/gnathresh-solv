from .basic import BasicEnviro

class DeathEnviro(BasicEnviro):
    '''
    ### Options ###
    
    PRINTTIME = False       # Prints the runtime of fullsolve if True
    
    STEADYDUR = 200         # simulation time for calculating steady state
    
    STEADYDT =  pow(2, -2)  # the dt used to reach a steady state
    
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
    def __init__(self, cell, deathrec, stim, **kwargs):
        #NOTE: second argument is not an APRecorder anymore
        super().__init__(cell, deathrec, stim, **kwargs)
        self.deathrec = self.aprec # simply realiasing it in the args and attributes
        del self.TSTOP  # simulation stops automatically based on channel activity

    def proptest(self, gbar):
        self.prerun(gbar)
        self.deathrec.run()
        return self.deathrec.proptest()

    def fullsolve(self, *args, maxsteps = 45):
        return(super().fullsolve(*args, maxsteps = maxsteps, tstop_init = 0))

    def fullsolveiter(self, search, tstop, acc):
        if search.searchstep():
            return 1
        if search.hi - search.lo <= acc: # NOTE: unable to detect double propagations
            return 2
        return 0
