import numpy as np
from cells.rincell import RinCell
from Tools.Rin_funcs import gna_run, rin_run, graph
from Tools.environment import DeathEnviro
from Tools.apdeath import DeathRec
from neuron import h
import time
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

h.dt = pow(2,-6)

b = RinCell(1)
b.setup_stim()
b.side1.L = 3 * elength(b.side1)
b._normalize()

# deathrec = DeathRec(b.main_shaft, b.prop_site, 6)
# e = DeathEnviro(b, deathrec, b.stim)
# e.prerun = b.prerun


# loc_lst = [i/100 for i in range(0, 100,10)]
len_lst = [i/100 for i in range(0, 610, 10)]
lab_lst = [0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,1]
label_lst = [0.4, 0.8, 1.2, 1.6]
label_lst2 = [0.0, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
gna_lst = ['base_0_gna_6l_tak3','base_01_gna_6l_tak2','base_02_gna_6l_tak2',
          'base_03_gna_6l_tak2','base_04_gna_6l_tak2','base_05_gna_6l_tak2','base_06_gna_6l_tak2',
          'base_07_gna_6l_tak2','base_08_gna_6l_tak2', 'base_09_gna_6l_tak2', 'base_1_gna_tak2']
gna2_lst = ['base_01_gna_6l_tak2.npy','base_02_gna_6l_tak2.npy','base_03_gna_6l_tak2.npy','base_04_gna_6l_tak2.npy']
gna3 = ['base_0_gna_6l_tak3.npy','base_05_gna_6l_tak2.npy','base_06_gna_6l_tak2.npy', 'base_07_gna_6l_tak2.npy',
        'base_08_gna_6l_tak2.npy', 'base_09_gna_6l_tak2.npy', 'base_1_gna_tak2.npy']

rin_lst = ['base_0_rin_6l_tak3','base_01_rin_6l_tak3','base_02_rin_6l_tak3',
          'base_03_rin_6l_tak3','base_04_rin_6l_tak3','base_05_rin_6l_tak3','base_06_rin_6l_tak3',
          'base_07_rin_6l_tak3','base_08_rin_6l_tak3', 'base_09_rin_6l_tak3', 'base_1_rin_tak3']
rin2_lst = ['base_01_rin_6l_tak3.npy','base_02_rin_6l_tak3.npy','base_03_rin_6l_tak3.npy','base_04_rin_6l_tak3.npy']
rin3 = ['base_0_rin_6l_tak3.npy','base_05_rin_6l_tak3.npy','base_06_rin_6l_tak3.npy', 'base_07_rin_6l_tak3.npy',
            'base_08_rin_6l_tak3.npy', 'base_09_rin_6l_tak3.npy', 'base_1_rin_tak3.npy']
cell_lst = [b for x in range(4)]
cell2 = [b for y in range(7)]