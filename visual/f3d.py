from neuron import h
def reset3d(m): # doesnt even work
    for sec in m.all:
        if sec.n3d() < 0.5:
            print("3d info does not need to be reset, loop break at section:" + str(sec))
            return
        if sec.pt3dclear() < 0.5:
            print("failed to clear section 3d info because plotshape is open")

def autof3d(cell, ratio = 4, min = 50):
    sec = cell.main_shaft
    f = 0
    children = sec.children()
    if children:
        for sec in children:
            f += max(sec.diam * ratio, min)
            f3d(sec, f = f)
def autof3d0(tree, ratio = 4):
    f = 0
    for sec in tree:
        children = sec.children()
        if children:
            for sec in children:
                f += sec.diam * ratio
                f3d(sec, f = f)

def f3d(sec, f = 0):
    #if h.pt3dclear(sec = sec) > 0.5:
    #    print("ShapePlot must be closed to fuck 3d.")
    #else:
    if sec.n3d() < 1:
        print("how can one fuck 3d if there is no 3d?")
        return
    if f == 0:
        f = sec.L
    h.pt3dstyle(1, 0,f, 0, sec = sec)

