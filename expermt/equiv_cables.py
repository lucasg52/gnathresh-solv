#import necessary libraries, cells, and functions
from cells.rincell import RinCell, Rin_Ycell, Rin_Trident, Rin_Vcell, Rin_Tcell, Rin_2bbcell
from cells.adoptedeq import elength
from cells.expermt.graphing_equiv_cables import grapher
from neuron import h
import time
import numpy as np
h.load_file("stdrun.hoc")

# file for the Equivalent Cables Experiment
h.dt = pow(2,-6)

#creating Lists for length and files
len_lst = [j / 100 for j in range(0, 610, 10)]
file_lst = ['base_both.out', 'Y_both.out', 'Tri_both.out', 'V_both.out','T_both.out','Phat_both.out','2branch_both.out']

#creating cells
m = RinCell(0)
n = Rin_Ycell(1)
w = Rin_Trident(2)
v = Rin_Vcell(3)
t = Rin_Tcell(4)
m2 = RinCell(5)
m2.side1.diam = 0.4
b2 = Rin_2bbcell(6)
b2.csite = 0.7
gcells = [m,n,w,v,t, m2, b2]
for cell in gcells:
    cell.setup_stim()
    cell.set_matx(len(len_lst))

#function for changing the lengths of each cell
def setting_length(dau_len):
    if dau_len == 0:
        m.side1.disconnect()
        n.side1.disconnect()
        w.side1.disconnect()
        v.side1.disconnect()
        v.dau1.disconnect()
        t.side1.disconnect()
        m2.side1.disconnect()
        b2.side1.disconnect()
        b2.side2.disconnect()
        b2.csite(0.6)
        for cell in gcells:
            cell._normalize()

    else: #all modications to length were made to have the cables be of the same input resistance
        m.side1.L = dau_len*elength(m.side1)
        n.side1.L = (dau_len/2)*elength(n.side1)
        n.dau1.L = (dau_len / 2) * elength(n.dau1)
        n.dau2.L = (dau_len / 2) * elength(n.dau2)
        w.side1.L = (dau_len / 2) * elength(w.side1)
        w.dau1.L = (dau_len / 2) * elength(w.dau1)
        w.dau2.L = (dau_len / 2) * elength(w.dau2)
        w.dau3.L = (dau_len/2)*elength(w.dau3)
        v.side1.L = (dau_len) * elength(v.side1)
        v.dau1.L = (dau_len) * elength(v.dau1)
        t.side1.L = (dau_len) * elength(t.side1)
        t.dau1.L = (dau_len/3) * elength(t.dau1)
        m2.side1.L = (dau_len/2)*elength(m2.side1)
        b2.side1.L = b2.side2.L = (dau_len)*elength(b2.side1)
        b2.csite(0.7)
        for cell in gcells:
            cell._normalize()

def run(solver, file_lst): #function for the entire experiment; it requires knowing ehat test to preform and what file to save it to
    start_all = time.perf_counter()
    for i, cell in enumerate(gcells):
        print(f"{cell.name}:")
        for j, l in enumerate(len_lst):
            setting_length(l)
            print(f"i:{l}")
            if l == 0:
                print("base case")
                if solver == 'gna':
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6) #to use, uncomment the fullsolve function in the RinCell class in the rincell file
                    cell.mtx[j][0]+=l
                    cell.mtx[j][1]+=gna
                elif solver == 'rin':
                    rin = cell.getRin(cell.csite)
                    cell.mtx[j][0] += l
                    cell.mtx[j][2] += rin
                else:
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
                    rin = cell.getRin(cell.csite)
                    cell.mtx[j][0] += l
                    cell.mtx[j][1] += gna
                    cell.mtx[j][2] += rin
                if cell == b2:
                    cell.side1.connect(cell.main_shaft(0.5))
                    cell.side2.connect(cell.main_shaft(0.7))
                elif cell == v:
                    cell.side1.connect(cell.main_shaft(0.6))
                    cell.dau1.connect(cell.main_shaft(0.6))
                else:
                    cell.side1.connect(cell.main_shaft(0.6))
            else:
                if solver == 'gna':
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
                    cell.mtx[j][0]+=l
                    cell.mtx[j][1]+=gna
                elif solver == 'rin':
                    rin = cell.getRin(cell.csite)
                    cell.mtx[j][0] += l
                    cell.mtx[j][2] += rin

                else:
                    gna = cell.fullsolve(cell.est, err=1e-4, acc=1e-6)
                    rin = cell.getRin(cell.csite)
                    cell.mtx[j][0] += l
                    cell.mtx[j][1] += gna
                    cell.mtx[j][2] += rin

        np.save(file_lst[i], cell.mtx)
    end_all = time.perf_counter()
    print(f"total time: {(end_all - start_all) / 60} mins")

def main(test):
    if test == 'rin':
        run('rin', file_lst)
    elif test == 'gna':
        run('gna', file_lst)
    elif test == 'graph':
        grapher()