import numpy as np
from gnatsolv.cells.dcell import DCell
from gnatsolv.tools.environment import DeathEnviro
from gnatsolv.tools.apdeath import DeathRec
from neuron import h
h.load_file("stdrun.hoc")


def collect_gna(e, est, err):
    cell = e.m
    mtx = []
    for x in cell.iter_length(1):
        gna_lst = []
        # print(f"NEW SPOT: b1 seg = {x}")
        for y in cell.iter_length(2):
            # h.topology()
            # print(f"NEW SPOT: seg = {y}")
            gna = e.fullsolve(est, err, 1e-9)
            gna_lst.append(gna)

            # guess subsequent error based on previous error
            err = (abs(est - gna) + err) / 2
            # update the estimate to ensure faster convergence of subsequent binary search
            est = gna

        # print(f"gna for seg {x} = {gna}")
        mtx.append(gna_lst)
    # len_mtx = np.linspace(
    #             0, cell.lmax[1],
    #             int((cell.lmax[1]-0)/(1*cell.dx))
    #             )

    return mtx

def main():

    cell = DCell()  # set up cell
    cell.l[3] = 0  # sets lengths of unneeded branches to 0
    cell.l[1] = cell.l[2] =4.0
    cell.update_geom(lengths=[1,2,3])  # removes the side branches we don't want
    cell.side[1].connect(cell.main_shaft(0.2)) #
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
    initial_error = 0.05

    data = collect_gna(
        e,
        initial_estimate, initial_error
    )
    np.save('2_side_branches_lengths_gna_matrix1', data)
    # np.save('2_side_branches_lengths_side_len_matrix1', len_data)

    # print(f"gna data for 2 branch lengths in 2_side_branches_lengths_gna_matrix1.npy")
    # print(f"len data for 2 branch lengths in 2_side_branches_lengths_side_len_matrix1.npy")

if __name__ == '__main__':
    main()

