# -*- coding: utf-8 -*-

# Write : lgy
# Data : 2017-09-24
# function: Algorithm class Layer for bp network

from Node import Node
from ConstNode import ConstNode

class Layer(object):
	def __init__(self, layer_index, node_count):
		"""
		初始化一层
		:param layer_index: 层编号
		:param node_count: 层包含的节点数
		"""
		self.layer_index = layer_index
		self.nodes = []
		for i in range(node_count):
			self.nodes.append(Node(layer_index,i))
		self.nodes.append(ConstNode(layer_index,node_count))

	def set_output(self, data):
		"""
		设置层的输出，当层是输入层时会用到
		:param data:
		:return:
		"""
		for i in xrange(len(data)):
			self.nodes[i].set_output(data[i])

	def calc_output(self):
		"""
		计算层的输出向量
		:return:
		"""
		for node in self.nodes[:-1]:
			node.calc_output()

	def dump(self):
		"""
		打印层的信息
		:return:
		"""
		for node in self.nodes:
			print node

