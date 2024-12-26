from neuron import h

RVARPLOT = None
GRAPH = None
STEPTIME = 0.25
STARTTIME = 0
ENDCMD = 'q'
MAXSTEPS = 15

def setup(m = None, start = None, end = None, varname  ='v'):
    global RVARPLOT, GRAPH
    if GRAPH is not None:
        del GRAPH
    if RVARPLOT is not None:
        del RVARPLOT
    if m is not None:
        start = m.soma(0)
        end = m.prop_site(1)
    RVARPLOT = h.RangeVarPlot(varname, start, end)
    GRAPH = h.Graph()
    GRAPH.addobject(RVARPLOT)

def prerun():
    pass

def run():
    GRAPH.flush()
    from neuron import gui
    prerun()
    for i in range(MAXSTEPS):
        if ENDCMD in input():
            break
        step()

def step():
    h.continuerun(h.t + STEPTIME)
    GRAPH.flush()

