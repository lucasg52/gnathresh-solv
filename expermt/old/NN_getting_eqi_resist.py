from Rin_cells2 import Rin_cell_1, Rin_cell_1y, AdjSearch
from neuron import h
from cells.adoptedeq import elength
import time
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import cm as cmap

m = Rin_cell_1(0)
m._normalize()
m.dx = 0.025/10
m.side1.disconnect()
n=Rin_cell_1y(1)
n.dau1.diam = n.dau2.diam = 0.125992105
n.side1.disconnect()
n.dx = 0.025/10

def adjust_factor(len,dl):
	n.side1.L = (len/dl)*elength(n.side1)
	n.dau1.L = (len/dl)*elength(n.dau1)
	n.dau2.L = (len/dl)*elength(n.dau2)
	n.side1.connect(n.main_shaft(0.6))
	n._normalize()
	n.side1.disconnect()

def adjust(len):
	n.side1.L = (0.5*len)*elength(n.side1)
	n.dau1.L = (0.5*len)*elength(n.dau1)
	n.dau2.L = (0.5*len)*elength(n.dau2)
	n.side1.connect(n.main_shaft(0.6))
	n._normalize()
	n.side1.disconnect()
	print(n.side1.L/118.84, n.dau1.L/118.84)

def m_adjust(len):
	m.side1.L = len*elength(m.side1)
	m.side1.connect(m.main_shaft(0.6))
	m._normalize()
	m.side1.disconnect()

def test():
	adj_lst = [j/1000 for j in range(100, 35000, 1)]
	adj_lst2 = []
	diff_lst = []
	lengths = [g/100 for g in range(5,205,5)]
	len_lst=[]
	fin_results = []
	min_diff = []
	act_len = []
	# rin_base = []
	# eqi_base = []
	# e_rin=[]
	# b_rin=[]
	for k in lengths:
		print(f"for length {k}")
		m_adjust(k)
		# adjust(k)
		# M = m.Rin(m.side1(0))
		# N = n.Rin(n.side1(0))
		# adj_lst2.append(0.0285736*k)
		# diff_lst.append(M-N)
		# fin_results.append(k)

	# if k < 3:
		for i in adj_lst:
			adjust_factor(k, i)
			M = m.Rin(m.side1(0))
			#b_rin.append(M)
			N = n.Rin(n.side1(0))
			#e_rin.append(N)
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
	fig, ax = plt.subplots(nrows=3,ncols=1,figsize=(8,4))
	ax[0].plot(act_len, diff_lst, label="diff")
	ax[1].plot(fin_results, diff_lst, label="factor")
	ax[2].plot(act_len, fin_results, label='lengths')
	ax[0].grid()
	ax[1].grid()
	ax[2].grid()
	plt.show()