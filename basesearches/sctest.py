from searchclasses import GNASearch, ExpandingSearch
def gna(x):
    return (x > 100)

g = GNASearch(0,1000,gna)
g.searchstep()

e = ExpandingSearch(500,600,gna,0,1000)

