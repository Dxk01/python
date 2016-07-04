#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-01

import sys
sys.path.append("/home/spark/anqu/python/code/Cluster")
sys.path.append("/home/spark/anqu/python/code/data_deal")
sys.path.append("/home/spark/anqu/python/code/Tools")
# sys.path.append("/home/spark/anqu/python/code")

reload(sys)
sys.setdefaultencoding('utf-8')

from cluster_k_means import Cluster_K_Means
import selectWord
import time
from data_deal import data_deal
from selectWord import selectWord
from calculSimilarity import similarity
from combine_cluster import combine_cluster
import os 

class clusterByCompleteObject():
	# init 
	def __init__(self,k = 100):
		self.cluster_k = k
		self.data = data_deal()
		self.cluster_Method = Cluster_K_Means()

	#获取基本的数据
	def getData(self,complete_ids):
		Matrix,wddic,word_list = self.data.getKeyWordDataByIds(complete_ids)
		Iddic = self.data.getIddic(wdic)
		return Matrix,Iddic,wdic,word_list

	#获取数据
	def analysis(self,Matrix,Iddic,wdic):
		if len(Matrix) <= self.cluster_k:
			self.cluster_k = len(Matrix) / 2
		resualt = self.cluster_Method.cluster_k_means(Matrix,self.cluster_k)
		cluster_resault = self.cluster_Method.mapResault(resualt,Iddic)
		# SelectWord = selectWord(cluster_resault,wdic)
		sim = similarity()
		similarity_re = sim.calSimilarityN(Matrix,cluster_resault,wdic)
		return resualt,similarity_re 

	#判断竞品关键ID是否相等
	def is_equals(self,com_ids,old_com_ids):
		if len(com_ids) != len(old_com_ids):
			return False
		od_len = len(old_com_ids)
		for c_id in com_ids:
			state = true
			i = 0
			while i < od_len:
				if old_com_ids[i] == c_id:
					break
				i += 1
			if i == od_len:
				return False
		return True


	#测试代码
	def run(self,complete_Ids):
		select = selectWord()
		##提取竞品词从数据库
		# word_list = None
		if os.path.exists('/home/spark/anqu/analysisResault/Object/complete_Ids.txt') == False or self.is_equals(complete_Ids,select.readObj("complete_Ids.txt")) == False:
			word_list = self.data.getDataByID(complete_Ids)
			# select.writeObj(word_list,"word_list.txt")
			#测试使用读取竞品词并将词的各属性列分离
			# word_list = select.readObj('word_list.txt')
			data = self.data.devide_data(word_list)
			words_ps = self.data.delRepeat(word_list)
			#得到分析计算矩阵，以及相关映射集合
			Matrix,wdic = self.data.calMatrix(data)
			Iddic = self.data.getIddic(wdic)
			# #计算聚类相似度
			resualt,similarity_re = self.analysis(Matrix,Iddic,wdic)
			#写入数据库
			if len(resualt) == len(words_ps) and len(resualt):
				print len(resualt)
				select.insert_data(words_ps,similarity_re,resualt)
			else:
				print "Error"
				print len(resualt),len(word_list),len(similarity_re)
			#获取聚类结果
			cluster_resault = self.cluster_Method.mapResault(resualt,Iddic)
			return cluster_resault
		else:
			select.writeObj(complete_Ids,"complete_Ids.txt")
			word_list = select.readObj("cluster_resault.txt")

def main():
	k = 5
	combine_num = 5
	cluster = clusterByCompleteObject(k)
	select = selectWord()
	cluster_resault = select.readObj('cluster_resault.txt')
	key_len = len(cluster_resault.keys())
	# print key_len
	if len(cluster_resault.keys()) != k:	
		cluster_resault = cluster.run(('593499239','399353136','1003165584','737310995','1086911361','1080228178','1067238109','1017226508','909532141','903782554','914791167','952503776658','1070817891','1093026147','1067627594','1069231086'))
		select.writeObj(cluster_resault,'cluster_resault.txt')

	combine = combine_cluster()
	sort_list = combine.sort(cluster_resault)
	com_resault = combine.combine_cluster(sort_list,combine_num)
	select.getBetterPriorityWord(com_resault,20)
	select.getBetterClassWord(com_resault,20)

if __name__ == '__main__':
	main()