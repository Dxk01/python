#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-15

import sys
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
import MySQLdb
sys.setdefaultencoding('utf8') 

import mysql_op
import numpy as np
import time
from chinese import chinese
import MySQLdb

# from selectWord import selectWord
# 数据处理
class data_deal():
	#初始化
	def __init__(self):
		self.mysql = mysql_op.mysql_op(config.Host_IP,config.dataBase_user,config.dataBase_passwd,config.dataBase)
	
	# 获取App store 的类别ID
	def getCategory(self):
		return sorted(list(set(self.mysql.select('select genreID from _category'))))
	
	#获取searchApp 表的word
	def getsearchword(self,sql="select word from ansearchApp where type=1 and genre like \'%6014%\'"):
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
		for i in xrange(length):
			if word[i] in wdic:
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
		sql = 'select distinct(word),priority,searchCount,genre from ansearchApp'
		words = self.mysql.getWordPriority(sql)
		for word in words:
			if word[0] in thinkWord:
				data_thinkWord.append(word)
		return data_thinkWord

	def mapwordAgenreOnAll(self,word_list):
		wdic = {}
		count = 0
		genredic = {}
		length = len(word)
		for i in xrange(length):
			if word[i] in wdic:
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

	#获取去重后的GenreID 列表
	def getGenreIDlist(self,genre):
		return list(set(genre.split(",")))

	#构建分析矩阵
	def buildMatrix(self,wdic,gdic,ddic):
		print len(wdic)
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
		gdata = self.getCategory() 
		ddic = self.mapgenreID(gdata)
		s_time = time.time()
		data1 = self.getsearchword()
		e_time = time.time()
		s_time = time.time()
		data2 =  self.getsearchgenre()	
		e_time = time.time()
		wdic,gdic = self.mapwordAgenre(data1,data2)
		Matrix = self.buildMatrix(wdic,gdic,ddic)
		return Matrix,wdic

	#获取数据记录根据竞品ID   chinese
	def getDataByID_ch(self,IDs):
		if IDs == None or len(IDs) == 0:
			return []
		sql = "select count(word) from searchApp"
		mysqlconn = MySQLdb.connect(host = config.Host_IP,user=config.dataBase_user,passwd=config.dataBase_passwd,db = config.dataBase,port=config.dataBase_port,charset='utf8')
		mysqlcur = mysqlconn.cursor()
		re = mysqlcur.execute(sql)
		chin = chinese()
		word_re = []
		num = mysqlcur.fetchall()[0][0]
		blockSize = 10000
		div = num / 10000 + 1

		for i in xrange(div):
			msql = 'select word,searchApp from searchApp limit %d , 10000'%(i*10000)
			# print msql
			re = mysqlcur.execute(msql)
			words = mysqlcur.fetchall()
			for word in words:
				if chin.is_chinese(word[0]):
					appId = word[1].split(',')
					for  ids in IDs:
						if ids in appId:
							word_re.append(word[0])
							break
			print 'read ',i,'times'
		return  word_re

	#获取数据记录根据竞品ID   english
	def getDataByID_en(self,IDs):
		if IDs == None or len(IDs) == 0:
			return []
		sql = "select count(word) from searchApp"
		mysqlconn = MySQLdb.connect(host = config.Host_IP,user=config.dataBase_user,passwd=config.dataBase_passwd,db = config.dataBase,port=config.dataBase_port,charset='utf8')
		mysqlcur = mysqlconn.cursor()
		re = mysqlcur.execute(sql)
		chin = chinese()
		word_re = []
		num = mysqlcur.fetchall()[0][0]
		blockSize = 10000
		div = num / 10000 + 1

		for i in xrange(div):
			msql = 'select word,searchApp from searchApp limit %d , 10000'%(i*10000)
			# print msql
			re = mysqlcur.execute(msql)
			words = mysqlcur.fetchall()
			for word in words:
				if chin.is_english(word[0]):
					appId = word[1].split(',')
					for  ids in IDs:
						if ids in appId:
							word_re.append(word[0])
							break
			print 'read ',i,'times'
		return  word_re

	#词的去重  chinese
	def delRepeatWord_ch(self,word_list):
		word_dic = {}
		chi = chinese()
		for word in word_list:
			if word[0] in word_dic:
				word_list.remove(word)
				continue
			else:
				if chi.is_chinese(word[0]):
					word_dic.setdefault(word[0])
				else:
					word_list.remove(word)
		return list(set(word_list))

	#词的去重  chinese
	def delRepeatWord_en(self,word_list):
		word_dic = {}
		chi = chinese()
		for word in word_list:
			if word[0] in word_dic:
				word_list.remove(word)
				continue
			else:
				if chi.is_english(word[0]):
					word_dic.setdefault(word[0])
				else:
					word_list.remove(word)
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


	#计算分析矩阵,和
	def calMatrix(self,data):
		gdata = self.getCategory() 
		ddic = self.mapgenreID(gdata)
		wdic,gdic = self.mapwordAgenre(data[0],data[3])
		Matrix = self.buildMatrix(wdic,gdic,ddic)
		return Matrix,wdic

	#计算分析矩阵
	def calMatrixByWordNews(self,words):
		gdata = self.getCategory()
		ddic = self.mapgenreID(gdata)
		return self.mapwordAgenerDic(words,ddic)

	#映射字典构建矩阵
	def mapwordAgenerDic(self,words,ddic):
		Matrix = np.zeros((len(words),len(ddic)))
		for i in xrange(len(words)):
			glist = words[i][3].split(',')
			for p_l in glist:
				p = ddic[long(p_l)]
				Matrix[i][p] = 1
		return Matrix

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
	# word_list = data_d.getDataByID([u'333206289', u'724295527', u'1090254952', u'1080608190', u'955253735', u'394075284', u'1046617847', u'1067721155', u'1061531453', u'996509117', '962734163', u'423084029', u'475966832', u'489782456', u'531761928', u'1014227673', u'407925512', u'438865278', u'1076606734', u'429885089', u'453718989', u'1075872386', u'919854496', u'414478124', u'393765873', u'412395632', u'409563112', u'1071403903', u'395893124', u'444934666', u'989673964', u'991018252', '994120614', u'592331499', u'1099554323', '1111594089', u'932299405', u'1042545880', u'1076471738', u'791532221', u'1027688889'])
	# print len(word_list)
	# # select = SW()
	# # select.writeObj(word_list,"word_list.txt")
	# # word_list = select.readObj("word_list.txt")
	# data = data_d.getWordPrioandSearchC(word_list)
	# for word in data:
	# 	print word[0],word[1]

if __name__ == '__main__':
	main()
