from .basic import BasicEnviro

class DeathEnviro(BasicEnviro):
    #__doc__ = AbstractEnviro.__doc__ + "\nDue to using a deathrec, this is unable to detect double-propagations"
    #DeathEnviro: An environment for solving using a DeathRec (AP death recorder)
    #Unlike BasicEnviro, proptest() automatically waits for membrane activity to die down before halting simulation.
    def __init__(self, m, deathrec, stim, **kwargs):
        #NOTE: second argument is not an APRecorder anymore
        super().__init__(m, deathrec, stim, **kwargs)
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
