from neuron import h
class APRecorder():
    """Record ap spikes at sec(ran)"""
    def __init__ (
            self,
            sec,
            ran = 0.5
            ):
        self.recorded = False
        self.nc = h.NetCon(sec(ran)._ref_v, None, sec = sec)
        self.nc.record(self._record)
    def _record(self):
        """called by hoc during simulation when an AP is recorded"""
        #print(str(self) + "recorded an AP")
        self.recorded = True
    def proptest(self):
        """read self.recorded and reset it to False"""
        ret = self.recorded
        self.recorded = False
        return ret
