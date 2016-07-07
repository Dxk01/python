#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-06
# 关键词的联想词的分析获取

import sys
sys.path.append("/home/spark/anqu/python/code/Tools")
sys.path.append("/home/spark/anqu/python/code/data_deal")
reload(sys)
sys.setdefaultencoding('utf-8')

from mysql_op import mysql_op
from particeple import participle
from data_deal import data_deal
from chinese import chinese

class thinkWord():
	def __init__(self):
		self.data = data_deal()
		self.mysql = mysql_op()

	#获取当前词的联想词集合
	def getThinkWord(self,word):
		mysql = mysql_op()
		chi = chinese()
		if chi.is_contains(word):
			sql = 'select * from hintWord where hintword=\"%s\"'%word
		else:
			sql = 'select * from hintWord where hintword=\'%s\''%word
		resault = mysql.select(sql)
		return list(set(resault))

	#当前聚类下的联想词的获得
	def getThinkWordCluster(self,cluster_Words):
		thinkWords = []
		for word in cluster_Words:
			thinkWords += self.getThinkWord(word)
			# print 1
		#去除联想词中的非中文词
		chi = chinese()
		for word in thinkWords:
			if chi.is_chinese(word) == False:
				thinkWords.remove(word)
				continue
			if word in cluster_Words:
				thinkWords.remove(word)
		return list(set(thinkWords))

	#获取联想词的词热等信息数据
	

	#处理聚类后品类词记录
	def getParticepleWord(self,Datas):
		clusterS = []
		for data in Datas:
			cluster_Words = []
			for word in data:
				cluster_Words.append(word[0])
			clusterS.append(cluster_Words)
		return clusterS
def main():
	tWord = thinkWord()
	tWord.getThinkWord('微信')

if __name__ == '__main__':
	main()