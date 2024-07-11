from matplotlib import pyplot as plt
import jun28
from jun28 import m, proptest, searchclasses
def searchreset(a, err):
    global search
    hi = a + err
    lo = a - err
    search = searchclasses.GNASearch(lo, hi, proptest)

def fullsolve(steps = 12, a = 0.5, err = 0.5):
    searchreset(a, err)
    for i in range(steps):
            search.searchstep()
    return search.a


results = []
xpnts = []
ypnts = []
def fullexperiment():
    global xpnts, ypnts
    for i, seg in enumerate(m.main_shaft):
        plate = [seg.x]
        m.prop_site.connect(seg)
        plate.append(fullsolve(15, pow(2,-5), pow(2,-6)))
        results.append(tuple(plate))

    xpnts = [x for x,y in results]
    ypnts= [y for x,y in results]

fullexperiment()
plt.plot(xpnts,ypnts)

