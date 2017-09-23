# -*- coding: utf-8 -*-

# Write : lgy
# Data : 2017-09-22
# function: Algorithm
# import numpy as np


class Perceptron(object):
	""" class Perceptron define Algorithm """

	def __init__(self,input_num,activator):
		""" init function
			:param input_num  ==: data feature number
			:param activator ==: activator val
		"""
		self.w_ = [0.0 for i in xrange(input_num)]
		self.activator = activator
		self.bias = 0.0

	def __str__(self):
		""" print learned weigths """
		return "weigths \t:{0}\nbias\t:{1}\n".format(self.w_,self.bias)

	def predict(self,input_vec):
		"""
			input vector output perceptron predict result
		"""
		# 把input_vec[x1,x2,...,xn] 和 weights 打包在一起
		# 变成（x1,w1）...
		# 利用map计算 xi*wi
		# 利用reduce 求和
		return self.activator(reduce(lambda a,b :a+b,
		                             map(lambda (x,w): x*w,zip(input_vec,self.w_)))+self.bias)

	def train(self,input_vecs,labels,iteration,rate):
		"""
		输入训练数据：
		:param input_vecs: 数据向量
		:param labels: 数据分类标签
		:param iteration: 训练轮数
		:param rate: 学习率
		:return:
		"""
		for i in xrange(iteration):
			self._one_iterrtion(input_vecs,labels,rate)

	def _one_iterrtion(self, input_vecs, labels, rate):
		"""
		一次迭代
		:param input_vecs:
		:param labels:
		:param rate:
		:return:
		"""
		samples = zip(input_vecs,labels)
		for (input_vec,label) in samples:
			output = self.predict(input_vec)
			self.update_weights(input_vec,output,label,rate)

	def update_weights(self, input_vec,output,label,rate):
		"""
		按照感知器的规则更新权重
		:param input_vec:
		:param output:
		:param label:
		:param rate:
		:return:
		"""
		delta = label - output
		self.w_ = map(
			lambda (x,w): w + rate * delta*x,zip(input_vec,self.w_)
		)
		# update bias
		self.bias += rate * delta
