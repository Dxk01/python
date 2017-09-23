# -*- coding: utf-8 -*-

# Write : lgy
# Data : 2017-09-22
# function: Algorithm activator function sets

import math

class Activator(object):
	"""
		神经网络算法的各种激活函数 集合
	"""
	def __init__(self):
		pass

	def AndFunction(self, X):
		return 1 if X > 0 else 0

	def Sigmoid(self, X):
		# val = reduce(lambda a,b: a+b, X)
		return 1.0 / (1.0 + math.e ** X)

	def tanH(self, X):
		return math.tanh(X)
