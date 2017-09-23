# -*- coding: utf-8 -*-

# Write : lgy
# Data : 2017-09-22
# function: Algorithm linearUnit

from MyCode.Algorithm.Perceptron.Perceptron import Perceptron

class LinearUnit(Perceptron):
	"""
	线性单元
	"""
	def __init__(self, input_num, activator):
		"""
		 init class LinearUnit
		:param input_num:
		:param activator:
		"""
		Perceptron.__init__(self,input_num,activator)
