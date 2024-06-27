from neuron import h
import numpy as np
from neuron import h
from math import sqrt
import kinetics_transcribe as kin
import adoptedeq as eq


class ExpcellTemplate:
    def __init__(
            self,
            dx,
            ratio,
            layer,
            n_cells,
            *args,
            gid = 0,
            kinetics = 0
            ):
        self.dx = dx # i belive this is the only paramater that really matters (for now)
        self.ratio = ratio

        self.soma = h.Section(          name = "soma")
        self.IS = h.Section(            name = "IS")
        self.main_shaft = h.Section(    name = "main_shaft")
        #self.extstim_site = h.Section(  name = "extstim_site")
        #self.junction_site = h.Section( name = "junction_site" )
                # these are unused since in the original code, they are destroyed if lengths d2 and d3 are not provided
        self.prop_site = h.Section(     name = "prop_site")


        self.main_diam = 0.6
        self.IS_diam = 1.6
        self.s_ratio = 12.5
        self.ell_c = 0.015
        self.stim1 = None
        self.stim2 = None

        if(layer==2): # // estimate parameters based on cell reconstructions
            self.main_diam = 0.6
            self.IS_diam = 1.2
            self.s_ratio = 14
            self.ell_c = 0.015
        elif(layer==4):
            self.main_diam = 0.6
            self.IS_diam = 1.5
            self.s_ratio = 11.2
            self.ell_c = 0.015
        elif(layer==5):
            self.main_diam = 1.2
            self.IS_diam = 2
            self.s_ratio = 11.4
            self.ell_c = 0.02
        else: # // use averages for all cells
            print ("Invalid layer: Using guessed averages for cell parameters!")
        #main_diam = self.main_diam 
        IS_diam =   self.IS_diam
        s_ratio =   self.s_ratio
        ell_c =     self.ell_c  
        self.soma_diam = s_ratio*IS_diam
        
        if(kinetics==1):
            self.main_length = 4
        else:
            self.main_length = 8 # // electronic length of main shaft
        # this entire section below I am considering tossing it in adoptedeq.py
        self.alpha=                     \
                ((
                    (sqrt(s_ratio)-1)
                    /
                    (s_ratio-1)
                )**4)                   \
                /                       \
                (
                    25**4
                    *
                    100 *
                    IS_diam**2
                )
        alpha = self.alpha

        self.gamma=                     \
                IS_diam**2              \
                *                       \
                (s_ratio-1)**2          \
                /4
        gamma = self.gamma

        self.taper =                    \
                sqrt(
                    -gamma/2 +
                    sqrt(
                        alpha**2
                        *
                        gamma**2
                        +
                        4 * alpha * ell_c**4
                        )
                    /
                    (2*alpha)
                )

        self._setup_biophysics()
        self._setup_morphology()
    def _setup_biophysics(self):
        kin.insmod_Traub(self.soma,         "soma")
        kin.insmod_Traub(self.main_shaft,   "axon")
        kin.insmod_Traub(self.IS,           "axon")
        kin.insmod_Traub(self.prop_site,    "axon")
    def normalize_dx(self): # line 166, not clear why some sections get normalized differently. so I am just assuming it is homogenous. also made my own subroutine 
        for sec in self.all:
            sec.nseg = int(sec.L/self.dx) + 1
    def _setup_morphology(self):

        #the following definitions for section diameter are taken from lines 89-105. 
        #self.soma.L = self.soma.diam = self.soma_diam
        #self.IS.L = 40 # line 98 
        #self.main_shaft.L = self.main_length * eq.elength(self.main_shaft, d = self.main_diam)
        self.main_shaft.diam = self.main_diam
        self.prop_site.diam = self.main_diam/self.ratio
        sec = self.soma
        h.pt3dadd(0,self.soma_diam,0,self.soma_diam, sec = sec)
        h.pt3dadd(0,0,0,self.soma_diam, sec = sec)
        sec = self.IS
        h.pt3dadd(0,0,0,self.soma_diam, sec = sec)
        # // taken from TypicalCell's geometry
        h.pt3dadd(0,-self.taper,0,self.IS_diam, sec = sec)
        h.pt3dadd(0,-40,0,self.main_diam)	
        sec = self.main_shaft
        h.pt3dadd(0,-40,0,self.main_diam, sec = sec)
        h.pt3dadd(0,-40 -self.main_length*eq.elength(sec, d = self.main_diam),0,self.main_diam, sec = sec)
        #self.IS.connect(self.soma(1))
        #self.main_shaft.connect(self.IS(1)) # (line 107)
        #self.prop_site.connect(self.main_shaft(0)) # connections must be made first for self.all to be correct
        self.all = self.soma.wholetree()
        self.normalize_dx() # technically this is executed at the end

    def set_soma_leak(cell, e, g): # (simulation_base_com.hoc line 457; vs-expcell.hoc line 34, ) // Set soma leak/passive current 
        # why tf was this a subroutine in the old code...? well here it is reimagined in python in all two lines of its glory
        cell.soma.e_pas = e
        cell.soma.g_pas = g

    def set_extim_site(self, sec): # i have genuinely no idea what the old code was supposed to do with the paramaters, so this will have none.
        self.stim1 = h.IClamp(sec(0.5))
        self.stim2 = h.IClamp(sec(0.5))
        self.stim1.__setattr__("del", 5) 
        self.stim2.__setattr__("del", 10)
        self.stim1.amp = self.stim2.amp = 0.2
        self.stim1.dur = self.stim2.dur = 0.3125


