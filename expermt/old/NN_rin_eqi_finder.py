from expermt.Laura.Rin_cells2 import Rin_cell_1, Rin_cell_v
from neuron import h
from cells.adoptedeq import elength
import time
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import cm as cmap

m = Rin_cell_1(0)
m.side1.disconnect()
l=Rin_cell_v(1)
l.side1.disconnect()
l.dau1.disconnect()
l.side1.diam = l.dau1.diam = 0.075

def adjust_factor(len,dl):
	l.side1.L = (len/dl)*elength(l.side1)
	l.dau1.L = (len/dl)*elength(l.dau1)
	l.side1.connect(l.main_shaft(0.6))
	l.dau1.connect(l.main_shaft(0.6))
	l._normalize()
	l.side1.disconnect()
	l.dau1.disconnect()

# def adjust(len):
# 	n.side1.L = (0.0285736*len)*elength(n.side1)
# 	n.dau1.L = (0.0285736*len)*elength(n.dau1)
# 	n.dau2.L = (0.0285736*len)*elength(n.dau2)
# 	n.side1.connect(n.main_shaft(0.6))
# 	n._normalize()
# 	n.side1.disconnect()
# 	print(n.side1.L/118.84, n.dau1.L/118.84, n.dau2.L/118.84)

def m_adjust(len):
	m.side1.L = len*elength(m.side1)
	m.side1.connect(m.main_shaft(0.6))
	m._normalize()
	m.side1.disconnect()

def test():
	adj_lst = [j/1000 for j in range(100, 5001, 1)]
	adj_lst2 = []
	diff_lst = []
	lengths = [g/100 for g in range(5,305,5)]
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
			M = m.Rin(m.side1(0))/2
			N = l.Rin(l.side1(0))
			min_diff.append(abs(M-N))
			len_lst.append(l.side1.L / 118.84)
		print(f"{adj_lst[min_diff.index(min(min_diff))]} with a diff of {min(min_diff)} and the lengths are {l.side1.L/118.84}")
		adj_lst2.append(adj_lst[min_diff.index(min(min_diff))])
		act_len.append(len_lst[min_diff.index(min(min_diff))])
		diff_lst.append(min(min_diff))
		fin_results.append(k)
		min_diff=[]
		len_lst = []
	return adj_lst2, diff_lst, fin_results, act_len

def plot():
	fig, ax = plt.subplots(nrows=3,ncols=1,figsize=(8,4))
	ax[0].plot(act_len, diff_lst, label="length")
	ax[1].plot(fin_results, adj_lst2, label="factor")
	ax[2].plot(fin_results, act_len)
	ax[0].grid()
	ax[1].grid()
	ax[2].grid()
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