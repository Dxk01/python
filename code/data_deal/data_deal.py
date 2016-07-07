#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-15

import sys
sys.path.append("/home/spark1/python/")
sys.path.append("/home/spark/anqu/python/code")
reload(sys)
sys.setdefaultencoding('utf8') 

import mysql_op
import numpy as np
import time
from chinese import chinese
# 数据处理
class data_deal():
	#初始化
	def __init__(self):
		self.mysql = mysql_op.mysql_op("127.0.0.1","root","root","mysql")
	# 获取App store 的类别ID
	def getCategory(self):
		return sorted(list(set(self.mysql.select('select genreID from _category'))))
	#获取searchApp 表的word
	def getsearchword(self,sql="select word from ansearchApp where type=1 and genre like \'%6014%\'"):
		# return list(self.mysql.select("select word, genre from searchApp"))
		 # and genre like \'%6014%\'
		return self.mysql.select(sql)

	#获取词的genre ID
	def getsearchgenre(self,sql="select genre from ansearchApp where type=1  and genre like \'%6014%\'"):
		return self.mysql.select(sql)

	#获取word的词热和searchCount
	def getWordPrioandSearchC(self,sql="select word,priority,searchCount from ansearchApp where type = 1  and genre like \'%6014%\'"):
		data = self.mysql.getWordPriority(sql)
		return self.delRepeat(data)

	#去除重复的热词，合并词热和searchCount
	def delRepeat(self,data):		
		word = {}
		priority_searchCount = []
		count = 0
		for w in data:
			w = list(w)
			if word.has_key(w[0]):
				Id = word[w[0]]
				if priority_searchCount[Id][1] < w[1]:
					priority_searchCount[Id][1] = w[1]
				if priority_searchCount[Id][2] < w[2]:
					priority_searchCount[Id][2] = w[2]
			else:
				re = [w[0],w[1],w[2]]
				priority_searchCount.append(re)
				word.setdefault(w[0],count)
				count += 1
		return priority_searchCount

	#获取app store 的类别Id 列表
	def tranGenretoGenreIDList(self,genrelist):
		genreIDlist = []
		for genre in genrelist :
			# print genre.split(',')
			genreIDlist.append(list(set(genre.split(','))))

	#映射类别ID到相应的整数
	def mapgenreID(self,data):
		count = 0
		ddic = {}
		for d in data:
			if ddic.has_key(d) == False:
				ddic.setdefault(d,count)
				count += 1
		return ddic

	#生成词字典和类别字典
	def  mapwordAgenre(self,word,genre): #needed 
		wdic = {}
		count = 0
		genredic = {}
		length = len(word)
		leng = len(genre)
		# print length,leng
		for i in xrange(length):
			if word[i] in wdic:
				# print 'info'
				Id = wdic.get(word[i])
				data = genredic.get(Id)
				data = data +','+genre[i]  #list(set(data.extend(genre[i])))
				genredic.pop(Id)
				genredic.setdefault(Id,data)
			else :
				wdic.setdefault(word[i],count)
				genredic.setdefault(count,genre[i])
				count += 1
		return wdic,genredic

	#获取联想词的类别标签信息
	def getThinkWordGenre(self,thinkWord):
		data_thinkWord = []
		for word in thinkWord:
			sql = "select genre from ansearchApp where word = \'%s\'"%word
			word_genre = self.mysql.select(sql)
			data_thinkWord.append(word_genre)
		return data_thinkWord

	#获取联想词的词热和searchCount,genre等信息
	def getThinkWordPriorityAndSearchC(self,thinkWord):
		data_thinkWord = []
		chi = chinese()
		for word in thinkWord:
			if chi.is_contains(word):
				sql = "select word,priority,searchCount,genre from ansearchApp where word =\"%s\""%word
			else:
				sql = "select word,priority,searchCount,genre from ansearchApp where word =\'%s\'"%word
			word_prio_search = self.mysql.getWordPriority(sql)
			data_thinkWord.append(word_prio_search)
		return data_thinkWord

	# def mapwordAgenreOnAll(self,word_list):
	# 	wdic = {}
	# 	count = 0
	# 	genredic = {}
	# 	length = len(word)
	# 	# leng = len(genre)
	# 	# print length,leng
	# 	for i in xrange(length):
	# 		if word[i] in wdic:
	# 			# print 'info'
	# 			Id = wdic.get(word[i])
	# 			data = genredic.get(Id)
	# 			data = data +','+genre[i]  #list(set(data.extend(genre[i])))
	# 			genredic.pop(Id)
	# 			genredic.setdefault(Id,data)
	# 		else :
	# 			wdic.setdefault(word[i],count)
	# 			genredic.setdefault(count,genre[i])
	# 			count += 1
	# 	return wdic,genredic

	#获取去重后的GenreID 列表
	def getGenreIDlist(self,genre):
		return list(set(genre.split(",")))

	#构建分析矩阵
	def buildMatrix(self,wdic,gdic,ddic):
		n,m = len(wdic),len(ddic)
		Matrix = np.zeros((n,m))
		for key in wdic.keys():
			Id = wdic.get(key)
			genre = gdic.get(Id)
			glist = list(set(genre.split(",")))
			for genreId in glist:
				yId = ddic.get(long(genreId))
				Matrix[Id][yId] = 1  #can define by yourself
		return Matrix

	#映射？？
	def mapData(self,Matrix):
		mat = Matrix.tolist()
		dalist = []
		count = 0
		for line in mat:
			lineD = []
			lineD.append(count)
			lineD.append(line)
			dalist.append(lineD)
			count += 1
		return dalist

	#
	def getMatrix(self):
		# data_d = data_deal()
		gdata = self.getCategory() 
		ddic = self.mapgenreID(gdata)
		# print ddic
		s_time = time.time()
		data1 = self.getsearchword()
		# print data1
		e_time = time.time()
		# print e_time - s_time
		s_time = time.time()
		data2 =  self.getsearchgenre()	
		e_time = time.time()
		# print e_time - s_time
		wdic,gdic = self.mapwordAgenre(data1,data2)
		# print len(wdic),len(gdic)
		# print wdic
		Matrix = self.buildMatrix(wdic,gdic,ddic)
		# daDic = self.mapData(Matrix)
		# return daDic
		return Matrix,wdic

	#获取数据记录根据竞品ID
	def getDataByID(self,IDs):
		word_list = []
		for ID in IDs:
			sql = "select distinct(word),priority,searchCount,genre from searchApp where searchApp like \'%"+ID +"%\'"
			print sql
			data = self.mysql.getWordPriority(sql)
			word_list.extend(data)
		return list(set(word_list))

	#devide data 
	def devide_data(self,word_list):
		data = []
		dat1 = []
		dat2 = []
		dat3 = []
		dat4 = []
		for word in word_list:
			dat1.append(word[0])
			dat2.append(word[1])
			dat3.append(word[2])
			dat4.append(word[3])
		data.append(dat1)
		data.append(dat2)
		data.append(dat3)
		data.append(dat4)
		return data


	#计算分析矩阵
	def calMatrix(self,data):
		gdata = self.getCategory() 
		ddic = self.mapgenreID(gdata)
		wdic,gdic = self.mapwordAgenre(data[0],data[3])
		Matrix = self.buildMatrix(wdic,gdic,ddic)
		return Matrix,wdic


	#依据竞品ID 获取关键词
	def getKeyWordDataByIds(self,complete_Ids):
		word_list = self.getDataByID(complete_Ids)
		data = self.devide_data(word_list)
		gdata = self.getCategory() 
		ddic = self.mapgenreID(gdata)
		wdic,gdic = self.mapwordAgenre(data[0],data[3])
		Matrix = self.buildMatrix(wdic,gdic,ddic)
		return Matrix,wdic

	#
	def getDadic(self):
		Matrix,wdic = self.getMatrix()
		return  self.mapData(Matrix)

	def getIddic(self,wdic):
		Iddic = {}
		for key in wdic.keys():
			Id = wdic.get(key)
			Iddic.setdefault(Id,key)
		return Iddic

def main():
	data_d = data_deal()
	# mat = data_d.getMatrix()
	# print len(mat[0])
	# word_list = data_d.getDataByID(('593499239','399353136','1003165584','737310995','1086911361','1080228178','1067238109','1017226508','909532141','903782554','914791167','952503776658','1070817891','1093026147','1067627594','1069231086'))
	# # data = data_d.getWordPrioandSearchC()
	# for word in word_list:
	# 	print word[0],word[1]

if __name__ == '__main__':
	main()
