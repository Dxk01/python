#encodig=utf8mb4
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-14

import MySQLdb
import sys
sys.path.append("/home/spark/anqu/code/Tools")
reload(sys)
sys.setdefaultencoding("utf8") 
import chinese

class mysql_op():
	def __init__(self,host = 'localhost',user='root',passwd = 'root',database='mysql'):
		try :
			self.conn = MySQLdb.connect(host = host,user=user,passwd=passwd,db = database,port=3306,charset='utf8')
			self.cur =  self.conn.cursor()
		except MySQLdb.Error ,e:
			print "Mysql connect Error   %d:  %s"%(e.args[0],e.args[1])

	def  is_contains(self,line):
		if line[0].contain("\'"):
			return "insert into ansearchApp values(\"%s\",%d,%s,%d,%s,%d,%d)"%line
		else :
			return "insert into ansearchApp values(\"%s\",%d,%s,%d,%s,%d,%d)"%line

	def selectA(self):
		resault = self.cur.execute("select * from searchApp")
		data = self.cur.fetchall()
		data_l = []
		count = 0
		chin = chinese.chinese()
		for line in data:#self.cur.fetchall():
			if chin.is_chinese(line[0]):
				data_l.append(line)
				if chin.is_contains(line[0]):
					sql = "insert into ansearchApp values(\"%s\",%d,\'%s\',%d,\'%s\',%d,%d)"%line
				else : 
					sql = "insert into ansearchApp values(\'%s\',%d,\'%s\',%d,\'%s\',%d,%d)"%line
				self.cur.execute(sql)
				self.conn.commit()

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
	data = mysql.getWordPriority("select  word,priority,searchCount from ansearchApp where type = 1 and genre like \"%6014%\"")
	for line in data:
		print line[0],line[1],line[2]


if __name__ == '__main__':
	main()


