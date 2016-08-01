#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-25

import sys
sys.path.append('/home/mysql1/anqu/python/code/Tools')
sys.path.append('/home/mysql1/anqu/python/anquProduct/Server')
reload(sys)
sys.setdefaultencoding('utf8')
import config 


from pyspark import SparkConf,SparkContext
from pyspark.sql import HiveContext
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,LongType
# from selectWord import selectWord as sw
from pyspark.sql import Row
import all_shame as als

class HqlSpark():
	# init Spark sql 
	def __init__(self):
		self.conf = SparkConf().setAppName("my_hive")
		self.sc = SparkContext(conf=self.conf)
		self.sql = HiveContext(self.sc)
		database = self.sql.sql('show databases').collect()
		have_hive = True
		for data in database:
			if 'myhive'.find(data['result']) >= 0:
				have_hive = False
		if have_hive :
			print 'init myhive database!'
			self.sql.sql('create database myhive')
		self.sql.sql('use myhive')
		# print self.sql.sql("show tables").collect()

	def refreshTable(self,tableName):
		self.sql.refreshTable(tableName)

	#create table 
	def createTable(self,sql_sentence):
		table_name = sql_sentence.split(' ')[2]
		self.sql.sql(sql_sentence)
		self.sql.refreshTable(table_name)
		print 'create table %s success'%table_name

	#insert data into table
	def  insertData(self,sql_sentence):
		self.sql.sql(sql_sentence)

	# insert data into table from data_struct 
	def insertDataFromStruct(self,data,tableName = 'searchapp_',d_type = 'cn',state=False):   #data tuple or list list   data,
		# rdd = self.sc.parallelize(data)
		in_data = self.sql.createDataFrame(data,als.searchApp_shame)
		# final_data = in_data
		if state:
			in_data.saveAsTable(tableName='searchapp_'+d_type,Source='metastore_db',mode='append')#   append  overwrite
		else:
			in_data.saveAsTable(tableName='searchapp_'+d_type,Source='metastore_db',mode='overwrite')

	# delete table 
	def deleteDataFromTable(self,table='searchapp_',d_type='ch'):
		sql_sentence = 'delete from '+table+d_type
		self.sql.dropTempTable(table+d_type)
		self.sql.refreshTable(table+d_type)

	def showTales(self):
		table_list = []
		tables = self.sql.sql('show tables').collect()
		for table in  tables:
			table_list.append(table['tableName'])
		return table_list

	def getData(self,sql_hive):
		# self.sql.registerDataFrameAsTable(self.sql,'searchapp_cn')
		datas = self.sql.sql(sql_hive).collect()
		return datas
		# for data in datas:
			# print data
		
def main():
	hqlS = HqlSpark()
	# hqlS.createTable('create table searchapp (word string,priority string,searchapp string,searchCount string,genre string,type string,time string)')
	# hqlS.insertData('insert into wordSelectFeature values(\'indianapolis indians\',4605,289,0,1)')
	# print hqlS.getData('select * from searchapp_cn limit 10')
	# hqlS.deleteDataFromTable(table='searchapp',d_type='')
	# data = sw().readObj('word_list.txt')
	# hqlS.insertDataFromStruct(data[1:10],d_type = 'cn',state=False)
	datas = hqlS.getData('select * from searchapp_cn limit 10')
	for data in datas:
		print data
	# hqlS.deleteDataFromTable()
	# re = hqlS.showTales()
	# for r in re:
		# print r
if __name__ == '__main__':
	main()
