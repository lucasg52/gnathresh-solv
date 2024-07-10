from neuron import h
class APRecorder():
    """Record ap spikes at sec(ran)"""
    def __init__ (
            self,
            sec,
            ran = 0.5
            ):
        self.recorded = h.Vector()
        self.nc = h.NetCon(sec(ran)._ref_v, None, sec = sec)
        self.nc.record(self.recorded)

    def proptest(self):
        """returns len(self.recorded)"""
        ret = len(self.recorded)
        return ret
