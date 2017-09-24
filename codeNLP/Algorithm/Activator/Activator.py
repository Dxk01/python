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
	@staticmethod
	def AndFunction(X):
		return 1 if X > 0 else 0

	@staticmethod
	def Sigmoid(X):
		# val = reduce(lambda a,b: a+b, X)
		return 1.0 / (1.0 + math.e ** X)

	@staticmethod
	def tanH(X):
		return math.tanh(X)
