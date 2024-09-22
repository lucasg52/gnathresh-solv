#import necessary libraries, cells, and functions
from cells.rincell import Rin_Tcell
from Tools.Rin_funcs import gna_run, rin_run, graph2
from neuron import h
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

# file for the Shifting T cells experiment

__MAXGBAR__ = 0.3
__tstop__ = h.tstop = 15
h.dt = pow(2,-6)

#setting up the cell
t = Rin_Tcell(1)
t.setup_stim()
t.side1.L = 3 * elength(t.side1)
t._normalize()

#creating lists of lengths and locations
len_lst = [i/100 for i in range(10, 610, 10)] #used to change the lengths of the sub-branch
pos_lst = [j/10 for j in range(0,11,1)] #used to move the location of the sub-branch
label_lst = [3*k/10 for k in range(0,11,1)] #used when creating the legend for the graph
cells = [t for x in range(len(pos_lst))] #used to iterate through the graphing function

#creating lists for creating and calling .npy files housing the corresponding collected data

#list for collecting gna
gna_lst = ['t_0_gna_6l_tak3']
for i in range(1,10):
    gna_lst.append(f't_0{i}_gna_6l_tak3')
gna_lst.append('t_1_gna_6l_tak3')

#list for accessing the gna data
gna2_lst = ['../modfiles/t_0_gna_6l_tak3.npy']
for i in range(1,10):
    gna2_lst.append(f'../modfiles/t_0{i}_gna_6l_tak3.npy')
gna2_lst.append('../modfiles/t_1_gna_6l_tak3.npy')


#list for collecting rin
rin_lst = ['t_0_rin_6l_tak3']
for i in range(1,10):
    rin_lst.append(f't_0{i}_rin_6l_tak3')
rin_lst.append('t_1_rin_6l_tak3')

#list for accessing the rin data
rin2_lst = ['../modfiles/t_0_rin_6l_tak3.npy']
for i in range(1,10):
    rin2_lst.append(f'../modfiles/t_0{i}_rin_6l_tak3.npy')
rin2_lst.append('../modfiles/t_1_rin_6l_tak34.npy')

def main(test): #runs the experiment; the test input indicates which test you want to do
    if test == 'gna':
        gna_run(t, t.dau1, t.side1, pos_lst, len_lst, gna_lst)
    elif test == 'rin':
        rin_run(t, t.dau1, t.side1, pos_lst, len_lst, rin_lst)
    elif test == 'graph': #the graphing function requires manual modifications reflecting what you want graphed
        graph2(cells, rin2_lst, gna2_lst)
        #if graphing with the legend:
        #graph2(cells, rin2_lst, gna2_lst, lab_lst, 'Shifting T-Cells')