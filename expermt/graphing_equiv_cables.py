import numpy as np
from matplotlib import pyplot as plt

#the graphing file for all the equivalent cables, T, Wide, and two branches
mat = np.load('../modfiles/base_06_rin_6l_tak3.npy')
mat2 = np.load('../modfiles/base_06_gna_6l_tak2.npy')

file_gna = ['../modfiles/tak1_Y_gna.npy','../modfiles/tak1_trident_gna.npy','../modfiles/tak1_V_gna.npy',
            '../modfiles/tak1_T_gna.npy','../modfiles/tak1_wide_no_len_gna.npy','../modfiles/tak1_twoB_gna.npy']
file_rin = ['../modfiles/tak2_Y_rin.npy','../modfiles/tak1_trident_rin.npy','../modfiles/tak1_V_rin.npy',
            '../modfiles/tak1_T_rin.npy','../modfiles/tak1_wide_no_len_rin.npy','../modfiles/tak1_twoB_rin.npy']
lab_lst = ['Base', 'Y', 'Trident','V','T',"Wide",'2 Branches']
colors = ['black', 'red', 'purple', 'blue', 'cyan', 'green', 'orange', 'pink', 'brown', 'olive', 'grey']



plt.plot(mat[:,1], mat2[:,1], color='black')
for i, file in enumerate(file_rin):
    mtx = np.load(file)
    mtx2 = np.load(file_gna[i])
    mtx[0,1] = mat[0,1]
    mtx2[0,1] = mat2[0,1]
    plt.plot(mtx[:,1], mtx2[:, 1], color=colors[i+1])
# plt.legend(labels=lab_lst, title='Side Branch Geometry', loc="lower left", ncols=2)
        # plt.title(r"$\text{R}_{\text{in}}$ (M$\Omega$) Base on Length [T Cells]")
# plt.xlabel("log$_{10}$(side branch length in $\\lambda$)")
# plt.ylabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
plt.grid()
# plt.title(r"$\text{g}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$ Based on Length [Base Cables]")
plt.ylabel(r"$\text{g}_{\text{Na}} (\frac{\text{mho}}{\text{cm}^2})$")
# plt.title(r"$\text{R}_{\text{in}}$ vs $\text{g}_{\text{Na}}$ [Base Cells]")
plt.xlabel(r"$\text{R}_{\text{in}}$ (M$\Omega$)")
plt.show()