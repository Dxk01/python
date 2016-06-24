#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-23

import sys
sys.path.append("/home/spark/anqu/code/data_deal")
sys.path.append("/home/spark/anqu/code/Tools")
sys.path.append("/home/spark/anqu/code/wordAnalysis")
reload(sys)
sys.setdefaultencoding('utf8') 

import MySQLdb
import mysql_op
import data_deal
import calculSimilarity
import chinese
import cPickle as pickle

class selectWord():
	"""docstring for ClassName"""
	def __init__(self):
		self.my_data = data_deal.data_deal()
	def print_line(self,x,y,z):
		chin = chinese.chinese()

		try :
			if chin.is_contains(x[0]):
				sql = "insert into wordSelectFeature values(\"%s\",%d,%d,%d,%d)"%(str(x[0]),x[1],x[2],y,z)
			else:
				sql = "insert into wordSelectFeature values(\'%s\',%d,%d,%d,%d)"%(str(x[0]),x[1],x[2],y,z)
			print sql
			mysql = mysql_op.mysql_op()
			# mysql.excute("delete from wordSelectFeature")
			mysql.excute(sql)
		except Exception, e:
			print "Mysql connect Error   %s"%(e.args[0])
			return 

	def insert_analysis_data(self):
		#加载分析结果
		data = self.readObj('data.txt')
		similarity = self.readObj('similarity.txt')
		resault = self.readObj('resault.txt')
		#写入数据库
		print len(data)
		# self.mysql = mysql_op.mysql_op()
		mysql = mysql_op.mysql_op()
		mysql.excute("delete from wordSelectFeature")
		# 创建存储word的相关属性的列表
		# create table wordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int);
		map(lambda x,y,z: self.print_line(x,y,z),data,similarity,resault)
		# for line in data:


	def selectWord(self):
		# print u'获取词的集合'
		data = self.my_data.getWordPrioandSearchC()
		# print '计算样本集的各类簇的词的相似度'
		# print '返回相似度向量和聚类的样本分类结果'
		similarity,resault = calculSimilarity.similarity().run()
		self.writerObj(similarity,'similarity.txt')
		self.writerObj(resault,'resault.txt')
		self.writerObj(data,'data.txt')

		# print '返回数据',len(data),len(resault)
		# self.mysql = mysql_op.mysql_op()
		#创建存储word的相关属性的列表
		#  create table wordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int);
		# map(lambda x,y,z: self.print_line(x,y,z),data,similarity,resault)

	def writerObj(self,obj,file):
		f = open(file, 'wb')
		pickle.dump(obj, f)
		f.close()

	def readObj(self,file):
		f = open(file,'rb')
		return pickle.load(f)

def main():
	SelectWord = selectWord()
	# SelectWord.selectWord()
	SelectWord.insert_analysis_data()

if __name__ == '__main__':
	main()
