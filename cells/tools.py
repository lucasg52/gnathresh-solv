from neuron import h

# If you want something added to this file, please implement it in a different file or different branch first
class APRecorder():
    def __init__ (
            self,
            sec,
            ran = 0.5
            ):
        self.recorded = False
        self.nc = h.NetCon(sec(ran)._ref_v, None, sec = sec)
        self.nc.record(self._record)
    def _record(self):
        #print(str(self) + "recorded an AP")
        self.recorded = True
    def proptest(self):
        ret = self.recorded
        self.recorded = False
        return ret
