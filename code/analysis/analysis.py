#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-07

import sys
sys.path.append("/home/mysql1/anqu/python/code")
# sys.path.append("/home/mysql1/anqu/python/code/Tools")
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

# run analysis chinese 
def runAnalysis_ch(Input_Ids,genreIDs,Cluster_K = 20,div = 20,TopKDiv = 50):
	ClusteBCO = cbco()
	cwd = CWD()
	data = data_deal()
	select  = selectWord()
	think = thinkWord()
	ckm = CKM()
	snn = SNN()

	complete_Ids = ClusteBCO.getCompleteProductId(Input_Ids)
	# print len(complete_Ids)
	#real
	keyWords = data.getDataByID_ch(complete_Ids)
	keyWords = data.delRepeatWord(keyWords)
	select.writeObj(keyWords,"com_keyWords.txt")

	#for test 
	# keyWords = select.readObj("com_keyWords.txt")

	print len(keyWords)
	# # #get think words  获取联想词
	# # #real
	thinkWords = think.getThinkWordCluster_ch(keyWords)
	select.writeObj(thinkWords,"thinkWords.txt")

	# thinkWords = select.readObj("thinkWords.txt")

	print len(list(set(thinkWords)))

	# #获取App 的类别下的关联词
	cwd_Words = cwd.getKeyWordofClassWord_ch(genreIDs)
	select.writeObj(cwd_Words,"cwd_Words.txt")

	# cwd_Words = select.readObj("cwd_Words.txt")

	print len(cwd_Words)

	all_Words = list(set(keyWords+thinkWords+cwd_Words))
	select.writeObj(all_Words,"all_Words.txt")

	# all_Words = select.readObj("all_Words.txt")
	print len(all_Words)

	# # #for test
	# # #获取词的信息(词，词热，searchCount,genre)
	WordNews = data.getThinkWordPriorityAndSearchC(all_Words)
	WordNews = list(set(WordNews))	
	select.writeObj(WordNews,"WordNews.txt")

	# WordNews  = select.readObj("WordNews.txt")
	print len(WordNews)

	# # #cluster word 
	# # # build matrix 
	Matrix = data.calMatrixByWordNews(WordNews)
	# # # cluster
	resualt = ckm.cluster_k_means(Matrix,Cluster_K)
	# resualt = snn.cluster(Matrix)
	# resualt = snn.unLearncluster(Matrix)

	print len(Matrix),len(resualt)
	# # 写入到数据库
	sim = np.zeros(len(resualt))	# all_Words = data.delRepeatWord(all_Words)
	select.insert_data(WordNews,sim,resualt)

	# #提取分析结果
	select.getTopKKeyWord(TopKDiv,Cluster_K)

#run analysis english
def runAnalysis_en(Input_Ids,genreIDs,Cluster_K = 20,div = 20,TopKDiv = 50):
	ClusteBCO = cbco()
	cwd = CWD()
	data = data_deal()
	select  = selectWord()
	think = thinkWord()
	ckm = CKM()
	snn = SNN()

	complete_Ids = ClusteBCO.getCompleteProductId(Input_Ids)
	# print len(complete_Ids)
	#real
	keyWords = data.getDataByID_ch(complete_Ids)
	keyWords = data.delRepeatWord(keyWords)
	select.writeObj(keyWords,"com_keyWords.txt")

	#for test 
	# keyWords = select.readObj("com_keyWords.txt")

	print len(keyWords)
	# # #get think words  获取联想词
	# # #real
	thinkWords = think.getThinkWordCluster_en(keyWords)
	select.writeObj(thinkWords,"thinkWords.txt")

	# thinkWords = select.readObj("thinkWords.txt")

	print len(list(set(thinkWords)))

	# #获取App 的类别下的关联词
	cwd_Words = cwd.getKeyWordofClassWord_en(genreIDs)
	select.writeObj(cwd_Words,"cwd_Words.txt")

	# cwd_Words = select.readObj("cwd_Words.txt")

	print len(cwd_Words)

	all_Words = list(set(keyWords+thinkWords+cwd_Words))
	select.writeObj(all_Words,"all_Words.txt")

	# all_Words = select.readObj("all_Words.txt")
	print len(all_Words)

	# # #for test
	# # #获取词的信息(词，词热，searchCount,genre)
	WordNews = data.getThinkWordPriorityAndSearchC(all_Words)
	WordNews = list(set(WordNews))	
	select.writeObj(WordNews,"WordNews.txt")

	# WordNews  = select.readObj("WordNews.txt")
	print len(WordNews)

	# # #cluster word 
	# # # build matrix 
	Matrix = data.calMatrixByWordNews(WordNews)
	# # # cluster
	resualt = ckm.cluster_k_means(Matrix,Cluster_K)
	# resualt = snn.cluster(Matrix)
	# resualt = snn.unLearncluster(Matrix)

	print len(Matrix),len(resualt)
	# # 写入到数据库
	sim = np.zeros(len(resualt))	# all_Words = data.delRepeatWord(all_Words)
	select.insert_data(WordNews,sim,resualt)

	# #提取分析结果
	select.getTopKKeyWord(TopKDiv,Cluster_K)


def main():
	
	#input  parameters
	# Input_Ids = [994120614,1111594089,962734163]
	# Input_Ids = ['994120614','1111594089','962734163']
	Input_Ids = ['620112416','504634395','526475745']
	genreIDs = ['6014','7014','6016','7008','7015','6024']
	# Input_Ids = ['998466140','639486670']
	Cluster_K = 20
	div = 20
	TopKDiv = 50
	if config.dataBase == config.database_en:
		runAnalysis_en(Input_Ids,genreIDs,Cluster_K,div,TopKDiv)



if __name__ == '__main__':
	main()
