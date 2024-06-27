# Lucas Swanson -- Ripon College '24
# adopt(ed )eq(uations)
# this file contains all equations that come from cited sources

from math import sqrt
#
#def alpha(**kwargs):
#    return(((
#                    (sqrt(kwargs['s_ratio'])-1)
#                    /
#                    (kwargs['s_ratio']-1)
#                )**4)                   \
#                /                       \
#                (
#                    25**4
#                    *
#                    100 *
#                    kwargs['IS_diam']**2
#            ))

def elength(sec = None, d = None): # // calculate the electrotonic length as given by Tuckwell p. 137
    if d is None:
        d = sec.diam
    g_pas = sec.g_pas
    Ra = sec.Ra
    return sqrt(d/(Ra*g_pas))*50 #*0.5*100 # // 100 is for conversion to um
    #simplified expression by changing *0.5*100 for *50

def gr(d_parent, *args): # calculate geometric ratio w/ parent branch diameter followed by daughter branch diameters
    return(
            sum(
                [pow(d_i, 1.5) for d_i in args]
                )
            ) / pow(d_parent, 1.5)

def normalize_dlambda(sec, dx = 1): 
    print(f"dx = {dx}")
    sec.nseg =  \
        int(
            sec.L/
            (
                dx *
                elength(
                    sec,
                    d = sec.diam
                    #d = min(sec(0).diam, sec(1).diam) # doesn't work as intended for 3d tapers
                )
            )
        ) + 1
