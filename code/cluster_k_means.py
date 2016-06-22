#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-15

import sys
sys.path.append("/home/spark1/python/")
sys.path.append("/home/spark/anqu/code")
reload(sys)
sys.setdefaultencoding('utf8') 
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import data_deal
import time 
import mysql_op
import myself_cluster

class Cluster_K_Means():
	def __init__(self):
		pass

	def  getData(self):
		data_a = data_deal.data_deal()
		mat,wdic = data_a.getMatrix()
		# print len(mat)
		Iddic = data_a.getIddic(wdic)
		return mat,Iddic

	def cluster_k_means(self,mat):
		# print mat[0]
		resualt = KMeans(n_clusters=2000,random_state=200).fit_predict(mat)
		# for re in resualt:
		# 	print re
		return resualt

	def cluster_mini_k_means(self,mat):
		return MiniBatchKMeans(n_clusters=2000,random_state=4000).fit_predict(mat)

	def classifaction(self,word_cluster_resault,Iddic,Id):
		pass

	def mapResault(self,resualt,Iddic):
		word_cluster_resault = {}
		length = len(resualt)
		for num in xrange(length):
			if word_cluster_resault.has_key(resualt[num]):
				word_cluster_resault.get(resualt[num]).append(Iddic.get(num))
			else:
				word_list = []
				word_list.append(Iddic.get(num))
				word_cluster_resault.setdefault(resualt[num],word_list)
		return word_cluster_resault

	def print_Resault(self,word_cluster_resault):
		for line  in word_cluster_resault.keys():
			print "class "+ str(line) + "  contain words : " 
			word_list = word_cluster_resault.get(line)
			count = 0
			for word in word_list:
				print word,"  : ",
				count += 1
				if count % 5 == 0:
					print ''
			print "\n\n\n"

	def writer_to_LocalFile(self,word_cluster_resault,type=2):
		filepath = "/home/spark/anqu/analysisResault/"
		ISOTIMEFORMAT='%Y-%m-%d %X'
		dateTime =  time.strftime( ISOTIMEFORMAT, time.localtime())
		filename = "clusterResault"+dateTime+".txt"
		fp = open(filepath+filename,"a")
		if type == 1:
			fp.write('''//--------------------------------------------------------------------------------------------------------//
				    ----------------------------------------using k-means method-------------------------------------\
				   //---------------------------------------------------------------------------------------------------------//''')
		else:
			fp.write('''//--------------------------------------------------------------------------------------------------------//
				    -----------------------------------using mini-k-means method----------------------------------\
				   //---------------------------------------------------------------------------------------------------------//''')
		for line in word_cluster_resault.keys():
			fp.write("class   "+ str(line) + "  contain words :   \n")
			word_list = word_cluster_resault.get(line)
			count = 0
			for word in word_list:
				fp.write(word+"   ")
				count += 1
				if count % 5 == 0:
					fp.write("\n")
			fp.write("\n\n\n\n")#k-means : 1 ;mini-k-means : 2

	def write_to_sql(self,word_cluster_resault):
		print 'start.......'
		mysql = mysql_op.mysql_op("127.0.0.1","root","root","mysql")
		mysql.excute("create table if not exists cluster_resault (class_num int,words text)")
		mysql.excute("delete from cluster_resault")
		for line in word_cluster_resault.keys():
			data = ""
			word_list = word_cluster_resault.get(line)
			for word in word_list:
				data += word+" , "
			sql = "insert into cluster_resault values(%d,%s)"%(line,data)
			print sql
			mysql.excute(sql)

def main():
	clusterk_means = Cluster_K_Means()
	Matrix,Iddic = clusterk_means.getData()
	

	# k-means method
	resualt = clusterk_means.cluster_k_means(Matrix)
	word_cluster_resault = clusterk_means.mapResault(resualt,Iddic)
	clusterk_means.writer_to_LocalFile(word_cluster_resault,1)
	# # mini k-means method
	# secResault = clusterk_means.cluster_mini_k_means(Matrix)
	# word_cluster_resault = clusterk_means.mapResault(secResault,Iddic)
	# clusterk_means.writer_to_LocalFile(word_cluster_resault)
	# # fuzzy self-organizing map Neural Network method
	# cla_num,resualt = myself_cluster.m_cluster_Som().cluster(Matrix)
	# word_cluster_resault = clusterk_means.mapResault(resualt,Iddic)
	# clusterk_means.writer_to_LocalFile(word_cluster_resault)
	# print "get classfacation : ",cla_num




if __name__ == '__main__':
	main()