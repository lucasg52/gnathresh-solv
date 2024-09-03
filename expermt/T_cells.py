from cells.rincell import Rin_Tcell, RinCell
from Tools.Rin_funcs import gna_run, rin_run, graph
from neuron import h
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

# file for the Shifting T cells experiment
#all functions used come form the Rin_funcs file in tools

__MAXGBAR__ = 0.3
__tstop__ = h.tstop = 15
h.dt = pow(2,-6)

#setting up the cell
t = Rin_Tcell(1)
t.setup_stim()
t.side1.L = 3 * elength(t.side1)
t._normalize()

#creating lists of lengths and locations
len_lst = [i/100 for i in range(10, 610, 10)]
lab_lst = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,1]
label_lst = [0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0]
cell_lst = [t for x in range(len(lab_lst))]

#creating lists for creating and calling .npy files housing the corresponding collected data
gna_lst = ['t_0_gna_6l_tak4', 't_01_gna_6l_tak4','t_02_gna_6l_tak4',
          't_03_gna_6l_tak4','t_04_gna_6l_tak4','t_05_gna_6l_tak4','t_06_gna_6l_tak4',
          't_07_gna_6l_tak4','t_08_gna_6l_tak4', 't_09_gna_6l_tak4', 't_1_gna_6l_tak4']
gna2_lst = ['t_0_gna_6l_tak4.npy', 't_01_gna_6l_tak4.npy','t_02_gna_6l_tak4.npy','t_03_gna_6l_tak4.npy',
            't_04_gna_6l_tak4.npy','t_05_gna_6l_tak4.npy','t_06_gna_6l_tak4.npy', 't_07_gna_6l_tak4.npy',
            't_08_gna_6l_tak4.npy', 't_09_gna_6l_tak4.npy', 't_1_gna_6l_tak4.npy']
gna3_lst = ['t_0_gna_6l_tak3.npy', 't_01_gna_6l_tak3.npy','t_02_gna_6l_tak3.npy','t_03_gna_6l_tak3.npy',
            't_04_gna_6l_tak3.npy','t_05_gna_6l_tak3.npy','t_06_gna_6l_tak3.npy', 't_07_gna_6l_tak3.npy',
            't_08_gna_6l_tak3.npy', 't_09_gna_6l_tak3.npy', 't_1_gna_6l_tak3.npy']
rin_lst = ['t_0_rin_6l_tak4', 't_01_rin_6l_tak4','t_02_rin_6l_tak4',
          't_03_rin_6l_tak4','t_04_rin_6l_tak4','t_05_rin_6l_tak4','t_06_rin_6l_tak4',
          't_07_rin_6l_tak4','t_08_rin_6l_tak4', 't_09_rin_6l_tak4', 't_1_rin_6l_tak4']
rin2_lst = ['t_0_rin_6l_tak3.npy', 't_01_rin_6l_tak3.npy','t_02_rin_6l_tak3.npy','t_03_rin_6l_tak3.npy',
            't_04_rin_6l_tak3.npy','t_05_rin_6l_tak3.npy','t_06_rin_6l_tak3.npy', 't_07_rin_6l_tak3.npy',
            't_08_rin_6l_tak3.npy', 't_09_rin_6l_tak3.npy', 't_1_rin_6l_tak3.npy']
rin3_lst = ['t_0_rin_6l_tak5.npy', 't_01_rin_6l_tak5.npy','t_02_rin_6l_tak5.npy',
          't_03_rin_6l_tak5.npy','t_04_rin_6l_tak5.npy','t_05_rin_6l_tak5.npy','t_06_rin_6l_tak5.npy',
          't_07_rin_6l_tak5.npy','t_08_rin_6l_tak5.npy', 't_09_rin_6l_tak5.npy', 't_1_rin_6l_tak5.npy']