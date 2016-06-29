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

class SomNeuralNetwork():
	#初始化
	def __init__(self):
		pass

	#获取数据
	def getData(self):
		data = data_deal.data_deal().getMatrix()
		return data

	#样本集的归一化
	def NormalSize(self, Marix):
		NormalMat = preP.normalize(Marix,'l2')
		return NormalMat

	#样本的归一化
	def NormalSizeOne(self,Matrix,num):
		Matrix[num,:] = preP.normalize([Matrix[num]],'l2')
		



def main():
	Som = SomNeuralNetwork()
	Matrix,wdic = Som.getData()
	# unitMat = Som.NormalSizeOne(Matrix,0)
	print Matrix[0]
	Som.NormalSizeOne(Matrix,0)
	print Matrix[0]


if __name__ == '__main__':
	main()
		