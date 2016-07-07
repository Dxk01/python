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
sys.path.append("/home/spark/anqu/python/code/linkWord")
reload(sys)
sys.setdefaultencoding('utf8') 

from mysql_op import mysql_op
from data_deal import data_deal
from linkWord import thinkWord
from clusterByComleteObject import clusterByCompleteObject as cbco
from selectWord import selectWord

def getWord(keyWords):
	words = []
	for word in keyWords:
		words.append(word[0])
	return words



def main():
	#input 
	complete_Ids = ['994120614','1111594089','962734163']
	Cluster_K = 16
	div = 16

	# get keywords
	ClusteBCO = cbco()
	complete_Ids = ClusteBCO.getCompleteProductId(complete_Ids)
	# print complete_Ids
	data = data_deal()
	#real
	# keyWords = data.getDataByID(complete_Ids)
	#for test 
	select = selectWord()
	keyWords = select.readObj('com_keyWords.txt')
	words = getWord(keyWords)
	#get think words
	think = thinkWord()
	#real
	thinkWords = list(set(think.getThinkWordCluster(words)))
	#for test
	select.writeObj(thinkWords,"thinkWords.txt")
	# thinkWords = select.readObj("thinkWords.txt")

	print len(keyWords)
	#获取联想词的信息
	thinkWordNews = data.getThinkWordPriorityAndSearchC(thinkWords)
	# print thinkWordNews[0]
	all_Words = keyWords + thinkWords
	print len(all_Words)

	# #get think words' priority searchCount and genre
	# thinkWordNews = data.getThinkWordPriorityAndSearchC(thinkWords)



	#read data

if __name__ == '__main__':
	main()
