#Lucas Swanson -- Ripon College '27

import numpy as np
def toarr_axis(
        filename,
        dep_wordnum, #which column of the file the dependant value/data member lies in
        *axis_wordnums, #the columns that contain the axis variables (independant vars)
        wordsep = '\t', #the seperator of columns
        emptyval = float(0) #the placeholder value used in the output array (for unfilled dependant var vals)
        #MUST BE FLOAT
        ):
    fp = open(filename, 'r')
    axisvals = [set() for i in axis_wordnums]
    for line in fp:
        try:
            lsep = line.split(wordsep)
            i = 0
            for wordnum in axis_wordnums:
                axisvals[i].add(float(lsep[wordnum]))
                i += 1
        except Exception:
            print("toarr_axis: skipped line:" + line)

    axisvals = [list(s) for s in axisvals]
    for s in axisvals:
        s.sort()
    fp.close()
    fp = open(filename, 'r')
    
    data = np.tile(
            emptyval,
            tuple(
                [len(s) for s in axisvals]
            )
    )
    for line in fp:
        lsep = line.split(wordsep)
        coord = []
        ii = 0
        for wordnum in axis_wordnums:
            coord.append(
                    axisvals[ii].index(
                        float(lsep[wordnum])
                    )
            )
            ii +=1
        data[tuple(coord)] = float(lsep[dep_wordnum])

    fp.close()
    return data, axisvals



def countcols(fp, wordnum = 0, wordsep = '\t'):
    first = None
    i = 0
    for line in fp:
        lsep = line.split(wordsep)
        if first is not None:
            if first != lsep[wordnum]:
                print(i)
                print(line)
                break
        else:
            first = lsep[wordnum]
        i = i+1
    return i

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
