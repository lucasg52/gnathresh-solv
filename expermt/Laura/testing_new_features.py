from Rin_cells2 import Rin_cell_1, Rin_cell_1y, AdjSearch
from neuron import h
from cells.adoptedeq import elength
import time
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import cm as cmap

m = Rin_cell_1(0)
m.side1.L = 0.2*elength(m.side1)
m._normalize()
m.side1.disconnect()
n=Rin_cell_1y(1)
n.side1.disconnect()

def adjust_factor(len,dl):
	n.side1.L = (len/dl)*elength(n.side1)
	n.dau1.L = (len/dl)*elength(n.dau1)
	n.dau2.L = (len/dl)*elength(n.dau2)
	n.side1.connect(n.main_shaft(0.6))
	n._normalize()
	n.side1.disconnect()

# def adjust_addent(len,dl):
# 	n.side1.L = (len-dl)*elength(n.side1)
# 	n.dau1.L = (len-dl)*elength(n.dau1)
# 	n.dau2.L = (len-dl)*elength(n.dau2)
# 	n.side1.connect(n.main_shaft(0.6))
# 	n._normalize()
# 	n.side1.disconnect()

def adjust(len):
	n.side1.L = (0.0285736*len)*elength(n.side1)
	n.dau1.L = (0.0285736*len)*elength(n.dau1)
	n.dau2.L = (0.0285736*len)*elength(n.dau2)
	n.side1.connect(n.main_shaft(0.6))
	n._normalize()
	n.side1.disconnect()
	print(n.side1.L/118.84, n.dau1.L/118.84, n.dau2.L/118.84)

def m_adjust(len):
	m.side1.L = len*elength(m.side1)
	m.side1.connect(m.main_shaft(0.6))
	m._normalize()
	m.side1.disconnect()

def test():
	adj_lst = [j/1000 for j in range(800, 35000, 1)]
	adj_lst2 = []
	diff_lst = []
	lengths = [g/100 for g in range(5,205,5)]
	len_lst=[]
	fin_results = []
	min_diff = []
	act_len = []
	for k in lengths:
		print(f"for length {k}")
		m_adjust(k)
		# adjust(k)
		# M = m.Rin(m.side1(0))
		# N = n.Rin(n.side1(0))
		# adj_lst2.append(0.0285736*k)
		# diff_lst.append(M-N)
		# fin_results.append(k)

		# if k < 0.5:

		for i in adj_lst:
			adjust_factor(k, i)
			M = m.Rin(m.side1(0))
			N = n.Rin(n.side1(0))
			min_diff.append(abs(M-N))
			len_lst.append(n.side1.L / 118.84)
		print(f"{adj_lst[min_diff.index(min(min_diff))]} with a diff of {min(min_diff)} and the lengths are {n.side1.L/118.84, n.dau1.L/118.84, n.dau2.L/118.84, m.side1.L/118.84}")
		adj_lst2.append(adj_lst[min_diff.index(min(min_diff))])
		act_len.append(len_lst[min_diff.index(min(min_diff))])
		diff_lst.append(min(min_diff))
		fin_results.append(k)
		min_diff=[]
		len_lst = []

		# else:
		# 	for l in range(0,int(k*100), 1):
		# 		# print(k-(l/100))
		# 		adjust_addent(k,l/100)
		# 		M = m.Rin(m.side1(0))
		# 		N = n.Rin(n.side1(0))
		# 		#diff_lst.append(M-N)
		# 		if abs(M-N)>=0 and abs(M-N)<500:
		# 			print(f"dl is {l/100} and the diff is {M-N}")
		# 			adj_lst2.append(l/100)
		# 			diff_lst.append(M-N)
		# 			fin_results.append(k)
	return adj_lst2, diff_lst, fin_results, act_len

def plot():
	fig, ax = plt.subplots(nrows=2,ncols=1,figsize=(8,4))
	# ax = fig.add_subplot(projection='3d')
	# x0 = fin_results
	# y0 = adj_lst2
	# X0,Y0 = np.meshgrid(x0,y0)
	# z1 = adj_lst2
	# z0 = diff_lst
	# Z0,y1 = np.meshgrid(z0,z1)
	# ax.plot_surface(X0, Y0, Z0,alpha=0.5, cmap = cmap.viridis)
	# ax.set_xlabel('length in lambda')#'length of side branches in lambda'
	# ax.set_ylabel('adjust element')#'node along main shaft')
	# ax.set_zlabel('difference')#'input resistance')
	# ax.set_title('creating equal input resistances')
	# plt.show()
	ax[0].plot(len_lst, diff_lst, label="length")
	ax[1].plot(fin_results, adj_lst2, label="factor")
	ax[0].grid()
	ax[1].grid()
	plt.show()

	# return fin_results
	# plt.plot(adj_lst, diff_lst)
	# plt.grid()
	# plt.show()
# ex_adj_lst = [234,3,34,562,4,35,6,452]
# ex_lengths = [345,34254,64,687,243,45,544]
# print(ex_lengths[ex_adj_lst.index(min(ex_adj_lst))], ex_adj_lst[ex_lengths.index(min(ex_lengths))])
# def fullsearch(nsteps=30):
# 	search = AdjSearch(0,4,test)
# 	for i in range(nsteps):
# 		search.searchstep()
# 		# print(search.a)
# 	return search.a