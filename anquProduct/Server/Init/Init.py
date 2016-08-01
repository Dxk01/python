#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-29


import sys
sys.path.append('/home/mysql1/anqu/python/anquProduct/Server')
reload(sys)
sys.setdefaultencoding('utf8')
import config
from pyspark import SparkConf
from pyspark import SparkContext
from HqlSpark import HqlSpark
from file_op import file_op

#init run envirenment main database
class InitClass():
	def __init__(self):
		# conf = SparkConf().setAppName("init")
		# self.sc = SparkContext(conf=conf)
		self.myHql = HqlSpark()
		# pass

	def init_category(self):
		fp = file_op()
		category = fp.get_category()
		# self.sc.paralize
		self.myHql.insertDataFromStruct(category,'category','',False)

	def init_searchapp(self):
		#config.searchapp_cn[0:len(config.searchapp_cn)-13]+
		with open(config.searchapp_cn,'r') as fp:
			line = fp.readline()
			lines = []
			p = len(config.searchapp_cn)-15
			tableName = config.searchapp_cn[0:p]
			d_type = config.searchapp_cn[p:p+2]
			print tableName,d_type
			state = False  # False rewrite search table 
			while  line != None and len(line):
				lines.append(line[0:-4].split("###"))
				line = fp.readline()
				if len(lines) > 0 and len(lines) >= 3000:
					self.myHql.insertDataFromStruct(lines,tableName,d_type,state)
					state = True
					break
			if len(lines) > 0:
				self.myHql.insertDataFromStruct(lines,tableName,d_type,state)				

def main():
	init_c = InitClass()
	# init_c.init_category()
	init_c.init_searchapp()

if __name__ == '__main__':
	main()


