#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-07

import sys
sys.path.append("/home/spark1/python/")
sys.path.append("/home/spark/anqu/python/code")
sys.path.append("/home/spark/anqu/python/code/Tools")
sys.path.append("/home/spark/anqu/python/code/data_deal")
sys.path.append("/home/spark/anqu/python/code/Cluster")
sys.path.append("/home/spark/anqu/python/code/Word")
reload(sys)
sys.setdefaultencoding('utf8') 

from mysql_op import mysql_op
from data_deal import data_deal
from thinkWord import thinkWord
from clusterByComleteObject import clusterByCompleteObject as cbco
from selectWord import selectWord
from cluster_k_means import Cluster_K_Means as CKM
from calculSimilarity import similarity
import numpy as np

def getWord(keyWords):
	words = []
	for word in keyWords:
		words.append(word[0])
	return words



def main():
	
	#input 
	complete_Ids = ['994120614','1111594089','962734163']
	Cluster_K = 8
	div = 8
	# get keywords
	ClusteBCO = cbco()
	complete_Ids = ClusteBCO.getCompleteProductId(complete_Ids)
	# print complete_Ids
	data = data_deal()
	#real
	# keyWords = data.getDataByID(complete_Ids)
	# for word in keyWords:
	# 	print word[0]
	#for test 
	select = selectWord()
	# select.writeObj(keyWords,"com_keyWords.txt")

	keyWords = select.readObj('com_keyWords.txt')
	# # keyWords = data.delRepeatWord(keyWords)
	words = getWord(keyWords)
	# #get think words
	think = thinkWord()
	# #real
	thinkWords = think.getThinkWordCluster(words)
	select.writeObj(thinkWords,"thinkWords.txt")
	# #for test
	# thinkWords = select.readObj("thinkWords.txt")
	# # print len(keyWords)
	# #获取联想词的信息
	thinkWordNews = data.getThinkWordPriorityAndSearchC(thinkWords)
	all_Words = keyWords + thinkWordNews
	all_Words = data.delRepeatWord(all_Words)
	# # #get think words' priority searchCount and genre
	# #cluster word 
	# # build matrix 
	Matrix = data.calMatrixByWordNews(all_Words)
	# # cluster
	ckm = CKM()
	resualt = ckm.cluster_k_means(Matrix,Cluster_K)

	# 写入到数据库
	sim = np.zeros(len(resualt))
	select.insert_data(all_Words,sim,resualt)

	#提取分析结果
	select = selectWord()
	select.getTopKKeyWord(20,Cluster_K)
	select.getTopKClassWord(20,Cluster_K)

if __name__ == '__main__':
	main()
