#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-25

import sys
sys.path.append('/home/mysql1/anqu/python/code/Tools')
reload(sys)
sys.setdefaultencoding('utf8') 

from pyspark import SparkConf,SparkContext
from pyspark.sql import HiveContext
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,LongType
from selectWord import selectWord as sw
from pyspark.sql import Row
import all_shame as als

class HqlSpark():
	# init Spark sql 
	def __init__(self):
		self.conf = SparkConf().setAppName("my_hive")
		print type(self.conf)
			# print da
		self.sc = SparkContext(conf=self.conf)
		self.sql = HiveContext(self.sc)

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
	def insertDataFromStruct(self,data,d_type = 'cn',state=False):   #data tuple or list list   data,
		# rdd = self.sc.parallelize(data)
		in_data = self.sql.createDataFrame(data,als.searchApp_shame)
		# final_data = in_data
		final_data = in_data.dropDuplicates(["word",])
		del(in_data)
		final_data = final_data.collect()
		final_data = self.sql.createDataFrame(final_data,als.searchApp_shame)
		if state:
			final_data.saveAsTable(tableName='searchapp_'+d_type,Source='metastore_db',mode='append')#   append  overwrite
		else:
			final_data.saveAsTable(tableName='searchapp_'+d_type,Source='metastore_db',mode='overwrite')

	# delete table 
	def deleteDataFromTable(self,table='searchapp_',d_type='ch'):
		sql_sentence = 'delete from '+table+d_type
		self.sql.dropTempTable(table+d_type)
		self.sql.refreshTable(table+d_type)

	def getData(self,sql_hive):
		pass
		
def main():
	hqlS = HqlSpark()
	# hqlS.createTable('create table wordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int)')
	# hqlS.insertData('insert into wordSelectFeature values(\'indianapolis indians\',4605,289,0,1)')
	# hqlS.getData('select * from searchapp_cn limit 1')
	# hqlS.deleteDataFromTable(table='searchapp',d_type='')
	# data = sw().readObj('word_list.txt')
	# hqlS.insertDataFromStruct(data,d_type = 'cn',state=False)
	hqlS.deleteDataFromTable()
if __name__ == '__main__':
	main()
