#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-23

import sys
sys.path.append("/home/spark/anqu/python/code/data_deal")
sys.path.append("/home/spark/anqu/python/code/Tools")
sys.path.append("/home/spark/anqu/python/code/wordAnalysis")
reload(sys)
sys.setdefaultencoding('utf8') 

import MySQLdb
import mysql_op
import data_deal
import calculSimilarity
import chinese
import cPickle as pickle
import time

class selectWord():
	"""docstring for ClassName"""
	def __init__(self):
		self.my_data = data_deal.data_deal()
	#结果写入数据库
	def print_line(self,mysql,x,y,z):
		chin = chinese.chinese()

		try :
			# print len(x)
			# print x[0],x[1],x[2]
			if chin.is_contains(x[0]):
				sql = "insert into wordSelectFeature values(\"%s\",%d,%d,%d,%d)"%(str(x[0]),x[1],x[2],y,z)
			else:
				sql = "insert into wordSelectFeature values(\'%s\',%d,%d,%d,%d)"%(str(x[0]),x[1],x[2],y,z)
			# print sql
			# mysql = mysql_op.mysql_op()
			# mysql.excute("delete from wordSelectFeature")
			mysql.excute(sql)
			# time.sleep(0.01)
		except Exception, e:
			print "Mysql connect Error  %s"%(e.args[0])
			return 

	#插入数据到数据库表词以及词的选择特征数据（热度、竞争度、聚类相似度、类簇）
	def insert_analysis_data(self):
		#加载分析结果
		data = self.readObj('data.txt')
		similarity = self.readObj('similarity.txt')
		#/home/spark/anqu/python/code/Cluster/Som_
		resault = self.readObj('resault.txt')
		#写入数据库
		# print len(data)
		# print len(similarity)
		# print len(resault)
		# self.mysql = mysql_op.mysql_op()
		mysql = mysql_op.mysql_op()
		mysql.excute("delete from wordSelectFeature")

		# 创建存储word的相关属性的列表
		# create table wordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int);
		map(lambda x,y,z: self.print_line(mysql,x,y,z),data,similarity,resault)
		# for line in data:

	def insert_data(self,word,similarity,resault):
		mysql = mysql_op.mysql_op()
		mysql.excute("delete from wordSelectFeature")
		# 创建存储word的相关属性的列表
		# create table wordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int);
		map(lambda x,y,z: self.print_line(mysql,x,y,z),word,similarity,resault)
	#
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

	#推荐词选择
	def getBetterPriorityWord(self,clusters,topWord = 20):
		datas = []
		for cluster in clusters:
			str_cluster = ''
			for cluster_id in cluster:
				str_cluster += str(cluster_id)+','
			str_cluster += str(0)
			sql = 'select * from wordSelectFeature where cluster in (%s) and searchCount < 1500 order by priority desc limit %d'%(str_cluster,topWord)
			mysql = mysql_op.mysql_op()
			data = mysql.getWordPriority(sql)
			datas.append(data)
		self.write_to_local(datas,topWord)

	#推荐品类词
	def getBetterClassWord(self,clusters,topWord=20):
		datas = []
		for cluster in clusters:
			str_cluster = ''
			for cluster_id in cluster:
				str_cluster += str(cluster_id) +','
			str_cluster += '-1'
			sql = 'select * from wordSelectFeature where cluster in (%s) and searchCount >= 6000 order by priority desc limit %d'%(str_cluster,topWord)
			data = mysql_op.mysql_op().getWordPriority(sql)
			datas.append(data)
		self.write_to_local(datas,topWord,'ClassWord',2)

	#将推荐的结果写入到文件
	def write_to_local(self,Datas,topWord = 20,filename='keyword',type=1):
		# filepath = "/home/spark/anqu/analysisResault/"
		ISOTIMEFORMAT='%Y-%m-%d %X'
		dateTime =  time.strftime( ISOTIMEFORMAT, time.localtime())
		filepath = '/home/spark/anqu/analysisResault/'
		filename = filepath+filename+"/"+filename+dateTime+".txt"
		fp = open(filename,'a')
		count = 1
		if type == 1:
			fp.write("关键字的推荐词：\n")
		else :
			fp.write("品类词的推荐词：\n")
		for KeyWords in Datas:
			fp.write("第  %d  维度       Top  %d 关键词\n"%(count,topWord))
			for word in KeyWords:
				fp.write(word[0] + "  " +str(word[1])+"   "+str(word[2])+"  "+str(word[4])+"\n")
			count += 1
			fp.write("\n\n\n")
		fp.close()

	#数据对象写入文件存储
	def writeObj(self,obj,file):
		filepath = '/home/spark/anqu/analysisResault/Object/'
		f = open(filepath+file, 'wb')
		pickle.dump(obj, f)
		f.close()

	#读取文件中的数据对象
	def readObj(self,file):
		filepath = '/home/spark/anqu/analysisResault/Object/'
		f = open(filepath+file,'rb')
		return pickle.load(f)

def main():
	SelectWord = selectWord()

	# SelectWord.selectWord()
	# SelectWord.insert_analysis_data()

if __name__ == '__main__':
	main()
