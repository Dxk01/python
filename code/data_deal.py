#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-15

import sys
sys.path.append("/home/spark1/python/")
sys.path.append("/home/spark/anqu/code")
reload(sys)
sys.setdefaultencoding('utf8') 

import mysql_op
import numpy as np
import time
# 
class data_deal():
	def __init__(self):
		self.mysql = mysql_op.mysql_op("127.0.0.1","root","root","mysql")

	def getCategory(self):
		return sorted(list(set(self.mysql.select('select genreID from _category'))))

	def getsearchword(self):
		# return list(self.mysql.select("select word, genre from searchApp"))
		return self.mysql.select("select word from ansearchApp where type=1")

	def getsearchgenre(self):
		return self.mysql.select("select genre from ansearchApp where type=1")

	def tranGenretoGenreIDList(self,genrelist):
		genreIDlist = []
		for genre in genrelist :
			# print genre.split(',')
			genreIDlist.append(list(set(genre.split(','))))

	def mapgenreID(self,data):
		count = 0
		ddic = {}
		for d in data:
			if ddic.has_key(d) == False:
				ddic.setdefault(d,count)
				count += 1
		return ddic

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

	def getGenreIDlist(self,genre):
		return list(set(genre.split(",")))

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

	def getMatrix(self):
		# data_d = data_deal()
		gdata = self.getCategory() 
		ddic = self.mapgenreID(gdata)
		# print ddic
		s_time = time.time()
		data1 = self.getsearchword()
		e_time = time.time()
		# print e_time - s_time
		s_time = time.time()
		data2 =  self.getsearchgenre()	
		e_time = time.time()
		# print e_time - s_time
		wdic,gdic = self.mapwordAgenre(data1,data2)
		# print len(wdic),len(gdic)
		Matrix = self.buildMatrix(wdic,gdic,ddic)
		# daDic = self.mapData(Matrix)
		# return daDic
		return Matrix,wdic

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
	mat = data_d.getMatrix()

if __name__ == '__main__':
	main()
