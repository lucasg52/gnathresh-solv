import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
h.load_file("stdrun.hoc")


def collect_gna(e, est, rad, end, start=0):
    cell = e.cell
    mtx_len = np.linspace(start, end,int((end-start)/(1*cell.dx)))
    mtx_diam = mtx_len.size
    gna_mtx = np.zeros((mtx_diam, mtx_diam))
    for m,len1 in enumerate(mtx_len):
        cell.update_length(1,len1)

        for n,len2 in enumerate(mtx_len):
            cell.update_length(2, len2)
        #     # h.topology()
            gna = e.fullsolve(est, rad, 1e-9)
            gna_mtx[m, n] = gna

            # guess subsequent radius based on previous radius
            rad = (abs(est - gna) + rad) / 2
            # update the estimate to ensure faster convergence of subsequent binary search
            est = gna
    return gna_mtx

def main():

    cell = DCell()  # set up cell
    cell.l[3] = 0  # sets lengths of unneeded branches to 0
    cell.l[1], cell.l[2] = 4.0, 4.0
    cell.update_geom(lengths=[1,2,3])  # removes the side branches we don't want
    cell.side[1].disconnect()
    cell.side[2].disconnect()
    cell.side[1].connect(cell.main_shaft(0.2))
    cell.side[2].connect(cell.main_shaft(0.2))

    # h.topology() #checks the topology of the cell

    stim = h.IClamp(cell.parent(0.5)) #setups the stimulator
    stim.amp = 0.2 #gives it an amp in mV
    stim.delay = 0 #delay of Clamp from start in ms
    stim.dur = 5 / 16 #duration of clamp in ms

    # set up death recorder and gna solver

    deathrec = DeathRec(cell.main_shaft, cell.main_shaft, 1)
    e = DeathEnviro(cell, deathrec, stim)
    e.PRINTTIME = True  # enable solver to print runtime of each individual solve

    initial_estimate = 0.15
    initial_radius = 0.05

    print(cell.dx)
    # data = collect_gna(
    #     e,
    #     initial_estimate, initial_radius,
    #     end=6
    # )
    # print(data)
    # np.save('2_side_branches_lengths_gna_matrix1', data)
    # # np.save('2_side_branches_lengths_side_len_matrix1', len_data)
    #
    # print(f"gna data for 2 branch lengths in 2_side_branches_lengths_gna_matrix1.npy")
    # print(f"len data for 2 branch lengths in 2_side_branches_lengths_side_len_matrix1.npy")

if __name__ == '__main__':
    main()

