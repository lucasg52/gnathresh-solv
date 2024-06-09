#Lucas Swanson -- Ripon College '27

import numpy as np

def countcols(fp, wordnum = 0, wordsep = '\t'):
    first = None
    i = 0
    for line in fp:
        lsep = line.split(wordsep)
        if first is not None:
            if first != lsep[wordnum]:
                break
            else:
                first = lsep[wordnum]
        i = i+1

def torectarr(filename, cols = None, wordnum = 2, wordsep = '\t'):
    if cols is None: 
        fp = open(filename, 'r')
        cols = countcols(fp)
        fp.close()
    fp = open(filename, 'r')
    i = 0
    rowarr = []
    rectarr = []
    for line in fp:
        lsep = line.split(wordsep)
        rowarr.append(float(lsep[wordnum]))
        if (i % cols) == (cols - 1):
            rectarr.append(rowarr)
            rowarr = []
        i +=1
    fp.close()
    return rectarr

def tonparr(filename, cols = None, wordnum = 2, wordsep = '\t'):
    return np.array(torectarr(filename, cols = cols, wordnum = wordnum, wordsep = wordsep))
