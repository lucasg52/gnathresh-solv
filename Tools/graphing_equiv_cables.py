import numpy as np
from matplotlib import pyplot as plt

def grapher():
    #the graphing file for all the equivalent cables, T, Wide, and two branches
    mat = np.load('../modfiles/base_06_rin_6l_tak3.npy')
    mat2 = np.load('../modfiles/base_06_gna_6l_tak2.npy')

    file_gna = ['../modfiles/tak1_Y_gna.npy','../modfiles/tak1_trident_gna.npy','../modfiles/tak1_V_gna.npy',
                '../modfiles/tak1_T_gna.npy','../modfiles/tak1_wide_no_len_gna.npy','../modfiles/tak1_twoB_gna.npy']
    file_rin = ['../modfiles/tak2_Y_rin.npy','../modfiles/tak1_trident_rin.npy','../modfiles/tak1_V_rin.npy',
                '../modfiles/tak1_T_rin.npy','../modfiles/tak1_wide_no_len_rin.npy','../modfiles/tak1_twoB_rin.npy']
    labs = ['Base', 'Y', 'Trident','V','T',"Wide",'2 Branches']
    colors = ['black', 'red', 'purple', 'blue', 'cyan', 'green', 'orange', 'pink', 'brown', 'olive', 'grey']


    plt.plot(mat[:,0], mat[:,1], color='black')
    for i, file in enumerate(file_rin):
        mtx = np.load(file)
        mtx2 = np.load(file_gna[i])
        mtx[0,1] = mat[0,1]
        mtx2[0,1] = mat2[0,1]
        plt.plot(mtx[:,0], mtx[:, 1], color=colors[i+1])
    plt.legend(labels=labs, title='Side Branch Geometry',
           bbox_to_anchor=(1.5, 1.05), ncols=2)
    plt.title(r"$\text{R}_{\text{in}}$ Based on Length")
    plt.xlabel("Side Branch Length ($\\lambda$)")
    plt.ylabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
    plt.grid()
    # plt.title(r"$\bar{\text{g}}_{\text{Na}}$ Based on Length")
    # plt.ylabel(r"$\bar{\text{g}}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$")
    # plt.title(r"$\text{R}_{\text{in}}$ vs $\bar{\text{g}}_{\text{Na}}$")
    # plt.xlabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
    plt.show()