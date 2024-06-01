import numpy as np
from searchclasses import GNASearch as BinSearch
import math

def find_crit_vals_basic(nparr):
    #finds critical values for a numpy array by finding points where the first difference (delta_arr) crosses zero
    delta_arr = np.diff(nparr,1)
    iprev = -1
    ret = []
    ind = 0
    for i in delta_arr:   
        if iprev*i < 0:
            ret.append((ind, nparr[ind]))
        ind += 1
        iprev = i
    return ret


def find_zeros_bins(
    #finds ranges (bins) of entries in nparr where zero is crossed
        nparr,  
        spread = 1, #the size of the bins
        start = 0, #the lower bound of the first possible bin
        minmax = 1 #a value of -1 finds negative to positive crossings, a value of 1 does the opposite
    ):
    minmax_dict = {"min":-1, "max":1}
    if minmax in minmax_dict:
        minmax = minmax_dict[minmax]
    assert (spread >= 1)
    assert (start >= 0)
    assert (minmax in [-1,1])
    
    i = int(start)
    prev = 0
    prevval = -1
    searchbins = []
    while i < len(nparr):
        curr = nparr[i]
        if (minmax * prevval) > 0 and (minmax * curr) < 0:
            searchbins.append((
                prev, i,
                lambda a : nparr[round(a)] * minmax < 0
            ))
        prevval = nparr[i]
        prev = i
        i += spread

    return searchbins

def eval_zero_bins (searchbins, iters):
    ret = []
    for bargs in searchbins:
        s = BinSearch(*bargs)
        sol = math.nan
        for i in range(iters):
            sol =math.nan 
            s.searchstep()
            if (s.lo - s.hi) <= 1:
                sol = int(s.a)
                break

        ret.append(sol)

    return ret


def find_crit_vals_heuristic(
        nparr,
        iters, 
        spread = 4, 
        start = 0, 
        minmax = 1):
    delta_arr = np.diff(nparr,1)
    searchbins = find_zeros_bins(delta_arr, spread, start, minmax)
    return(
        [
            (x, nparr[x]) for x in 
            eval_zero_bins(searchbins, iters)
        ]
    )

