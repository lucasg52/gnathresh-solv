from neuron import h
from math import sqrt
import kinetics_transcribe as kin



axon = dict()
soma = dict()

class ExpcellTemplate:
    def __init__(
            self,
            kinetics,
            dx,
            ratio,
            layer,
            n_cells,
            gid = 0
            ):
        self.IS = h.Section(            name = "IS")
        self.main_shaft = h.Section(    name = "main_shaft")
        self.extstim_site = h.Section(  name = "extstim_site")
        self.junction_site = h.Section( name = "junction_site" )
        self.prop_site = h.Section(     name = "prop_site")
        self.main_diam = 0.6
        self.IS_diam = 1.6
        self.s_ratio = 12.5
        self.ell_c = 0.015
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

    def _setup_morphology(self):
        pass
    def _setup_biophysics(self):
        pass

    
    
    
    
    
           
