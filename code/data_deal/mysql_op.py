#encodig=utf8mb4
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-14

import sys
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding("utf8") 
import chinese
import MySQLdb

class mysql_op():
	def __init__(self,host = config.Host_IP,user=config.dataBase_user,passwd = config.dataBase_passwd,database=config.dataBase):
		try :
			self.conn = MySQLdb.connect(host = host,user=user,passwd=passwd,db = database,port=3306,charset='utf8')
			self.cur =  self.conn.cursor()
		except MySQLdb.Error ,e:
			print "Mysql connect Error   %d:  %s"%(e.args[0],e.args[1])

	def  is_contains(self,line):
		if line[0].contain("\'"):
			return "insert into ansearchApp values(\"%s\",%d,%d,%d)"%line
		else :
			return "insert into ansearchApp values(\"%s\",%d,%d,%d)"%line

	#过滤searchApp表中的非汉语词
	def selectA(self):
		resault = self.cur.execute("select word,priority ,searchCount  ,genre ,type,time from searchApp")
		# data = self.cur.fetchall()
		# self.cur.execute("delete from ansearchApp")
		data_l = []
		count = 0
		chin = chinese.chinese()
		#创建ansearchApp表
		#create table ansearchApp(word varchar(255),priority int,searchCount int ,genre varchar(255),type int,time int);
		anS_conn = MySQLdb.connect(host = 'localhost',user='root',passwd='root',db = 'mysql',port=3306,charset='utf8')
		anS_cur = anS_conn.cursor()
		# print self.cur.rowcount
		word = {}
		for i in  xrange(self.cur.rowcount):#self.cur.fetchall():
			line = self.cur.fetchone()
			if line[0] in word:
				continue
			word.setdefault(line[0])
			if chin.is_chinese(line[0]) :
				data_l.append(line)
				# if line[0] == '轻':
					# print 1
				if chin.is_contains(line[0]):
					sql = "insert into ansearchApp values(\"%s\",%d,%d,\'%s\',%d,%d)"%line
				else : 
					sql = "insert into ansearchApp values(\'%s\',%d,%d,\'%s\',%d,%d)"%line
				# print sql
				anS_cur.execute(sql)
				anS_conn.commit()

	def delete(self):
		try :
			resault = self.cur.execute("select word from searchApp")
			data = self.cur.fetchall()
			chin = chinese.chinese()
			for line in data:
				if chin.is_chinese(line[0]) == False:
					sql = "delete from searchApp where word = \""+line[0]+"\""
					print sql
					try :
						re = self.cur.execute(sql)
						self.conn.commit()
					except MySQLdb.Error ,e :
						continue
		except MySQLdb.Error ,e:
			print "Mysql  execute error   %d  :  %s"%(e.args[0],e.args[1])

	def  select(self,select):
		try :
			resault = self.cur.execute(select)
			# print 'there has %s rows record ' % resault
			data = self.cur.fetchall()
			data_l = []
			for line in data:
				data_l.append(line[0])
			return list(data_l)
		except MySQLdb.Error ,e:
			print "Mysql  execute error   %d  :  %s"%(e.args[0],e.args[1])

	def insert(self,insert):
		try :
			resault = self.cur.execute(insert)
		except MySQLdb.Error ,e:
			print "mysql insert error  %d  : %s"%(e.args[0],e.args[1])

	def excute(self,sql):
		resault = self.cur.execute(sql)
		self.conn.commit()

	def getWordPriority(self,sql):
		try :
			# sql = 'select priority from %s where type = 1'%table
			# print sql
			self.cur.execute(sql)
			data = self.cur.fetchall()
			data_l = []
			# print "there has %d rows record"%len(data)
		 	for line in data:
				data_l.append(line)
			return list(data_l)
		except MySQLdb.Error ,e :
			print "Mysql execute error %d : %s"%(e.args[0],e.args[1])

def main():
	mysql = mysql_op("127.0.0.1","root","root","mysql")
	# data = mysql.getWordPriority("select  word,priority,searchCount from ansearchApp where type = 1 and genre like \"%6014%\"")
	# for line in data:
		# print line[0],line[1],line[2]
	# 数据去重，过滤速度慢
	# mysql.selectA()

if __name__ == '__main__':
	main()



