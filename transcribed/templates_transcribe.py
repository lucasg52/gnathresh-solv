#Lucas Swanson -- Ripon College '27

#transcribed from Beloit_axon_propagation/expcell_templates.hoc
#original comments start with HOC's double-slash
import numpy as np
from neuron import h
from math import sqrt
import kinetics_transcribe as kin
import adoptedeq as eq



#axon = dict()
#soma = dict()
# original code organized sections into dictionary-like objects that I believe neuronHOC parses through w/ keyword "forsec", and takes the different dictionaries as diffeent catagories of sections (axon, dendrite, soma). I decided that this was not worth the hassle to implement an equivalent in python since only two dictionaries are used. 
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
        self.IS = h.Section(            name = "IS")
        self.main_shaft = h.Section(    name = "main_shaft")
        #self.extstim_site = h.Section(  name = "extstim_site")
        #self.junction_site = h.Section( name = "junction_site" )
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
        #god yall code is ugly *smh*
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
        map(lambda args : kin.insmod_Traub(*args),
                (self.soma,         "soma"),
                (self.main_shaft,   "axon"),
                (self.IS,           "axon"),
                (self.prop_site,    "axon"))
    def normalize_dx(self): # line 166, not clear why some sections get normalized differently. so I am just assuming it is homogenous. also made my own subroutine 
        for sec in self.all:
            sec.nseg = int(sec.L/self.dx) + 1
    def taper_IS(self):
        taper = self.taper
        taperpnt = int((taper / self.IS.L) * self.IS.nseg)
        taperarr = np.concatenate((
                np.linspace(self.soma_diam, taper, taperpnt),
                np.linspace(taper, self.main_diam, self.IS.nseg - taperpnt)
                ))
        i = 0
        for seg in self.IS:
            seg.diam = taperarr[i]
            i = i+1


        #for seg in self.IS:
        #    x = seg.x
        #    if x < taper:
        #        seg.diam = ((1-(x/ taper)) * (soma_diam)    \
        #                +                                   \
        #                (x/ taper) * (IS_diam))             \
        #                / 2
        #    else:
        #        seg.diam = ((1-(x/ taper)) * (soma_diam)    \
        #                +                                   \
        #                (x/ taper) * (IS_diam))             \
        #                / 2

    def _setup_morphology(self):
        self.IS.connect(self.soma(1))
        self.main_shaft.connect(self.IS(1)) # (line 107)
        self.prop_site.connect(self.main_shaft(0)) # connections must be made first for self.all to be correct
        self.all = self.soma.wholetree()
        #the following definitions for section diameter are taken from lines 89-105. 
        self.soma.L = self.soma.diam = self.soma_diam
        self.IS.L = 40 # line 98 
        self.main_shaft.L = self.main_length * eq.elength(d = self.main_diam)
        self.normalize_dx() # technically this is executed at the end
        self.taper_IS() # this was implimented entirely on my own discretion since the old code seemed to be letting neuron taper it using pt3dadd... and they also normalized dx afterwards, which seems like a bad idea since it would probably just rebin the segment diameters 







    def set_soma_leak(cell, e, g): # (simulation_base_com.hoc line 457; vs-expcell.hoc line 34, ) // Set soma leak/passive current 
        # why tf was this a subroutine in the old code...? well here it is reimagined in python in all two lines of its glory
        cell.soma.e_pas = e
        cell.soma.g_pas = g

    def set_extim_site(self, sec):# i have genuinely no idea what the old code was supposed to do with the paramaters, so this will have none.
        self.stim1 = h.IClamp(sec(0.5))
        self.stim2 = h.IClamp(sec(0.5))
        self.stim1.__setattr__("del", 5) 
        self.stim2.__setattr__("del", 10)
        self.stim1.amp = self.stim2.amp = 0.2
        self.stim1.dur = self.stim2.dur = 0.3125


class Expcell_demo(ExpcellTemplate):
    def __init__(self, *args):
        super().__init__(*args)
        self.set_soma_leak(
                -70, # (vs-expcell.hoc, line 17)// somatic voltage, options are typically -80, -70, -60
                0.002 # (vs-expcell.hoc, line 34)
                )
        self.set_extim_site(self.prop_site)


        

    
    
    
    
    
           
