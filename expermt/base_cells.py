#import necessary libraries, cells, and functions
from cells.rincell import RinCell
from Tools.Rin_funcs import gna_run, rin_run, graph2
from neuron import h
from cells.adoptedeq import elength
h.load_file("stdrun.hoc")

#file for the Base Cable Experiment
h.dt = pow(2,-6)

#setting up the cell
b = RinCell(1)
b.setup_stim()
b.side1.L = 3 * elength(b.side1)
b._normalize()

# loc_lst = [i/100 for i in range(0, 100,10)]
len_lst = [i/100 for i in range(0, 610, 10)]
pos_lst = [j/10 for j in range(0,11,1)] #used to move the location of the sub-branch
label_lst = [4*k/10 for k in range(0,11,1)] #used when creating the legend for the graph
cells = [b for z in range(11)]

#creating lists for creating and calling files of data:
#lists for collecting gna
gna_lst = ['base_0_gna_6l_tak3']
for i in range(1,10):
    gna_lst.append(f't_0{i}_gna_6l_tak2')
gna_lst.append('t_1_gna_6l_tak2')

#list for accessing the gna data
gna2_lst = ['../modfiles/base_0_gna_6l_tak3.npy']
for i in range(1,10):
    gna2_lst.append(f'../modfiles/base_0{i}_gna_6l_tak2.npy')
gna2_lst.append('../modfiles/t_1_gna_6l_tak2.npy')

#list for collecting rin
rin_lst = ['base_0_rin_6l_tak3']
for i in range(1,10):
    rin_lst.append(f'base_0{i}_rin_6l_tak3')
rin_lst.append('base_1_rin_6l_tak3')

#list for accessing the rin data
rin2_lst = ['../modfiles/base_0_rin_6l_tak3.npy']
for i in range(1,10):
    rin2_lst.append(f'../modfiles/base_0{i}_rin_6l_tak3.npy')
rin2_lst.append('../modfiles/base_1_rin_6l_tak34.npy')

def main(test):#runs the experiment; the test input indicates which test you want to do
    if test == 'gna':
        gna_run(b, b.side1, b.main_shaft, pos_lst, len_lst, gna_lst)
    elif test == 'rin':
        rin_run(b, b.side1, b.main_shaft, pos_lst, len_lst, rin_lst)
    elif test == 'graph': #the graphing function requires manual modifications reflecting what you want graphed
        graph2(cells, rin2_lst, gna2_lst)
        #if graphing with the legend:
        #graph2(cells, rin2_lst, gna2_lst, lab_lst, 'Base Cables')