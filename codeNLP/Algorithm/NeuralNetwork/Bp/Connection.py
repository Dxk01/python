# -*- coding: utf-8 -*-
# learn from 零基础入门深度学习
# Write : lgy
# Data : 2017-09-24
# function: Algorithm class Connection for bp network

import random

class Connection(object):
	def __init__(self, upstram_node, downstream_node):
		"""
		初始化连接，权重初始化为是一个很小的随机数
		:param upstram_node: 连接的上游节点
		:param downstream_node: 连接的下游节点
		"""
		self.upstream_node = upstram_node
		self.downstream_node = downstream_node
		self.weight = random.uniform(-0.1,0.1)
		self.gradient = 0.0

	def calc_gradient(self):
		"""
		计算梯度
		:return:
		"""
		self.gradient = self.downstream_node.delta * self.upstream_node.output

	def get_gradient(self):
		"""
		获取当前梯度
		:return: gradient
		"""
		return self.gradient

	def update_weight(self, rate):
		"""
		根据梯度下降算法更新权重
		:param rate:
		:return:
		"""
		self.calc_gradient()
		self.weight += rate * self.gradient

	def __str__(self):
		"""
		打印连接信息
		:return:
		"""
		return '(%u-%u) -> (%u-%u) = %f' % (
			self.upstream_node.layer_index,
			self.upstream_node.node_index,
			self.downstream_node.layer_index,
			self.downstream_node.node_index,
			self.weight)