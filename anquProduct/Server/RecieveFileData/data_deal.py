#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-08-02

import sys
sys.path.append('/home/mysql1/anqu/python/anquProduct/Server')
reload(sys)
sys.setdefaultencoding('utf8')
import config
from HqlSpark import HqlSpark

class data_deal():
	def __init__(self):
		self.myHql = HqlSpark()

	def insertData(self,data,tableName='search_',d_type='cn',state=False):
		self.myHql.insertDataFromStruct(data,tableName,d_type,state)

def main():
	pass

if __name__ == '__main__':
	main()

