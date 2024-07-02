# Lucas Swanson -- Ripon College '24
""" adopt(ed )eq(uations)
this file contains all equations that come from cited sources, old code, etc...
It just contains equations, okay?
"""
from math import  sqrt as __sqrt__

def alphagammataper(
        IS_diam,
        s_ratio,
        ell_c 
        ):
    """Legacy equation to get taper dimensions, alledgedly creates a section with electrotonic length ell_c, but I find this hard to believe."""
        
    alpha=                          \
            ((
                    (__sqrt__(s_ratio)-1)
                    / (s_ratio-1))
                ** 4)               \
            / (25**4
                * 100 * IS_diam**2)

    gamma=                          \
            IS_diam**2              \
            * (s_ratio-1)**2        \
            / 4

    taper =                         \
            __sqrt__(
                - gamma/2 
                + __sqrt__(
                    alpha**2 
                    * gamma**2
                    + 4 * alpha * ell_c**4
                    )
                / (2*alpha)
            )
    return alpha, gamma, taper

def elength(sec, d = None): 
    """ // calculate the electrotonic length as given by Tuckwell p. 137 
    Keyword arguments:
        sec                     The section from which diam, g_pas, and Ra is referenced
        d = None                (optional) Override the diam taken from sec
    """
    if d is None:
        d = sec.diam
    g_pas = sec.g_pas
    Ra = sec.Ra
    return __sqrt__(d/(Ra*g_pas))*50 #*0.5*100 # // 100 is for conversion to um
    #simplified expression by changing *0.5*100 for *50

def gr(d_parent, *args):
    """calculate geometric ratio w/ parent branch diameter followed by daughter branch diameters
    Arguments:
        d_parent                Parent branch diameter
        *args                   diameters of daughter branches
    """
    return(
            sum(
                [pow(d_i, 1.5) for d_i in args]
                )
            ) / pow(d_parent, 1.5)

def normalize_dlambda(sec, dx = 1): 
    """normalize the nseg of section sec such that segments are no more than dx*lambda, where lambda is the electronic length unit""" 
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
