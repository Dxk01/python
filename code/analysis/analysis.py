#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-07

import sys
sys.path.append("/home/spark/anqu/python/code")
sys.path.append("/home/spark/anqu/python/code/Tools")
reload(sys)
import config
sys.setdefaultencoding('utf8') 

from mysql_op import mysql_op
from data_deal import data_deal
from thinkWord import thinkWord
from clusterByComleteObject import clusterByCompleteObject as cbco
from selectWord import selectWord
from cluster_k_means import Cluster_K_Means as CKM
from calculSimilarity import similarity
import numpy as np
from ClassWordExtend import ClassWordExtend as CWD
from SomNeuralNetwoke import SomNeuralNetwork as SNN

def getWord(keyWords):
	words = []
	for word in keyWords:
		words.append(word[0])
	return words

def main():
	
	#input  parameters
	# Input_Ids = [994120614,1111594089,962734163]
	# Input_Ids = ['994120614','1111594089','962734163']
	# Input_Ids = ['284087761','284124560','284146702']
	Input_Ids = ['998466140','639486670']
	Cluster_K = 20
	div = 20
	TopKDiv = 50

	# Declare Variable
	# get keywords
	ClusteBCO = cbco()
	cwd = CWD()
	data = data_deal()
	select  = selectWord()
	think = thinkWord()
	ckm = CKM()
	snn = SNN()

	# print Input_Ids
	# complete_Ids = ClusteBCO.getCompleteProductId(Input_Ids)
	# print complete_Ids
	#real
	# keyWords = data.getDataByID(complete_Ids)
	# keyWords = data.delRepeatWord(keyWords)
	# select.writeObj(keyWords,"com_keyWords.txt")

	#for test 
	# keyWords = select.readObj("com_keyWords.txt")
	# # #get think words  获取联想词
	# # #real
	# thinkWords = think.getThinkWordCluster(keyWords)
	# select.writeObj(thinkWords,"thinkWords.txt")

	# thinkWords = select.readObj("thinkWords.txt")

	# #获取App 的类别下的关联词
	# genreIDs = cwd.getGenreIDByAppId(Input_Ids)
	# genreIDs = ['136425','7008','7009']
	# cwd_Words = cwd.getKeyWordofClassWord(genreIDs)
	# select.writeObj(cwd_Words,"cwd_Words.txt")

	# all_Words = data.delRepeatWord(keyWords+thinkWords+cwd_Words)
	# all_Words = data.delRepeatWord(all_Words)
	# select.writeObj(all_Words,"all_Words.txt")
	# all_Words = select.readObj("all_Words.txt")
	# print len(all_Words)
	# for word in all_Words:
		# print word

	# # #for test
	# # #获取词的信息(词，词热，searchCount,genre)
	# WordNews = data.getThinkWordPriorityAndSearchC(all_Words)
	# WordNews = list(set(WordNews))
	# select.writeObj(WordNews,"WordNews.txt")
	# WordNews  = select.readObj("WordNews.txt")
	# print len(WordNews)

	# for word in WordNews:
		# print word[0],word[1],word[2],word[3]
	# # #cluster word 
	# # # build matrix 
	# Matrix = data.calMatrixByWordNews(WordNews)
	# # # cluster
	# resualt = ckm.cluster_k_means(Matrix,Cluster_K)
	# resualt = snn.cluster(Matrix)
	# resualt = snn.unLearncluster(Matrix)

	# print len(Matrix),len(list(set(resualt)))
	# # 写入到数据库
	# sim = np.zeros(len(resualt))	# all_Words = data.delRepeatWord(all_Words)
	# select.insert_data(WordNews,sim,resualt)

	# #提取分析结果
	select.getTopKKeyWord(TopKDiv,Cluster_K)
	# select.getTopKClassWord(TopKDiv,Cluster_K)

if __name__ == '__main__':
	main()
