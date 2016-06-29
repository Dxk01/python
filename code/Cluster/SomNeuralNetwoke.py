#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-29
# 功能 ：SOM自适应神经网络聚类算法实现

import sys
sys.path.append("/home/spark/anqu/python/code/data_deal")
sys.path.append("/home/spark/anqu/python/code/Tools")
sys.path.append("/home/spark/anqu/python/code/wordAnalysis")
reload(sys)
sys.setdefaultencoding('utf8') 

import time
import mysql_op
import data_deal
import numpy as np
# import pandas as pd
import matplotlib as plot
from sklearn import preprocessing as preP
import math

class SomNeuralNetwork():
	#初始化
	def __init__(self,k_cluster=100, neighbor_radius = 5,learn_deep = 1):
		self.k_cluster = k_cluster
		self.neighbor_radius = neighbor_radius
		self.learn_deep = learn_deep
		self.stop_deep_val = learn_deep / 10
		self.cur_iter_time = 0

	#获取数据
	def getData(self):
		return data_deal.data_deal().getMatrix()

	#向量的归一化
	def NormalSize(self, Marix):
		return preP.normalize(Marix,'l2')

	#单个向量的归一化，
	def NormalSizeOne(self,Matrix,num):
		Matrix[num,:] = preP.normalize([Matrix[num]],'l2')

	#建立模型初始化参数权值向量矩阵
	def initParamater(self,feat_dim = 72):
		self.Weight = preP.normalize(np.random.random((self.k_cluster,feat_dim)))

	#更新邻域半径
	def updateNeighborRadius(self,iter_times):
		self.neighbor_radius = math.pow(math.e, -iter_times)

	#更新学习率
	def updateLearn_deep(self,iter_times):
		self.learn_deep =  self.neighbor_radius / iter_times

	#计算向量内积
	def calculInnerProduct(self,val,weigth):
		return sum(map(lambda x,y:x*y,val,weight))

	#寻找点积最大的权值向量
	def findMaxWeight(self,val):
		Max_j = 0
		Max_innerProduct = self.calculInnerProduct(val,self.Weight[0])
		cur_innerProduct = 0
		for i in xrange(len(self.Weight)):
			cur_innerProduct = self.calculInnerProduct(val,self.Weight[i])
			if cur_innerProduct > Max_innerProduct:
				Max_j = i
		return Max_j

	#更新权值向量
	def updateWeight(self):
		# self.updateNeighborRadius()
		pass
	#训练数据，调整权重向量,自适应聚类
	def cluster(self,Matrix):
		pass

def main():
	Som = SomNeuralNetwork()
	Matrix,wdic = Som.getData()

	unitMat = Som.NormalSize(Matrix)
	weigth = Som.productWeigth()
	print weigth
	# Som.NormalSizeOne(Matrix,0)
	# print unitMat[0]

if __name__ == '__main__':
	main()
		