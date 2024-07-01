from matplotlib import pyplot as plt
def searchreset(a, err):
    hi = a + err
    lo = a - err
    search = searchclasses.GNASearch(lo, hi, proptest)

def fullsolve(steps = 12, a = 0.5, err = 0.5):
    searchreset()
    for i in range(steps):
            search.searchstep(a, err)
    return search.a


results = []
for i, seg in enumerate(m.main_shaft):
    plate = [seg.x]
    m.prop_site.connect(seg)
    plate.append(fullsolve(a = ypnts[i], err = pow(2, -10)))
    results.append(tuple(plate))

xpnts = [x for x,y in results]
ypnts = [y for x,y in results]
plt.plot(xpnts,ypnts)

pass
