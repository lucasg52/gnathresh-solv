from gnatsolv.cells import base
from neuron import h
from matplotlib import pyplot as plt


class resist_cell(BaseExpCell(0.2,3)):
	def collat():
		self.parent = h.Section()